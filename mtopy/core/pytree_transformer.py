
import ast
from typing import *

from mtopy.convert_utils.converter import MatlabTypeConverter
from .function_table import FunctionTable

class MPTreeTransformer(ast.NodeTransformer):
    def __init__(self, converter: MatlabTypeConverter=None, function_table: FunctionTable=None) -> None:
        super().__init__()
        self._converter = converter
        self._function_table = function_table
        self._function_path = []

    def visit_List(self, node: ast.AST) -> ast.AST:
        # Colon array
        if any(not isinstance(n, ast.List) for n in node.elts):
            return self._converter.arange(node.elts[0], node.elts[1], node.elts[2] if len(node.elts) >=3 else None)

        # Array
        if len(node.elts) != 1:
            return self._converter.create_mat([[element for element in row.elts] for row in node.elts])
        
        # Array or cell array
        if any(not isinstance(n, ast.List) for n in node.elts[0].elts):
            return self._converter.create_mat([[element for element in row.elts] for row in node.elts])

        # Cell array
        if node.elts[0].elts:
            return self._converter.create_cell([[element for element in row.elts] for row in node.elts[0].elts])
        else:
            return ast.Constant(value=None)

    def visit_Tuple(self, node: ast.AST) -> ast.AST:
        # Struct access
        if any(not isinstance(n, ast.Tuple) for n in node.elts):
            return self._converter.access_struct(node.elts[0], [arg for arg in node.elts[1:]])

        # Array access
        if any(not isinstance(n, ast.Tuple) for n in node.elts[0].elts):
            return self._converter.access_mat(node.elts[0].elts[0], [arg for arg in node.elts[0].elts[1:]])
        
        # Cell array access
        if any(not isinstance(n, ast.List) for n in node.elts[0].elts[0].elts):
            return self._converter.access_cell(node.elts[0].elts[0].elts[0], [arg for arg in node.elts[0].elts[0].elts[1:]])

        return node
    
    def visit_FunctionDef(self, node: ast.AST) -> ast.AST:
        self._function_table.enter_scope(node.name)
        self.generic_visit(node)
        self._function_table.exit_scope()

        return node

    def visit_Call(self, node: ast.AST) -> ast.AST:
        if self._function_table.lookup(ast.unparse(node.func)):
            return node
        
        if isinstance(node.func, ast.Name):
            converted_node = self._converter.convert_call(node)
            if converted_node is not None:
                return converted_node
        
        return self._converter.access_mat(node.func, node.args)
        