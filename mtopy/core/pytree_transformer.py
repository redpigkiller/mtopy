
import ast
from typing import *

from ..convert_utils.converter import MatlabTypeConverter
from .function_table import FunctionTable

class MPTreeTransformer(ast.NodeTransformer):
    def __init__(self, converter: MatlabTypeConverter=None, function_table: FunctionTable=None) -> None:
        super().__init__()
        self._converter = converter
        self._function_table = function_table
        self._function_path = []

        self._lst_tup_lock = False

    def visit_Module(self, node: ast.AST) -> ast.AST:
        # Add import module
        node.body = self._converter.import_module() + node.body

        self.generic_visit(node)

        return node

    def visit_List(self, node: ast.AST) -> ast.AST:
        if self._lst_tup_lock:
            self.generic_visit(node)
            return node
        
        # Colon array
        if any(not isinstance(n, ast.List) for n in node.elts):
            node = self._converter.arange(node.elts[0], node.elts[1], node.elts[2] if len(node.elts) >=3 else None)

        # Array
        elif len(node.elts) != 1:
            node = self._converter.create_mat([[element for element in row.elts] for row in node.elts])
        
        # Array or cell array
        elif any(not isinstance(n, ast.List) for n in node.elts[0].elts):
            node = self._converter.create_mat([[element for element in row.elts] for row in node.elts])

        # Cell array
        elif node.elts[0].elts:
            node = self._converter.create_cell([[element for element in row.elts] for row in node.elts[0].elts])

        else:
            node = ast.Constant(value=None)

        self._lst_tup_lock = True
        self.generic_visit(node)
        self._lst_tup_lock = False

        return node

    def visit_Tuple(self, node: ast.AST) -> ast.AST:
        if self._lst_tup_lock:
            self.generic_visit(node)
            return node

        # Struct access
        if any(not isinstance(n, ast.Tuple) for n in node.elts):
            node = self._converter.access_struct(node.elts[0], [arg for arg in node.elts[1:]])
            
        # Array access
        elif any(not isinstance(n, ast.Tuple) for n in node.elts[0].elts):
            node = self._converter.access_mat(node.elts[0].elts[0], [arg for arg in node.elts[0].elts[1:]])
        
        # Cell array access
        elif any(not isinstance(n, ast.List) for n in node.elts[0].elts[0].elts):
            node = self._converter.access_cell(node.elts[0].elts[0].elts[0], [arg for arg in node.elts[0].elts[0].elts[1:]])

        self._lst_tup_lock = True
        self.generic_visit(node)
        self._lst_tup_lock = False

        return node
    
    def visit_FunctionDef(self, node: ast.AST) -> ast.AST:
        self._function_table.enter_scope(node.name)

        self.generic_visit(node)
        
        self._function_table.exit_scope()

        return node

    def visit_Call(self, node: ast.AST) -> ast.AST:
        self.generic_visit(node)

        # If it is function, then call it
        if not self._function_table.lookup(ast.unparse(node.func)):
            # Check if it is the function defined in converter
            if isinstance(node.func, ast.Name):
                converted_node = self._converter.convert_call(node)
            else:
                converted_node = None
            
            # If it is not the function defined in converter, regard it as a matrix
            if converted_node is not None:
                node = converted_node
            else:
                node = self._converter.access_mat(node.func, node.args)

        return node
        