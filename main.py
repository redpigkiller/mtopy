import ast
import astor
from rich import print as rprint

from parse_matlab_code import Parser, Tree
from mtopy.symbol_table import semantic_analysis

s = """
a = 2;
b()
function x()
    b + 3
    b()
    a()
    return a
end
"""


# rprint(ast.dump(ast.parse(s)))
parser = Parser()
ast_tree = parser.parse(s)
rprint(ast_tree)
semantic_analysis(ast_tree)
rprint(ast_tree)

exit(0)

# Step 1: Create the function definition
function_def = ast.FunctionDef(
    name='hello',  # Function name
    args=ast.arguments(
        posonlyargs=[], args=['a'], kwonlyargs=[], kw_defaults=['j'], defaults=['6']
    ),  # No arguments
    body=[ast.Expr(
        value=ast.Call(
            func=ast.Name(id='print', ctx=ast.Load()),  # Call the print function
            args=[ast.Constant(value='Hello, World!')],  # with 'Hello, World!' as the argument
            keywords=[]
        )
    )],  # Body of the function (print statement)
    decorator_list=[]
)

# Step 2: Create the module node and assign the function as its body
module = ast.Module(body=[function_def], type_ignores=[])

# Step 3: Compile the AST into a Python code object
# compiled_code = compile(module, filename="<ast>", mode="exec")
print(astor.to_source(module))
# # Step 4: Execute the compiled code
# exec(compiled_code)

# # Now you can call the function
# hello()  # Output: Hello, World!

