import ast

def construct_attribute_call_ast(attrs: list[str], args: list[ast.AST]) -> ast.AST:
        """Helper method to construct AST nodes for function calls"""
        if not attrs:
            raise ValueError("At least one attribute must be provided")
        
        node = ast.Name(id=attrs[0], ctx=ast.Load())
        for attr in attrs[1:]:
            node = ast.Attribute(value=node, attr=attr, ctx=ast.Load())
        
        return ast.Call(func=node, args=args, keywords=[])