import ast
import astor
from rich import print as rprint
from pathlib import Path

from parse_matlab_code import Parser, Tree, Error
from mtopy.core.function_table import semantic_analysis

from mtopy.convert_utils.default_converter import DefaultConverter
from mtopy.mtree_to_pytree import MPTreeConverter, MPTreeConversionError, NotImplementedConversionError
from mtopy.core.function_table import FunctionTable
from mtopy.pytree_transformer import MPTreeTransformer
# conversion_config = MPTreeConversionConfig(DefaultConverter)

parser = Parser()
cc = DefaultConverter()
ff = FunctionTable("test_data/src")
converter = MPTreeConverter(function_table=ff)
tt = MPTreeTransformer(converter=cc, function_table=converter.get_function_table())

if __name__ == "__main__":

    matlab_code = r"""
[]
[2]
[2 3]
[2 3; 3]
 {"32", "fh";3}
2:4
1:2:3
1:2:3:4
x(2, 3)
x{2}
x.(2)
    """


    matlab_code = r"""
ndim(x)
reshape(x, 2, b, h)

size(a, 8)
function t1()
end
f.b = @(x) x
function t122()
end
"""

    # with open(r"test_data\src\tools\inputsdlg.m", 'r') as f:
    #     matlab_code = f.read()

    matlab_ast = parser.parse(matlab_code)
    # rprint(matlab_ast)

    python_ast = converter.convert(matlab_ast)

    # print(ast.dump(python_ast, include_attributes=False, indent=4))
    # print(ast.unparse(python_ast))

    python_ast = tt.visit(python_ast)
    # print(ast.dump(python_ast, indent=4))
    print(ast.unparse(python_ast))

    exit(0)

    for file_path in Path("test_data").rglob("*.m"):
        with open(file_path, 'r', encoding='utf-8') as f:
            matlab_code = f.read()
        print(f"{file_path}")

        try:
            matlab_ast = parser.parse(matlab_code)
        except Error.NotImplementedFeatureError as e:
            # print(e)
            print("NotImplementedFeatureError")
        except Exception as e:
            # print(e)
            print("5555")
            exit(0)

        try:
            python_ast = converter.convert(matlab_ast)
        except NotImplementedConversionError as e:
            # print(e)
            print("NotImplementedConversionError")
        except Exception as e:
            print(e)
            print("5555")
            exit(0)
            
        python_code = ast.unparse(python_ast)
        # try:
        #     python_code = ast.unparse(python_ast)
        # except Exception as e:
        #     print(e)
        #     print("5555")
        #     exit(0)
        # rprint(ast.unparse(python_ast))

        # rprint((matlab_ast))
    
    # try:
    #     python_ast = converter.convert(matlab_ast)
    #     print(converter._symbol_table._mfile_scope)
    # except Exception as e:
    #     rprint(e)
    #     exit(0)

    # from mtopy.utils import compare_ast

    # true_ast = ast.parse(matlab_code)
    # res = compare_ast(python_ast, true_ast)
    # print(res)


#     rprint(ast.dump(python_ast))
#     # rprint(ast.dump(true_ast))
#     rprint(ast.unparse(python_ast))
#     exit(0)
#     for file_path in Path("test_data").rglob("*.m"):
#         with open(file_path, 'r') as f:
#             matlab_code = f.read()
#         matlab_ast = parser.parse(matlab_code)
#         rprint(matlab_ast)
#         python_ast = convert_tree(matlab_ast)
#         rprint(ast.dump(python_ast))
#         rprint(astor.to_source(python_ast))



# exit(0)

# s = """
# np.arange(2, 1, 3+3)
# """

# rprint(ast.dump(ast.parse(s)))
# rprint(astor.to_source(ast.parse(s)))
# rprint(ast.unparse(ast.parse(s)))

# # Module(body=[Expr(value=If(test=Compare(left=Name(id='x', ctx=Load()), ops=[Eq()], comparators=[Constant(value=2.0)]), body=[Pass()],
# # orelse=If(test=Compare(left=Name(id='x', ctx=Load()), ops=[Eq()], comparators=[Constant(value=2.0)]), body=[Pass()],
# # orelse=If(test=Compare(left=Name(id='x', ctx=Load()), ops=[Eq()], comparators=[Constant(value=2.0)]), body=[Pass()],
# # orelse=If(test=Compare(left=Name(id='x', ctx=Load()), ops=[Eq()], comparators=[Constant(value=2.0)]), body=[Pass()], orelse=[Pass()])))))],     
# # type_ignores=[])
# # parser = Parser()
# # ast_tree = parser.parse(s)
# # rprint(ast_tree)
# # semantic_analysis(ast_tree)
# # rprint(ast_tree)

# # exit(0)

# # Step 1: Create the function definition
# function_def = ast.FunctionDef(
#     name='hello',  # Function name
#     args=ast.arguments(
#         posonlyargs=[], args=['a'], kwonlyargs=[], kw_defaults=['j'], defaults=['6']
#     ),  # No arguments
#     body=[ast.Expr(
#         value=ast.Call(
#             func=ast.Name(id='print', ctx=ast.Load()),  # Call the print function
#             args=[ast.Constant(value='Hello, World!')],  # with 'Hello, World!' as the argument
#             keywords=[]
#         )
#     )],  # Body of the function (print statement)
#     decorator_list=[]
# )

# # Step 2: Create the module node and assign the function as its body
# module = ast.Module(body=[function_def], type_ignores=[])

# # Step 3: Compile the AST into a Python code object
# # compiled_code = compile(module, filename="<ast>", mode="exec")
# print(astor.to_source(module))
# # # Step 4: Execute the compiled code
# # exec(compiled_code)

# # # Now you can call the function
# # hello()  # Output: Hello, World!

