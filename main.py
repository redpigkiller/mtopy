import ast


code = """
sum = 0

for i in np.arange(1, 5 + 1):
    sum = sum + i
"""

print(ast.dump(ast.parse(code), indent=2))
print(ast.unparse(ast.parse(code)))
print('----------------------------------------------')
code = """
sum = 0
for i in np.arange(1, 5 + 1):
    sum = sum + i
"""

print(ast.dump(ast.parse(code), indent=2))
print(ast.unparse(ast.parse(code)))