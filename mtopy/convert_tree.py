import ast
import astor
from typing import *
from rich import print as rprint

from parse_matlab_code import Parser, Tree

def convert_tree(node: Tree.Node) -> Optional[ast.AST]:
    # Terminal symbols
    if isinstance(node, Tree.Number):
        return ast.Constant(value=float(node.value.val))
    elif isinstance(node, Tree.ImagNumber):
        return ast.Constant(value=complex(0, float(node.value.val[:-1])))
    elif isinstance(node, Tree.String):
        return ast.Constant(value=str(node.value.val))
    elif isinstance(node, Tree.Identifier):
        return ast.Name(id=str(node.value.val), ctx=ast.Load())
    elif isinstance(node, Tree.Ignore):
        return ast.Name(id='_', ctx=ast.Load())
    elif isinstance(node, (Tree.WhiteSpace, Tree.COLON, Tree.Comment, Tree.Ellipsis, Tree.EndOfLine)):
        return None
    
    # Complex structures
    if isinstance(node, Tree.Program):


        return ast.Module(body=[convert_tree(x) for x in node.body if convert_tree(x) is not None], type_ignores=[])
    
    elif isinstance(node, Tree.FunctionDefinition):
        func_body = [convert_tree(stmt) for stmt in node.body if convert_tree(stmt) is not None]

        ret_val = [ast.arg(arg=convert_tree(param).id) for param in node.output_params]
        if len(ret_val) == 1:
            func_body.append(ast.Return(value=ret_val[0]))
        elif len(ret_val) > 1:
            func_body.append(ast.Return(value=ast.Tuple(elts=ret_val)))
        
        return ast.FunctionDef(
            name=node.name.value.val,
            args=ast.arguments(
                posonlyargs=[],
                args=[ast.arg(arg=convert_tree(param).id) for param in node.input_params],
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[]
            ),
            body=func_body,
            decorator_list=[]
        )
    
    elif isinstance(node, Tree.AnonymousFunction):
        return ast.Lambda(
            args=ast.arguments(
                posonlyargs=[],
                args=[ast.arg(arg=convert_tree(param).id) for param in node.parameters],
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[]
            ),
            body=convert_tree(node.body[0])  # Assuming single expression for lambda body
        )
    
    elif isinstance(node, Tree.IfStatement):
        return ast.If(
            test=convert_tree(node.condition),
            body=[convert_tree(stmt) for stmt in node.then_body if convert_tree(stmt) is not None],
            orelse=convert_elseif_chain(node.elseif_clauses, node.else_body)
        )
    
    elif isinstance(node, Tree.ForLoop):
        return ast.For(
            target=convert_tree(node.identifier),
            iter=convert_tree(node.expression),
            body=[convert_tree(stmt) for stmt in node.body if convert_tree(stmt) is not None],
            orelse=[]
        )
    
    elif isinstance(node, Tree.WhileLoop):
        return ast.While(
            test=convert_tree(node.condition),
            body=[convert_tree(stmt) for stmt in node.body if convert_tree(stmt) is not None],
            orelse=[]
        )
    
    elif isinstance(node, Tree.SwitchStatement):
        return convert_switch_to_if(node)
    
    elif isinstance(node, Tree.TryCatchStatement):
        return ast.Try(
            body=[convert_tree(stmt) for stmt in node.try_body if convert_tree(stmt) is not None],
            handlers=[ast.ExceptHandler(
                type=convert_tree(node.exception),
                name=None,
                body=[convert_tree(stmt) for stmt in node.catch_body if convert_tree(stmt) is not None]
            )],
            orelse=[],
            finalbody=[]
        )
    
    elif isinstance(node, Tree.BreakStatement):
        return ast.Break()
    
    elif isinstance(node, Tree.ContinueStatement):
        return ast.Continue()
    
    elif isinstance(node, Tree.ReturnStatement):
        return ast.Return(value=None)  # MATLAB's 'return' doesn't specify a value
    
    elif isinstance(node, Tree.Assignment):
        return ast.Assign(
            targets=[convert_tree(lval) for lval in node.lvalue],
            value=convert_tree(node.rvalue)
        )
    
    elif isinstance(node, Tree.FunctionCall):
        return ast.Call(
            func=convert_tree(node.identifier),
            args=[convert_tree(arg) for arg in node.arguments],
            keywords=[]
        )
    
    elif isinstance(node, Tree.BinaryOperation):
        return ast.BinOp(
            left=convert_tree(node.left),
            op=convert_operator(node.operator),
            right=convert_tree(node.right)
        )
    
    elif isinstance(node, Tree.UnaryOperation):
        return ast.UnaryOp(
            op=convert_operator(node.operator),
            operand=convert_tree(node.operand)
        )
    
    # Add more node type conversions as needed
    
    raise NotImplementedError(f"Conversion not implemented for node type: {type(node)}")

def convert_elseif_chain(elseif_clauses: list[Tree.ElseIfClause], else_body: Optional[list[Tree.Node]]) -> list[ast.AST]:
    if not elseif_clauses and not else_body:
        return []
    
    if not elseif_clauses:
        return [convert_tree(stmt) for stmt in else_body if convert_tree(stmt) is not None]
    
    next_clause = elseif_clauses[0]
    return [ast.If(
        test=convert_tree(next_clause.condition),
        body=[convert_tree(stmt) for stmt in next_clause.body if convert_tree(stmt) is not None],
        orelse=convert_elseif_chain(elseif_clauses[1:], else_body)
    )]

def convert_switch_to_if(node: Tree.SwitchStatement) -> ast.If:
    if not node.cases:
        return ast.Pass()
    
    first_case = node.cases[0]
    return ast.If(
        test=ast.Compare(
            left=convert_tree(node.expression),
            ops=[ast.Eq()],
            comparators=[convert_tree(first_case.condition)]
        ),
        body=[convert_tree(stmt) for stmt in first_case.body if convert_tree(stmt) is not None],
        orelse=convert_switch_to_if(Tree.SwitchStatement(
            expression=node.expression,
            cases=node.cases[1:],
            otherwise=node.otherwise
        )) if len(node.cases) > 1 or node.otherwise else [ast.Pass()]
    )

def convert_operator(op: str) -> ast.operator:
    operator_map = {
        'addition': ast.Add(),
        'subtraction': ast.Sub(),
        'multiplication': ast.Mult(),
        'matrix_multiplication': ast.Mult(),
        '/': ast.Div(),
        'power': ast.Pow(),
        'matrix_power': ast.Pow(),
        'equal_to': ast.Eq(),
        'not_equal_to': ast.NotEq(),
        'less_than': ast.Lt(),
        'less_than_or_equal_to': ast.LtE(),
        'greater_than': ast.Gt(),
        'greater_than_or_equal_to': ast.GtE(),
        '&': ast.BitAnd(),
        '|': ast.BitOr(),
        '~': ast.Invert(),
    }
    return operator_map.get(op, ast.Add())  # Default to Add if not found

# Main execution
if __name__ == "__main__":
    parser = Parser()
    matlab_code = """
    function [a, b] = example(x)
        if x > 0
            y = x * 2;
        elseif x < 0
            y = x * -1;
        else
            y = 0;
        end
    end
    """
    matlab_ast = parser.parse(matlab_code)
    rprint(matlab_ast)
    python_ast = convert_tree(matlab_ast)
    rprint(ast.dump(python_ast))
    rprint(astor.to_source(python_ast))