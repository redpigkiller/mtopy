from typing import *

from parse_matlab_code import Parser, Tree


class Symbol:
    def __init__(self, name :str, node_type: Type[Tree.Node]):
        self.name = name
        self.node_type = node_type

class SymbolTable:
    def __init__(self) -> None:
        # Start with global scope
        self.scopes = [{}]

    def enter_scope(self) -> None:
        self.scopes.append({})

    def exit_scope(self) -> None:
        self.scopes.pop()

    def add_symbol(self, name: str, node_type: Type[Tree.Node]) -> None:
        self.scopes[-1][name] = Symbol(name, node_type)

    def lookup(self, name: str) -> Optional[Symbol]:
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
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