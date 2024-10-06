import ast
from typing import *

from . import tree as Tree
from .symbol_table import SymbolTable, SymbolType

from .conversion_error import *


class MPTreeConverter:
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

    def __init__(self, symbol_table: SymbolTable=None) -> None:
        # TODO
        # 1. lineno
        # 2. change converter to use m_invert...
        # 3. process python's ast to convert m_invert to ~
        self._symbol_table = symbol_table if symbol_table is not None else SymbolTable()

    def get_symbol_table(self) -> SymbolTable:
        return self._symbol_table

    def convert(self, node: Tree.Node) -> Optional[ast.AST]:
        if isinstance(node, Tree.Program):
            self._flag_in_lhs = False
            self._flag_in_rhs = False
            
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
                # Converting left value
                self._flag_in_lhs = True
                if len(node.lvalue) > 1:
                    targets = [ast.Tuple(elts=[self._convert_tree(lval, ast.Store()) for lval in node.lvalue], ctx=ast.Store())]
                else:
                    targets = [self._convert_tree(node.lvalue[0], ast.Store())]
                self._flag_in_lhs = False

                # Converting right value
                self._flag_in_rhs = True
                rvalue = self._convert_tree(node.rvalue)
                self._flag_in_rhs = False

                # Process for symbol table
                # A. For anonymousFunction
                if isinstance(rvalue, ast.Lambda):
                    assert len(targets) == 1
                    self._symbol_table.add_symbol(ast.unparse(targets[0]), SymbolType.FUNC)
                elif isinstance(rvalue, ast.Name) and getattr(rvalue, '_custom_flag', 'None') == "matlab_function_handle":
                    assert len(targets) == 1
                    self._symbol_table.add_symbol(ast.unparse(targets[0]), SymbolType.FUNC)

                # B. Determine targets:
                else:
                    for target in targets:
                        # 1. x
                        if isinstance(target, ast.Name):
                            self._symbol_table.add_symbol(ast.unparse(target), SymbolType.VAR)

                        # 2. x{1}
                        elif isinstance(target, ast.Call) and getattr(target, '_custom_flag', 'None') == "matlab_cell_access":
                            self._symbol_table.add_symbol(ast.unparse(target.args[0]), SymbolType.VAR)

                        # 3. x.b
                        elif isinstance(target, ast.Call) and getattr(target, '_custom_flag', 'None') == "matlab_struct_access":
                            self._symbol_table.add_symbol(ast.unparse(target.args[0]), SymbolType.VAR)

                        # 4-1. x(1)
                        elif isinstance(target, ast.Call) and getattr(target, '_custom_flag', 'None') == "matlab_array_access":
                            self._symbol_table.add_symbol(ast.unparse(target.args[0]), SymbolType.VAR)

                        # 4-2. x(1)
                        elif isinstance(target, ast.Call) and isinstance(target.func, ast.Name):
                            self._symbol_table.add_symbol(ast.unparse(target.func), SymbolType.VAR)
                
                lineno = 1
                # lineno = node.lvalue[-1].value.ln + 1
                return ast.Assign(
                    targets=targets,
                    value=rvalue,
                    lineno=lineno
                )
            
            elif isinstance(node, Tree.MatrixExpression):
                return ast.Call(
                    func=ast.Name(id='matlab_array', ctx=ast.Load()),
                    args=[
                        ast.List(
                            elts=[ast.List(elts=[self._convert_tree(elem) for elem in row], ctx=ast.Load()) for row in node.elements],
                            ctx=ast.Load()
                        )
                    ],
                    keywords=[],
                    _custom_flag='matlab_array'
                )
            
            elif isinstance(node, Tree.CellArrayExpression):
                return ast.Call(
                    func=ast.Name(id='matlab_cell', ctx=ast.Load()),
                    args=[
                        ast.List(
                            elts=[ast.List(elts=[self._convert_tree(elem) for elem in row], ctx=ast.Load()) for row in node.elements],
                            ctx=ast.Load()
                        )
                    ],
                    keywords=[],
                    _custom_flag='matlab_cell'
                )
            
            elif isinstance(node, Tree.ColonArray):
                if node.step:
                    func_arg = ast.List(elts=[self._convert_tree(node.start), self._convert_tree(node.stop), self._convert_tree(node.step)], ctx=ast.Load())
                else:
                    func_arg = ast.List(elts=[self._convert_tree(node.start), self._convert_tree(node.stop)], ctx=ast.Load())
                
                return ast.Call(
                    func=ast.Name(id='matlab_arange', ctx=ast.Load()),
                    args=[func_arg],
                    keywords=[],
                    _custom_flag='matlab_arange'
                )
            
            elif isinstance(node, Tree.ArrayAccess):
                return self._array_access(node)
            
            elif isinstance(node, Tree.CellArrayAccess):
                return ast.Call(
                    func=ast.Name(id='matlab_cell_access', ctx=ast.Load()),
                    args=[
                        self._convert_tree(node.identifier),
                        ast.List(
                            elts=[self._convert_tree(index) for index in node.arguments.indices],
                            ctx=ast.Load()
                        )
                    ],
                    keywords=[],
                    _custom_flag='matlab_cell_access'
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
                    
                return ast.Call(
                    func=ast.Name(id='matlab_struct_access', ctx=ast.Load()),
                    args=[
                        self._convert_tree(node.identifier),
                        ast.List(
                            elts=args,
                            ctx=ast.Load()
                        )
                    ],
                    keywords=[],
                    _custom_flag='matlab_struct_access'
                )
            
            elif isinstance(node, Tree.FunctionDefinition):
                fn_name = node.name.value.val

                self._symbol_table.add_symbol(fn_name, SymbolType.FUNC)
                self._symbol_table.enter_scope(fn_name)

                input_args = [ast.arg(arg=self._convert_tree(param).id) for param in node.input_params]
                func_body = self._body_list_to_ast(node.body)
                ret_var = [ast.arg(arg=self._convert_tree(param).id) for param in node.output_params]
                if len(ret_var) == 1:
                    func_body.append(ast.Return(value=ret_var[0]))
                elif len(ret_var) > 1:
                    func_body.append(ast.Return(value=ast.Tuple(elts=ret_var)))
                    
                self._symbol_table.exit_scope()
                
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
                return ast.Name(id=node.value, ctx=ast.Load(), _custom_flag='matlab_function_handle')
            
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
                    assert isinstance(identifier, Tree.Identifier), "Invalid global variable"
                    persistent_var.append(identifier.value.val)
                return ast.Global(names=persistent_var, _custom_flag='matlab_presistent')
            
            elif isinstance(node, Tree.BreakStatement):
                return ast.Break()
            
            elif isinstance(node, Tree.ContinueStatement):
                return ast.Continue()
            
            elif isinstance(node, Tree.ReturnStatement):
                return ast.Call(func=ast.Name(id='matlab_return', ctx=ast.Load()), args=[], keywords=[], _custom_flag='matlab_return')
            
            elif isinstance(node, Tree.FunctionCall):
                if self._flag_in_lhs:
                    return self._array_access(node)

                func_name = self._convert_tree(node.identifier)

                # Check symbol table
                if isinstance(func_name, ast.Name):
                    if self._symbol_table.lookup(func_name.id) is SymbolType.VAR:
                        return self._array_access(node)

                if node.arguments is not None:
                    arguments = [self._convert_tree(arg) for arg in node.arguments.indices if arg is not None]
                else:
                    arguments = []

                # Check default path relative command in Matlab
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
                    keywords=[],
                    _custom_flag='matlab_op'
                )
                
            elif isinstance(node, Tree.UnaryOperation):
                op = self._matlab_op_map.get(node.operator, None)
                return ast.Call(
                    func=ast.Name(id=op, ctx=ast.Load()),
                    args=[self._convert_tree(node.operand)],
                    keywords=[],
                    _custom_flag='matlab_op'
                )
                
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

    def _array_access(self, node: Tree.Node) -> ast.AST:
        return ast.Call(
            func=ast.Name(id='matlab_array_access', ctx=ast.Load()),
            args=[
                self._convert_tree(node.identifier),
                ast.List(
                    elts=[self._convert_tree(index) for index in node.arguments.indices],
                    ctx=ast.Load()
                )
            ],
            keywords=[],
            _custom_flag='matlab_array_access'
        )
    
    def _check_dir_change(self, func_name: ast.AST, args: list[ast.AST]) -> None:
        match func_name.id.lower():
            case "cd":
                self._symbol_table.cd(ast.unparse(args))
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
            case "addpath":
                # Parse the arguments of the addpath
                path = []
                for arg in args:
                    if isinstance(arg, ast.Constant):
                        assert isinstance(arg.value, str)
                        if arg.value == "-frozen":
                            pass
                        elif arg.value == "-begin":
                            pass
                        elif arg.value == "-end":
                            pass
                        else:
                            path.append(arg.value)
                    elif isinstance(arg, ast.Call):
                        assert isinstance(arg.func, ast.Name) and arg.func.id == 'genpath', "Unsupport addpath with another function call"
                        assert len(arg.args) <= 1
                        if len(arg.args) == 1:
                            assert isinstance(arg.args[0], ast.Constant) and isinstance(arg.args[0].value, str)
                            path.append(arg.args[0].value)
                
                self._symbol_table.add_path(path)
            case "rmpath":
                pass
            case "genpath":
                pass
