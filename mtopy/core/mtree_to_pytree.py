import ast
from typing import *

from . import tree as Tree
from .function_table import FunctionTable

from .conversion_error import *


class MPTreeConverter:
    # Creat matlab datatype
    #  Data type            |   matlab code  |   transformed code   |       Note
    # matlab array          |   [2 3; 4, 5]  |   [[2, 3], [4, 5]]   |  two dim list
    # matlab cell array     |   {2 3; 4, 5}  |  [[[2, 3], [4, 5]]]  | three dim list
    # matlab structure      |        -       |          -           | use struct to initialize
    # matlab colon array    |    2 : 1 : 10  |     [2, 10, 1]       |  one dim list

    # Access matlab datatype
    #  Data type            |  matlab code   |   transformed code   |      Note
    # matlab array          |   a(2, 3)      |     ((a, 2, 3))      |  two dim tuple
    # matlab cell array     |   c{4, 5}      |    (((c, 4, 5)))     | three dim tuple
    # matlab structure      |    s.e         |       (s, 'e')       |  one dim tuple

    # Special matlab keywords
    _matlab_persistent = "m_persistent"

    # Matlab operation
    _matlab_op_map = {
        'short_circuit_or': "or",
        'short_circuit_and': "and",
        'element_wise_or': "bitor",
        'element_wise_and': "bitand",
        'less_than': "lt",
        'less_than_or_equal_to': "le",
        'greater_than': "gt",
        'greater_than_or_equal_to': "ge",
        'equal_to': "eq",
        'not_equal_to': "ne",
        'addition': "plus",
        'subtraction': "minus",
        'unary_plus': "uplus",
        'unary_minus': "uminus",
        'logical_negation': "not",

        "multiplication": "times",
        "right_division": "rdivide",
        "left_division": "ldivide",
        "matrix_multiplication": "mtimes",
        "matrix_right_division": "mrdivide",
        "matrix_left_division": "mldivide",
        "power": "power",
        "matrix_power": "mpower",
        "transpose": "transpose",
        "hermitian": "ctranspose",
    }

    def __init__(self, function_table: FunctionTable=None) -> None:
        # TODO
        # 1. lineno
        # 2. change converter to use m_invert...
        # 3. process python's ast to convert m_invert to ~
        self._function_table = function_table if function_table is not None else FunctionTable()

    def get_function_table(self) -> FunctionTable:
        return self._function_table

    def convert(self, node: Tree.Node) -> Optional[ast.AST]:
        if isinstance(node, Tree.Program):
            return ast.Module(
                body=self._body_list_to_ast(node.body),
                type_ignores=[]
            )
        else:
            return None

    def _convert_tree(self, node: Tree.Node, ctx_typ=ast.Load()) -> Optional[ast.AST]:
        assert not isinstance(node, Tree.Program), "Nested tree is not allowed"

        try:
            # Terminal symbols
            if isinstance(node, Tree.Number):
                s = node.value.val
                if 'e' in s.lower():
                    return ast.Constant(value=float(s))
                elif '.' in s:
                    return ast.Constant(value=float(s))
                elif s.lower().startswith('0x'):
                    return ast.Constant(value=int(s, 16))
                else:
                    return ast.Constant(value=int(s))
                
            elif isinstance(node, Tree.ImagNumber):
                return ast.Constant(value=complex(0, float(node.value.val[:-1])))
            
            elif isinstance(node, Tree.String):
                return ast.Constant(value=str(node.value.val[1:-1]))
            
            elif isinstance(node, Tree.Identifier):
                return ast.Name(id=str(node.value.val), ctx=ctx_typ)
            
            elif isinstance(node, Tree.Ignore):
                return ast.Name(id='_', ctx=ctx_typ)
            
            elif isinstance(node, Tree.COLON):
                return ast.Slice()
            
            elif isinstance(node, (Tree.WhiteSpace, Tree.Comment, Tree.Ellipsis, Tree.EndOfLine)):
                return None
            
            elif isinstance(node, Tree.Assignment):
                targets = [self._convert_tree(lval, ast.Store()) for lval in node.lvalue]
                rvalue = self._convert_tree(node.rvalue)

                # Check for overwriting function variables
                for target in targets:
                    if self._function_table.lookup(ast.unparse(target)):
                        raise BadConversionError("Please do not assign")

                # For AnonymousFunction
                if isinstance(rvalue, ast.Lambda):
                    assert len(targets) == 1
                    self._function_table.add_function(ast.unparse(targets[0]))
                    
                lineno = 1
                # lineno = node.lvalue[-1].value.ln + 1
                return ast.Assign(
                    targets=targets,
                    value=rvalue,
                    lineno=lineno
                )
            
            elif isinstance(node, Tree.MatrixExpression):
                return ast.List(elts=[ast.List(elts=[self._convert_tree(elem) for elem in row], ctx=ast.Load()) for row in node.elements], ctx=ast.Load())
            
            elif isinstance(node, Tree.CellArrayExpression):
                return  ast.List(
                    elts=[ast.List(elts=[ast.List(elts=[self._convert_tree(elem) for elem in row], ctx=ast.Load()) for row in node.elements], ctx=ast.Load())],
                    ctx=ast.Load()
                )
            
            elif isinstance(node, Tree.ColonArray):
                if node.step:
                    return ast.List(elts=[self._convert_tree(node.start), self._convert_tree(node.stop), self._convert_tree(node.step)], ctx=ast.Load())
                else:
                    return ast.List(elts=[self._convert_tree(node.start), self._convert_tree(node.stop)], ctx=ast.Load())
            
            elif isinstance(node, Tree.ArrayAccess):
                return ast.Tuple(elts=[ast.Tuple(elts=[self._convert_tree(node.identifier)] + [self._convert_tree(index) for index in node.arguments.indices], ctx=ast.Load())], ctx=ast.Load())
            
            elif isinstance(node, Tree.CellArrayAccess):
                return ast.Tuple(
                    elts=[ast.Tuple(elts=[ast.Tuple(elts=[self._convert_tree(node.identifier)] + [self._convert_tree(index) for index in node.arguments.indices], ctx=ast.Load())], ctx=ast.Load())],
                    ctx=ast.Load()
                )
            
            elif isinstance(node, Tree.StructAccess):
                args = []
                for arg in node.arguments:
                    arg = self._convert_tree(arg)
                    if isinstance(arg, ast.Name):
                        arg = ast.Constant(value=str(arg.id))
                    elif isinstance(arg, ast.Constant):
                        arg = ast.Constant(value=str(arg.value))
                    args.append(arg)

                return ast.Tuple(elts=[self._convert_tree(node.identifier)] + args, ctx=ast.Load())
            
            elif isinstance(node, Tree.FunctionDefinition):
                fn_name = node.name.value.val

                self._function_table.add_function(fn_name)
                self._function_table.enter_scope(fn_name)

                input_args = [ast.arg(arg=self._convert_tree(param).id) for param in node.input_params]
                func_body = self._body_list_to_ast(node.body)
                ret_var = [ast.arg(arg=self._convert_tree(param).id) for param in node.output_params]
                if len(ret_var) == 1:
                    func_body.append(ast.Return(value=ret_var[0]))
                elif len(ret_var) > 1:
                    func_body.append(ast.Return(value=ast.Tuple(elts=ret_var)))
                    
                self._function_table.exit_scope()
                
                return ast.FunctionDef(
                    name=fn_name,
                    args=ast.arguments(
                        posonlyargs=[],
                        args=input_args,
                        kwonlyargs=[],
                        kw_defaults=[],
                        defaults=[]
                    ),
                    body=func_body,
                    decorator_list=[],
                    lineno=1
                )
            
            elif isinstance(node, Tree.AnonymousFunction):
                return ast.Lambda(
                    args=ast.arguments(
                        posonlyargs=[],
                        args=[ast.arg(arg=self._convert_tree(param).id) for param in node.parameters],
                        kwonlyargs=[],
                        kw_defaults=[],
                        defaults=[]
                    ),
                    body=self._convert_tree(node.body[0])  # Assuming single expression for lambda body
                )
            
            elif isinstance(node, Tree.FunctionHandle):
                return ast.Name(id=node.value, ctx=ast.Load())
            
            elif isinstance(node, Tree.IfStatement):
                return ast.If(
                    test=self._convert_tree(node.condition),
                    body=self._body_list_to_ast(node.then_body),
                    orelse=self._convert_elseif_chain(node.elseif_clauses, node.else_body)
                )
            
            elif isinstance(node, Tree.ForLoop):
                return ast.For(
                    target=self._convert_tree(node.identifier),
                    iter=self._convert_tree(node.expression),
                    body=self._body_list_to_ast(node.body),
                    orelse=[],
                    lineno=1
                )
            
            elif isinstance(node, Tree.ParforLoop):
                raise NotImplementedConversionError("parfor", node)
            elif isinstance(node, Tree.SPMDStatement):
                raise NotImplementedConversionError("spmd", node)
            
            elif isinstance(node, Tree.WhileLoop):
                return ast.While(
                    test=self._convert_tree(node.condition),
                    body=self._body_list_to_ast(node.body),
                    orelse=[]
                )
            
            elif isinstance(node, Tree.SwitchStatement):
                return self._convert_switch_to_if(node)
            
            elif isinstance(node, Tree.TryCatchStatement):
                return ast.Try(
                    body=self._body_list_to_ast(node.try_body),
                    handlers=[ast.ExceptHandler(
                        type=self._convert_tree(node.exception) if node.exception is not None else None,
                        name=None,
                        body=self._body_list_to_ast(node.catch_body)
                    )],
                    orelse=[],
                    finalbody=[]
                )
            
            elif isinstance(node, Tree.GlobalStatement):
                global_var = []
                for identifier in node.identifiers:
                    assert isinstance(identifier, Tree.Identifier), "Invalid global variable"
                    global_var.append(identifier.value.val)
                return ast.Global(names=global_var)
            
            elif isinstance(node, Tree.PersistentStatement):
                persistent_var = []
                for identifier in node.identifiers:
                    assert isinstance(identifier, Tree.Identifier), "Invalid persistent variable"
                    persistent_var.append(self._convert_tree(identifier))

                return ast.Call(
                    func=ast.Name(id=self._matlab_persistent, ctx=ast.Load()),
                    args=persistent_var,
                    keywords=[]
                )
            
            elif isinstance(node, Tree.BreakStatement):
                return ast.Break()
            
            elif isinstance(node, Tree.ContinueStatement):
                return ast.Continue()
            
            elif isinstance(node, Tree.ReturnStatement):
                return ast.Return(value=None)
            
            elif isinstance(node, Tree.FunctionCall):
                func_name = self._convert_tree(node.identifier)
                if node.arguments is not None:
                    arguments = [self._convert_tree(arg) for arg in node.arguments.indices if arg is not None]
                else:
                    arguments = []

                if isinstance(func_name, ast.Name):
                    self._check_dir_change(func_name, arguments)
                
                return ast.Call(
                    func=func_name,
                    args=arguments,
                    keywords=[]
                )
            
            elif isinstance(node, Tree.BinaryOperation):
                op = self._matlab_op_map.get(node.operator, None)
                return ast.Call(
                    func=ast.Name(id=op, ctx=ast.Load()),
                    args=[self._convert_tree(node.left), self._convert_tree(node.right)],
                    keywords=[]
                )
                
                # if op is not None:
                #     if isinstance(op, (ast.And, ast.Or,)):
                #         return ast.BoolOp(
                #             op=op,
                #             values=[self._convert_tree(node.left), self._convert_tree(node.right)]
                #         )
                    
                #     elif isinstance(op, (ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.Eq, ast.NotEq)):
                #         return ast.Compare(
                #             left=self._convert_tree(node.left),
                #             ops=[op],
                #             comparators=[self._convert_tree(node.right)]
                #         )

                #     else:
                #         return ast.BinOp(
                #             left=self._convert_tree(node.left),
                #             op=op,
                #             right=self._convert_tree(node.right)
                #         )
                # else:
                #     convert_func = getattr(self.config.converter, node.operator)
                #     return convert_func(self._convert_tree(node.left), self._convert_tree(node.right))
            
            elif isinstance(node, Tree.UnaryOperation):
                op = self._matlab_op_map.get(node.operator, None)
                return ast.Call(
                    func=ast.Name(id=op, ctx=ast.Load()),
                    args=[self._convert_tree(node.operand)],
                    keywords=[]
                )
                # if op is not None:
                #     return ast.UnaryOp(
                #         op=op,
                #         operand=self._convert_tree(node.operand)
                #     )
                # else:
                #     convert_func = getattr(self.config.converter, node.operator)
                #     return convert_func(self._convert_tree(node.operand))
            
            raise NotImplementedError(f"Conversion not implemented for node type: {type(node)}")
            
        except NotImplementedConversionError as e:
            raise NotImplementedConversionError(e.message, e.node)
        
        except MPTreeConversionError as e:
            raise MPTreeConversionError(e.message, e.node)
        
        except Exception as e:
            raise MPTreeConversionError(str(e), node)

    def _body_list_to_ast(self, body: list[Tree.Node]) -> list[ast.AST]:
        body = [self._convert_tree(stmt) for stmt in body if stmt is not None]
        ast_body = []
        for b in body:
            if b is None:
                continue
            elif isinstance(b, ast.Assign):
                ast_body.append(b)
            else:
                ast_body.append(ast.Expr(value=b))
        
        if len(ast_body) == 0:
            ast_body = [ast.Pass()]
        
        return ast_body

    def _convert_elseif_chain(self, elseif_clauses: list[Tree.ElseIfClause], else_body: Optional[list[Tree.Node]]) -> list[ast.AST]:
        if not elseif_clauses and not else_body:
            return []
        
        if not elseif_clauses:
            return self._body_list_to_ast(else_body)
        
        next_clause = elseif_clauses.pop(0)
        if_body = self._body_list_to_ast(next_clause.body)

        return [ast.If(
            test=self._convert_tree(next_clause.condition),
            body=if_body,
            orelse=self._convert_elseif_chain(elseif_clauses, else_body)
        )]

    def _convert_switch_to_if(self, node: Tree.SwitchStatement) -> ast.If:
        if not node.cases:
            return ast.Pass()
        
        test_list = []
        body_list = []

        for case in node.cases:
            test_list.append(
                ast.Compare(
                    left=self._convert_tree(node.expression),
                    ops=[ast.Eq()],
                    comparators=[self._convert_tree(case.condition)]
                )
            )

            body_list.append(self._body_list_to_ast(case.body))

        if_ast = ast.If(
            test=test_list[-1],
            body=body_list[-1],
            orelse=self._body_list_to_ast(node.otherwise)
        )
        
        for i in reversed(range(len(test_list) - 1)):
            if_ast = ast.If(
                test=test_list[i],
                body=body_list[i],
                orelse=[if_ast]
            )

        return if_ast

    def _check_dir_change(self, func_name: ast.AST, args):
        match func_name.id.lower():
            case "cd":
                self._function_table.cd(ast.unparse(args))
            case "copyfile":
                pass
            case "delete":
                pass
            case "recycle":
                pass
            case "mkdir":
                pass
            case "movefile":
                pass
            case "rmdir":
                pass
