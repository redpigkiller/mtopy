
import ast
from typing import *

from ..convert_utils.converter import MatlabTypeConverter
from .symbol_table import SymbolTable, SymbolType

class MPTreeTransformer(ast.NodeTransformer):
    def __init__(self, converter: MatlabTypeConverter=None, function_table: SymbolTable=None) -> None:
        super().__init__()
        self._converter = converter
        if function_table is None:
            self._function_table = SymbolTable()
        else:
            self._function_table = function_table

        self._ignore_func_name = None

    def visit_Module(self, node: ast.AST) -> ast.AST:
        # Add import module
        node.body = self._converter.import_module() + node.body

        self.generic_visit(node)

        return node
    
    def visit_Name(self, node: ast.AST) -> ast.AST:
        if self._ignore_func_name is not None and node.id == self._ignore_func_name:
            return node
        else:
            pseudo_func_node = ast.Call(func=node, args=[], keywords=[])
            pseudo_func_node = self._converter.convert_call(pseudo_func_node)
            if not isinstance(pseudo_func_node, str):
                return pseudo_func_node
            else:
                return node

    def visit_FunctionDef(self, node: ast.AST) -> ast.AST:
        self._function_table.enter_scope(node.name)

        self.generic_visit(node)
        
        self._function_table.exit_scope()

        return node

    def visit_Call(self, node: ast.AST) -> ast.AST:
        if isinstance(node.func, ast.Name):
            self._ignore_func_name = node.func.id
        self.generic_visit(node)
        self._ignore_func_name = None

        # Check if it is matlab datatype
        if isinstance(node.func, ast.Name) and getattr(node, '_custom_flag', 'None') == "matlab_array":
            node = self._converter.create_mat([[element for element in row.elts] for row in node.args[0].elts])
        
        elif isinstance(node.func, ast.Name) and getattr(node, '_custom_flag', 'None') == "matlab_cell":
            node = self._converter.create_cell([[element for element in row.elts] for row in node.args[0].elts])
        
        elif isinstance(node.func, ast.Name) and getattr(node, '_custom_flag', 'None') == "matlab_arange":
            node = self._converter.arange(node.args[0].elts[0], node.args[0].elts[1], node.args[0].elts[2] if len(node.args[0].elts) >=3 else None)
        
        elif isinstance(node.func, ast.Name) and getattr(node, '_custom_flag', 'None') == "matlab_array_access":
            node = self._converter.access_mat(node.args[0], node.args[1].elts)
            
        elif isinstance(node.func, ast.Name) and getattr(node, '_custom_flag', 'None') == "matlab_cell_access":
            node = self._converter.access_cell(node.args[0], node.args[1].elts)
            
        elif isinstance(node.func, ast.Name) and getattr(node, '_custom_flag', 'None') == "matlab_struct_access":
            node = self._converter.access_struct(node.args[0], node.args[1].elts)
            
        elif isinstance(node.func, ast.Name) and getattr(node, '_custom_flag', 'None') == "matlab_op":
            node = self._converter.convert_op(node)

        else:
            typ = self._function_table.lookup(ast.unparse(node.func))

            if typ is SymbolType.VAR:
                # Regard it as a matrix
                node = self._converter.access_mat(node.func, node.args)

            elif typ is SymbolType.UNK:
                # Check if it is a function
                converted_node = "None"

                # 1. Try to use the function converter defined in converter
                if isinstance(node.func, ast.Name):
                    converted_node = self._converter.convert_call(node)
                
                # 2. If the function is not defined in converter, check if there are arguments
                if isinstance(converted_node, str):
                    if len(node.args) != 0:
                        # Regard it as a matrix, if there are arguments, i.e., x() is regarded as function call
                        node = self._converter.access_mat(node.func, node.args)
                else:
                    node = converted_node
            # Note if typ is SymbolType.FUNC, then we don't need to convert it

        return node
        