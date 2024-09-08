import ast
import astor
from rich import print as rprint

from parse_matlab_code import Parser, Tree
from mtopy.symbol_table import semantic_analysis

# Main execution
if __name__ == "__main__":
    parser = Parser()
    matlab_code = r"""
a.\b
    """

    # with open("test_data/simple.m", 'r') as f:
    #     matlab_code = f.read()
    matlab_ast = parser.parse(matlab_code)

    rprint((matlab_ast))
    
    from mtopy.convert_utils.default_converter import DefaultConverter
    from mtopy.mtree_to_pytree import MPTreeConverter, MPTreeConversionConfig

    conversion_config = MPTreeConversionConfig(DefaultConverter)
    
    converter = MPTreeConverter(conversion_config)
    try:
        python_ast = converter.convert_tree(matlab_ast)
    except Exception as e:
        rprint(e)
        exit(0)

    from mtopy.utils import compare_ast

    # true_ast = ast.parse(matlab_code)
    # res = compare_ast(python_ast, true_ast)
    # print(res)


    rprint(ast.dump(python_ast))
    # rprint(ast.dump(true_ast))
    rprint(ast.unparse(python_ast))
    exit(0)
    for file_path in Path("test_data").rglob("*.m"):
        with open(file_path, 'r') as f:
            matlab_code = f.read()
        matlab_ast = parser.parse(matlab_code)
        rprint(matlab_ast)
        python_ast = convert_tree(matlab_ast)
        rprint(ast.dump(python_ast))
        rprint(astor.to_source(python_ast))



exit(0)

s = """
np.arange(2, 1, 3+3)
"""

rprint(ast.dump(ast.parse(s)))
rprint(astor.to_source(ast.parse(s)))
rprint(ast.unparse(ast.parse(s)))

# Module(body=[Expr(value=If(test=Compare(left=Name(id='x', ctx=Load()), ops=[Eq()], comparators=[Constant(value=2.0)]), body=[Pass()],
# orelse=If(test=Compare(left=Name(id='x', ctx=Load()), ops=[Eq()], comparators=[Constant(value=2.0)]), body=[Pass()],
# orelse=If(test=Compare(left=Name(id='x', ctx=Load()), ops=[Eq()], comparators=[Constant(value=2.0)]), body=[Pass()],
# orelse=If(test=Compare(left=Name(id='x', ctx=Load()), ops=[Eq()], comparators=[Constant(value=2.0)]), body=[Pass()], orelse=[Pass()])))))],     
# type_ignores=[])
# parser = Parser()
# ast_tree = parser.parse(s)
# rprint(ast_tree)
# semantic_analysis(ast_tree)
# rprint(ast_tree)

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

