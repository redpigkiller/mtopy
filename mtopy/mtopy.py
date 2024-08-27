import ast
import os
from pathlib import Path
from typing import *

from parse_matlab_code import Parser, Tree

class MatlabToPythonProjectConverter:
    def __init__(self, project_root: str):
        self._project_root = project_root

        self._python_asts: dict[str, ast.Module] = {}
        self._matlab_asts: dict[str, Tree] = {}

        self.global_symbol_table: dict[str, Dict[str, Any]] = {}
        self.file_dependencies: dict[str, set] = {}
        self.matlab_builtin_functions = set(['sin', 'cos', 'exp', 'log', 'sqrt'])  # Add more as needed

    def convert_project(self, project_path: str) -> dict[str, str]:
        """
        Convert an entire MATLAB project to Python.
        """
        self._scan_project()
        converted_files = {}
        for file_path in file_pathes:
            converted_files[file_path] = self._convert_file(file_path)

        return converted_files
    
    
    def convert_files(self, file_pathes: Union[str, list[str]]) -> dict[str, str]:
        """
        Convert all MATLAB files to Python, respecting dependencies.
        """
        if isinstance(file_pathes, str):
            file_pathes = [file_pathes]
        
        converted_files = {}
        for file_path in file_pathes:
            converted_files[file_path] = self._convert_file(file_path)

        return converted_files


    def _convert_file(self, file_path: str) -> str:
        with open(file_path, 'r') as f:
            content = f.read()

        matlab_ast = self.parse_matlab(content)
        python_ast = self.convert_matlab_ast(matlab_ast, file_path)
        converted_files[file_path] = astor.to_source(python_ast)
        return converted_files

    def _scan_project(self, project_root: str):
        """
        Scan the entire project to build the global symbol table and file dependencies.
        """
        for file_path in Path(project_root).rglob("*.m"):
            self._scan_file(file_path)

    def _scan_file(self, file_path: str):
        """
        Scan a single MATLAB file to extract function definitions and dependencies.
        """
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Parse the MATLAB file (you'll need to implement this based on your MATLAB parser)
        matlab_ast = self.parse_matlab(content)
        
        # Extract function definitions and update global symbol table
        for node in matlab_ast.body:
            if isinstance(node, FunctionDefinition):
                self.global_symbol_table[node.name.value] = {
                    'type': 'function',
                    'file': file_path,
                    'params': [param.value for param in node.input_params]
                }
        
        # Extract function calls and update file dependencies
        self.file_dependencies[file_path] = set()
        for node in self.traverse_ast(matlab_ast):
            if isinstance(node, FunctionCall):
                func_name = node.identifier.value
                if func_name in self.global_symbol_table:
                    called_file = self.global_symbol_table[func_name]['file']
                    if called_file != file_path:
                        self.file_dependencies[file_path].add(called_file)


    def convert_matlab_ast(self, matlab_ast: Program, file_path: str) -> ast.Module:
        """
        Convert a single MATLAB AST to a Python AST.
        """
        converter = MatlabToPythonConverter(self.global_symbol_table, file_path)
        return converter.convert(matlab_ast)

    def topological_sort(self, graph: Dict[str, set]) -> List[str]:
        """
        Perform a topological sort of the dependency graph.
        """
        result = []
        visited = set()

        def dfs(node):
            if node not in visited:
                visited.add(node)
                for neighbor in graph.get(node, []):
                    dfs(neighbor)
                result.append(node)

        for node in graph:
            dfs(node)

        return list(reversed(result))

    def parse_matlab(self, content: str) -> Program:
        """
        Parse MATLAB code into an AST.
        This is a placeholder - you'll need to implement this using your MATLAB parser.
        """
        # Placeholder implementation
        return Program(name="", body=[])

    def traverse_ast(self, node: Node) -> List[Node]:
        """
        Traverse the AST and yield all nodes.
        """
        yield node
        if hasattr(node, 'body'):
            for child in node.body:
                yield from self.traverse_ast(child)
        elif hasattr(node, 'elements'):
            for row in node.elements:
                for elem in row:
                    yield from self.traverse_ast(elem)

class MatlabToPythonConverter:
    def __init__(self, global_symbol_table: Dict[str, Dict[str, Any]], current_file: str):
        self.python_ast = None
        self.global_symbol_table = global_symbol_table
        self.current_file = current_file
        self.local_symbol_table: Dict[str, Dict[str, Any]] = {}
        self.matlab_builtin_functions = set(['sin', 'cos', 'exp', 'log', 'sqrt'])  # Add more as needed

    def convert(self, program: Program) -> ast.Module:
        """
        Convert the MATLAB program to a Python AST.
        """
        self.python_ast = ast.Module(body=[], type_ignores=[])
        self.add_imports()
        
        for node in program.body:
            self.python_ast.body.extend(self.convert_node(node))
        
        return self.python_ast

    # ... (rest of the MatlabToPythonConverter methods as before)

    def convert_FunctionCall(self, node: FunctionCall) -> Union[ast.Call, ast.Subscript]:
        """
        Convert a FunctionCall node to either a function call or array indexing in Python.
        """
        if self.is_likely_function(node.identifier):
            func_name = self.convert_node(node.identifier)
            args = [self.convert_node(arg) for arg in node.arguments]
            
            # Check if it's a function from another file
            if isinstance(func_name, ast.Name) and func_name.id in self.global_symbol_table:
                func_info = self.global_symbol_table[func_name.id]
                if func_info['file'] != self.current_file:
                    # It's a function from another file, so we need to import it
                    module_name = os.path.splitext(os.path.basename(func_info['file']))[0]
                    self.add_import(module_name, func_name.id)
                    func_name = ast.Attribute(value=ast.Name(id=module_name, ctx=ast.Load()), attr=func_name.id, ctx=ast.Load())
            
            # Special handling for MATLAB built-in functions
            elif isinstance(func_name, ast.Name) and func_name.id in self.matlab_builtin_functions:
                func_name = ast.Attribute(value=ast.Name(id='np', ctx=ast.Load()), attr=func_name.id, ctx=ast.Load())
            
            return ast.Call(func=func_name, args=args, keywords=[])
        else:
            # Convert to array indexing (as before)
            ...

    def add_import(self, module_name: str, function_name: str):
        """
        Add an import statement for a function from another file.
        """
        import_node = ast.ImportFrom(
            module=module_name,
            names=[ast.alias(name=function_name, asname=None)],
            level=0
        )
        # Add the import to the beginning of the file
        self.python_ast.body.insert(0, import_node)

# Usage
converter = MatlabToPythonProjectConverter("/path/to/matlab/project")
converted_files = converter.convert_project()
for file_path, python_code in converted_files.items():
    print(f"Converted {file_path}:")
    print(python_code)
    print("---")