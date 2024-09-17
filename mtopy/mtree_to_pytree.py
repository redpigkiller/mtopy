import ast
import astor
from pathlib import Path
from typing import *
from rich import print as rprint
import warnings

from parse_matlab_code import Parser, Tree
from .converter import MatlabTypeConverter
from .symbol_table import SymbolTable


class MPTreeConversionError(Exception):
    def __init__(self, message, node):
        self.message = message
        self.node = node
        super().__init__(f"Error at node {node}: {message}")

class NotImplementedConversionError(MPTreeConversionError):
    """Exception for non-implemented"""
    def __init__(self, message, node):
        self.message = message
        self.node = node
        super().__init__(f"{message} not implemented: {node}", node)

class MPTreeConversionConfig:
    def __init__(self, converter: MatlabTypeConverter):
        self.converter: MatlabTypeConverter = converter()
        self.required_imports: Set[str] = set()


class MPTreeConverter:
    _binop_map = {
        'short_circuit_or': ast.Or(),
        'short_circuit_and': ast.And(),
        'element_wise_or': ast.BitOr(),
        'element_wise_and': ast.BitAnd(),
        'less_than': ast.Lt(),
        'less_than_or_equal_to': ast.LtE(),
        'greater_than': ast.Gt(),
        'greater_than_or_equal_to': ast.GtE(),
        'equal_to': ast.Eq(),
        'not_equal_to': ast.NotEq(),
        'addition': ast.Add(),
        'subtraction': ast.Sub(),
        'unary_plus': ast.UAdd(),
        'unary_minus': ast.USub(),
        'logical_negation': ast.Invert(),
        }

    def __init__(self, config: MPTreeConversionConfig=None) -> None:
        self.config: MPTreeConversionConfig = config

    def convert(self, node: Tree.Node, file_path: Optional[str]=None) -> Optional[ast.AST]:
        self._symbol_table = SymbolTable(file_path)

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
                return ast.Constant(value=str(node.value.val))
            elif isinstance(node, Tree.Identifier):
                return ast.Name(id=str(node.value.val), ctx=ctx_typ)
            elif isinstance(node, Tree.Ignore):
                return ast.Name(id='_', ctx=ctx_typ)
            elif isinstance(node, Tree.COLON):
                return ast.Slice()
            elif isinstance(node, (Tree.WhiteSpace, Tree.Comment, Tree.Ellipsis, Tree.EndOfLine)):
                return None
            
            elif isinstance(node, Tree.MatrixExpression):
                return self.config.converter.create_mat([[self._convert_tree(elem) for elem in row] for row in node.elements])
            
            elif isinstance(node, Tree.CellArrayExpression):
                return self.config.converter.create_cell([[self._convert_tree(elem) for elem in row] for row in node.elements])

            elif isinstance(node, Tree.ColonArray):
                return self.config.converter.arange(
                    start=self._convert_tree(node.start),
                    stop=self._convert_tree(node.stop),
                    step=self._convert_tree(node.step) if node.step else None,
                )
            
            elif isinstance(node, Tree.FunctionDefinition):
                func_body = self._body_list_to_ast(node.body)

                ret_var = [ast.arg(arg=self._convert_tree(param).id) for param in node.output_params]
                if len(ret_var) == 1:
                    func_body.append(ast.Return(value=ret_var[0]))
                elif len(ret_var) > 1:
                    func_body.append(ast.Return(value=ast.Tuple(elts=ret_var)))
                
                return ast.FunctionDef(
                    name=node.name.value.val,
                    args=ast.arguments(
                        posonlyargs=[],
                        args=[ast.arg(arg=self._convert_tree(param).id) for param in node.input_params],
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
                for var in node.identifiers:
                    assert isinstance(var, Tree.Identifier), "In valid global variable"
                    global_var.append(var.value.val)
                return ast.Global(names=global_var)
            
            elif isinstance(node, Tree.PersistentStatement):
                raise NotImplementedConversionError("persistent", node)
                return ast.Break()
            
            elif isinstance(node, Tree.BreakStatement):
                return ast.Break()
            
            elif isinstance(node, Tree.ContinueStatement):
                return ast.Continue()
            
            elif isinstance(node, Tree.ReturnStatement):
                return ast.Return(value=None)  # MATLAB's 'return' doesn't specify a value
            
            elif isinstance(node, Tree.Assignment):
                targets = [self._convert_tree(lval, ast.Store()) for lval in node.lvalue]
                value = self._convert_tree(node.rvalue)
                for target in targets:
                    self._symbol_table.add_symbol(target, value)
            
                # lineno = node.lvalue[-1].value.ln + 1
                lineno = 1
                return ast.Assign(
                    targets=targets,
                    value=value,
                    lineno=lineno
                )
            
            elif isinstance(node, Tree.FunctionCall):
                if node.arguments is not None:
                    arguments = [self._convert_tree(arg) for arg in node.arguments.indices if arg is not None]
                else:
                    arguments = None
                
                return self.config.converter.convert_func(
                    self._convert_tree(node.identifier),
                    arguments
                )
            
            elif isinstance(node, Tree.ArrayAccess):
                return self.config.converter.access_mat(
                    self._convert_tree(node.identifier),
                    [self._convert_tree(index) for index in node.arguments.indices],
                )
            
            elif isinstance(node, Tree.CellArrayAccess):
                return self.config.converter.access_cell(
                    self._convert_tree(node.identifier),
                    [self._convert_tree(index) for index in node.arguments.indices],
                )
            
            elif isinstance(node, Tree.StructAccess):
                return self.config.converter.access_struct(
                    self._convert_tree(node.identifier),
                    [self._convert_tree(arg) for arg in node.arguments]
                )
            
            
            elif isinstance(node, Tree.BinaryOperation):
                op = self._binop_map.get(node.operator, None)
                
                if op is not None:
                    if isinstance(op, (ast.And, ast.Or,)):
                        return ast.BoolOp(
                            op=op,
                            values=[self._convert_tree(node.left), self._convert_tree(node.right)]
                        )
                    
                    elif isinstance(op, (ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.Eq, ast.NotEq)):
                        return ast.Compare(
                            left=self._convert_tree(node.left),
                            ops=[op],
                            comparators=[self._convert_tree(node.right)]
                        )

                    else:
                        return ast.BinOp(
                            left=self._convert_tree(node.left),
                            op=op,
                            right=self._convert_tree(node.right)
                        )
                else:
                    convert_func = getattr(self.config.converter, node.operator)
                    return convert_func(self._convert_tree(node.left), self._convert_tree(node.right))
            
            elif isinstance(node, Tree.UnaryOperation):
                op = self._binop_map.get(node.operator, None)
                if op is not None:
                    return ast.UnaryOp(
                        op=op,
                        operand=self._convert_tree(node.operand)
                    )
                else:
                    convert_func = getattr(self.config.converter, node.operator)
                    return convert_func(self._convert_tree(node.operand))
            
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


