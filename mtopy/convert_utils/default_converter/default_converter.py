from abc import ABC, ABCMeta, abstractmethod
import ast
from typing import *

from ..converter import MatlabTypeConverter
from .matlab_fundamentals import MatlabFundamentals


class IndexTransformer(ast.NodeTransformer):
    def visit_Name(self, node):
        if node.id == "end":
            return ast.Constant(value=0)
        else:
            return node

class DefaultConverter(MatlabTypeConverter, MatlabFundamentals):
    _op_map = {
        'or': ast.Or(),
        'and': ast.And(),
        'bitor': ast.BitOr(),
        'bitand': ast.BitAnd(),
        'lt': ast.Lt(),
        'le': ast.LtE(),
        'gt': ast.Gt(),
        'ge': ast.GtE(),
        'eq': ast.Eq(),
        'ne': ast.NotEq(),
        'plus': ast.Add(),
        'minus': ast.Sub(),
        'uplus': ast.UAdd(),
        'uminus': ast.USub(),
        'not': ast.Not(),
        }
    
    def __init__(self) -> None:
        super().__init__()
        self._index_transformer = IndexTransformer()
    
    def import_module(self) -> list[ast.AST]:
        
        return [ast.Import(names=[ast.alias(name='numpy', asname='np')])]
    
    def create_mat(self, elements: list[list[ast.AST]]) -> ast.AST:
        return ast.Call(
            func=ast.Attribute(value=ast.Name(id='np', ctx=ast.Load()), attr='array', ctx=ast.Load()),
            args=[ast.List(elts=[ast.List(elts=row, ctx=ast.Load()) for row in elements], ctx=ast.Load())],
            keywords=[]
        )
    
    def create_cell(self, elements: list[list[ast.AST]]) -> ast.AST:
        return ast.List(elts=[ast.List(elts=row, ctx=ast.Load()) for row in elements], ctx=ast.Load())
    
    def create_struct(self, elements: list[list[ast.AST]]) -> ast.AST:
        return None
    
    def _index_mapping(self, indexes: list[ast.AST]) -> list[ast.AST]:
        args = []
        for index in indexes:
            # Change 'end' to 0
            index = self._index_transformer.visit(index)

            # Get the index
            if not isinstance(index, ast.Slice):
                index = ast.BinOp(
                    left=index,
                    op=ast.Sub(),
                    right=ast.Constant(value=1)
                )
                
            args.append(index)
        
        return args

    def access_mat(self, identifier: ast.AST, arguments: list[ast.AST]) -> ast.AST:
        args = self._index_mapping(arguments)

        if len(args) == 1:
            args = args[0]
        elif len(args) > 1:
            args = ast.Tuple(elts=args)

        return ast.Subscript(value=identifier, slice=args)
    
    def access_cell(self, identifier: ast.AST, arguments: list[ast.AST]) -> ast.AST:
        args = self._index_mapping(arguments)

        if len(args) == 1:
            args = args[0]
        elif len(args) > 1:
            args = ast.Tuple(elts=args)

        return ast.Subscript(value=identifier, slice=args)
    
    def access_struct(self, identifier: ast.AST, arguments: list[ast.AST]) -> ast.AST:
        struct_element = identifier
        for arg in arguments:
            if isinstance(arg, ast.Name):
                arg = ast.Constant(value=arg.id)
            struct_element = ast.Subscript(value=struct_element, slice=arg, ctx=ast.Load())
        return struct_element
    
    def arange(self, start: ast.AST, stop: list[ast.AST], step: Optional[list[ast.AST]]=None) -> ast.AST:
        func_args = [start, stop]
        if step is not None:
            func_args.append(step)
        else:
            step = ast.Constant(value=1)
        func_args[1] = ast.BinOp(left=stop, op=ast.Add(), right=step)

        return ast.Call(
            func=ast.Attribute(value=ast.Name(id='np', ctx=ast.Load()), attr='arange', ctx=ast.Load()),
            args=func_args,
            keywords=[]
        )
    
    def convert_op(self, node: ast.AST) -> ast.AST:
        op = self._op_map.get(node.func.id, None)
        if op is not None:
            if isinstance(op, (ast.And, ast.Or)):
                return ast.BoolOp(
                    op=op,
                    values=node.args
                )
            
            elif isinstance(op, (ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.Eq, ast.NotEq)):
                return ast.Compare(
                    left=node.args[0],
                    ops=[op],
                    comparators=node.args[1:]
                )

            elif isinstance(op, (ast.UAdd, ast.USub, ast.Not)):
                return ast.UnaryOp(
                    op=op,
                    operand=node.args[0]
                )
            
            else:
                return ast.BinOp(
                    left=node.args[0],
                    op=op,
                    right=node.args[1]
                )
        
        match node.func.id:
            case "times":
                return self._multiplication(node.args[0], node.args[1])
            case "rdivide":
                return self._division(node.args[0], node.args[1])
            case "ldivide":
                return self._division(node.args[1], node.args[0])
            case "mtimes":
                return self._matrix_multiplication(node.args[0], node.args[1])
            case "mrdivide":
                return self._least_square(self._transpose(node.args[0]), self._transpose(node.args[1]))
            case "mldivide":
                return self._least_square(node.args[0], node.args[1])
            case "power":
                return self._power(node.args[0], node.args[1])
            case "mpower":
                return self._matrix_power(node.args[0], node.args[1])
            case "transpose":
                return self._transpose(node.args[0])
            case "ctranspose":
                return self._hermitian(node.args[0])
            
        return node
    
    def convert_call(self, node: ast.AST) -> ast.AST|str:
        # Convert the built-in functions
        convert_func = getattr(self, node.func.id, None)
        if convert_func:
            return convert_func(node.args)

        return f"Undefined function {node.func.id}"
    
    # ################################################################################
    # Basic operations
    # ################################################################################
    def _multiplication(self, left: ast.AST, right: ast.AST) -> ast.AST:
        return ast.BinOp(left=left, op=ast.Mult(), right=right)

    def _division(self, left: ast.AST, right: ast.AST) -> ast.AST:
        return ast.BinOp(left=left, op=ast.Div(), right=right)
    
    def _matrix_multiplication(self, left: ast.AST, right: ast.AST) -> ast.AST:
        return ast.BinOp(left=left, op=ast.MatMult(), right=right)
    
    def _least_square(self, left: ast.AST, right: ast.AST) -> ast.AST:
        return ast.Call(
            func=ast.Attribute(
                value=ast.Attribute(
                    value=ast.Name(id='np', ctx=ast.Load()),
                    attr='linalg',
                    ctx=ast.Load()
                ),
                attr='lstsq',
                ctx=ast.Load()
            ),
            args=[left, right],
            keywords=[]
        )
    
    def _power(self, left: ast.AST, right: ast.AST) -> ast.AST:
        return ast.BinOp(left=left, op=ast.Pow(), right=right)
    
    def _matrix_power(self, left: ast.AST, right: ast.AST) -> ast.AST:
        return ast.Call(
            func=ast.Attribute(
                value=ast.Attribute(
                    value=ast.Name(id='np', ctx=ast.Load()),
                    attr='linalg',
                    ctx=ast.Load()
                ),
                attr='matrix_power',
                ctx=ast.Load()
            ),
            args=[left, right],
            keywords=[]
        )
    
    def _transpose(self, left: ast.AST) -> ast.AST:
        return ast.Attribute(value=left, attr='T', ctx=ast.Load())
    
    def _hermitian(self, left: ast.AST) -> ast.AST:
        return ast.Attribute(
            value=ast.Call(
                func=ast.Attribute(
                    value=left,
                    ctx=ast.Load(),
                    attr='conj'
                ),
                args=[],
                keywords=[]
            ),
            attr='T',
            ctx=ast.Load()
        )
    
    # ################################################################################
    # Matlab built-in functions
    # ref: https://www.mathworks.com/help/matlab/referencelist.html?type=function&s_tid=CRUX_topnav
    # ################################################################################
    def _construct_attribute_call_ast(self, attrs: list[str], args: list[ast.AST]) -> ast.AST:
        if not attrs:
            raise ValueError("At least one attribute must be provided")
        
        node = ast.Name(id=attrs[0], ctx=ast.Load())
        for attr in attrs[1:]:
            node = ast.Attribute(value=node, attr=attr, ctx=ast.Load())
        
        return ast.Call(func=node, args=args, keywords=[])
    
    def struct(self, args: list[ast.AST]) -> ast.AST:
        return ast.Dict(keys=[], values=[])
