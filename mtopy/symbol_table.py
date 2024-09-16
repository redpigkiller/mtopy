from typing import *
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from functools import reduce
import operator
import ast

from parse_matlab_code import Parser, Tree

class SymbolType(Enum):
    VAR = auto()
    IF = auto()
    TRY = auto()
    LOOP = auto()
    FUNC = auto()



@dataclass
class Symbol:
    name: list[str]
    typ: SymbolType


def get_dict_by_path(root, items):
    """Access a nested object in root by item sequence."""
    return reduce(operator.getitem, items, root)

class SymbolTable:
    def __init__(self, cwd: Optional[str]=None) -> None:
        self._addpath_scope = {}
        self._cwd_scope = {}
        
        self._mfile_scope = {}
        self._mfile_scope_path = []

        if cwd is not None:
            self._cwd = Path(cwd)
            for f in self._cwd.glob("*.m"):
                self._cwd_scope[f.name] = f.absolute()

    def cd(self, cd_cmd: str) -> None:
        self._cwd = self._cwd / Path(cd_cmd)
        self._cwd_scope = {}
        for f in self._cwd.glob("*.m"):
            self._cwd_scope[f.name] = f.absolute()

    def add_path(self, path: str) -> None:
        for f in (self._cwd / Path(path)).rglob("*.m"):
            self._func_file_scope[f.name] = f.absolute()

    def enter_scope(self, func_name: str) -> None:
        target_dict = get_dict_by_path(self._mfile_scope, self._mfile_scope_path)
        target_dict[func_name] = {}
        self._mfile_scope_path.append(func_name)

    def exit_scope(self) -> None:
        self._mfile_scope_path.pop()

    def add_symbol(self, target_node: ast.AST, value_node: ast.AST) -> None:
        target_dict = get_dict_by_path(self._mfile_scope, self._mfile_scope_path)
        target_dict[target_node] = value_node

    def lookup(self, name: str) -> Optional[Symbol]:
        for i in range(len(self._mfile_scope_path)):
            scope_path = self._mfile_scope_path[:len(self._mfile_scope_path)-i]
            target_dict = get_dict_by_path(self._mfile_scope, scope_path)
            if name in target_dict:
                return target_dict[name]

        if name in self._mfile_scope_path:
            return self._mfile_scope_path[name]

        return None

class SemanticError(Exception):
    pass

def semantic_analysis(ast_root: Tree.Node) -> tuple[Tree.Node, list[str]]:
    symbol_table = SymbolTable()
    error_msg = []

    def analyze_node(node: Tree.Node, context: str="global") -> Tree.Node:
        try:
            if isinstance(node, Tree.Assignment):
                for lnode in node.lvalue:
                    if isinstance(lnode, Tree.Identifier):
                        symbol_table.add_symbol(lnode.value.val, Tree.Identifier)
                    elif isinstance(lnode, Tree.FunctionCall):
                        symbol_table.add_symbol(lnode.identifier.value.val, Tree.Identifier)
                node.rvalue = analyze_node(node.rvalue, context)

            elif isinstance(node, Tree.FunctionDefinition):
                # if context != "global":
                #     raise SemanticError(f"Nested function definitions are not allowed in MATLAB: {node.name.value.val}")
                symbol_table.add_symbol(node.name.value.val, Tree.FunctionDefinition)
                symbol_table.enter_scope()
                for in_node in node.input_params:
                    symbol_table.add_symbol(in_node.value.val, Tree.Identifier)
                for out_node in node.output_params:
                    symbol_table.add_symbol(out_node.value.val, Tree.Identifier)
                node.body = [analyze_node(child, "function") for child in node.body]
                symbol_table.exit_scope()

            elif isinstance(node, (Tree.ForLoop, Tree.ParforLoop)):
                symbol_table.add_symbol(node.identifier.value.val, Tree.Identifier)
                node.expression = analyze_node(node.expression, context)
                symbol_table.enter_scope()
                node.body = [analyze_node(child, "loop") for child in node.body]
                symbol_table.exit_scope()

            elif isinstance(node, Tree.WhileLoop):
                node.condition = analyze_node(node.condition, context)
                symbol_table.enter_scope()
                node.body = [analyze_node(child, "loop") for child in node.body]
                symbol_table.exit_scope()

            elif isinstance(node, Tree.IfStatement):
                node.condition = analyze_node(node.condition, context)
                symbol_table.enter_scope()
                node.then_body = [analyze_node(child, context) for child in node.then_body]
                symbol_table.exit_scope()
                for clause in node.elseif_clauses:
                    clause.condition = analyze_node(clause.condition, context)
                    symbol_table.enter_scope()
                    clause.body = [analyze_node(child, context) for child in clause.body]
                    symbol_table.exit_scope()
                if node.else_body:
                    symbol_table.enter_scope()
                    node.else_body = [analyze_node(child, context) for child in node.else_body]
                    symbol_table.exit_scope()

            elif isinstance(node, Tree.GlobalStatement):
                for id_node in node.identifiers:
                    symbol_table.add_symbol(id_node.value.val, Tree.Identifier)

            elif isinstance(node, Tree.PersistentStatement):
                for id_node in node.identifiers:
                    symbol_table.add_symbol(id_node.value.val, Tree.Identifier)

            elif isinstance(node, Tree.FunctionCall):
                symbol = symbol_table.lookup(node.identifier.value.val)
                if symbol and symbol.node_type == Tree.Identifier:
                    return Tree.ArrayAccess(
                        identifier=node.identifier,
                        arguments=[analyze_node(arg, context) for arg in node.arguments]
                    )
                node.arguments = [analyze_node(arg, context) for arg in node.arguments]

            elif isinstance(node, Tree.BinaryOperation):
                node.left = analyze_node(node.left, context)
                node.right = analyze_node(node.right, context)

            elif isinstance(node, Tree.UnaryOperation):
                node.operand = analyze_node(node.operand, context)

            elif isinstance(node, Tree.MatrixExpression):
                node.elements = [[analyze_node(elem, context) for elem in row] for row in node.elements]

            elif isinstance(node, Tree.CellArrayExpression):
                node.elements = [[analyze_node(elem, context) for elem in row] for row in node.elements]

            elif isinstance(node, Tree.AnonymousFunction):
                symbol_table.enter_scope()
                for param in node.parameters:
                    symbol_table.add_symbol(param.value.val, Tree.Identifier)
                node.body = analyze_node(node.body, "anonymous_function")
                symbol_table.exit_scope()

        except SemanticError as e:
            error_msg.append(str(e))

        return node
    
    ast_root.body = [analyze_node(node) for node in ast_root.body]
    return ast_root, error_msg