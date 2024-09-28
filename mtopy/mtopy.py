import ast
import os
from pathlib import Path
from typing import *

from .parser import Parser
from .core import parser_error as MParserError
from .core.mtree_to_pytree import MPTreeConverter
from .core import conversion_error as MConversionError
from .core.function_table import FunctionTable
from .core.pytree_transformer import MPTreeTransformer

from .convert_utils.default_converter import DefaultConverter


class MatlabToPythonConverter:
    def __init__(self, project_root: str=""):
        self._parser = Parser()
        self._f_table = FunctionTable(project_root)
        self._mptree_converter = MPTreeConverter(function_table=self._f_table)
        self._converter = DefaultConverter()

    def convert_code(self, matlab_code: str) -> str:
        try:
            matlab_ast = self._parser.parse(matlab_code)
        except MParserError.NotImplementedFeatureError as e:
            print("NotImplementedFeatureError")
            return None
        except Exception as e:
            print('Parsing error: ', e)
            return None

        try:
            python_ast = self._mptree_converter.convert(matlab_ast)
        except MConversionError.NotImplementedConversionError as e:
            print("NotImplementedConversionError")
            return None
        except Exception as e:
            print('Tree conversion error: ', e)
            return None

        transformer = MPTreeTransformer(
            converter=self._converter,
            function_table=self._mptree_converter.get_function_table()
        )

        python_ast = transformer.visit(python_ast)
        
        python_code = ast.unparse(python_ast)

        return python_code

#     def convert_project(self, project_path: str) -> dict[str, str]:
#         """
#         Convert an entire MATLAB project to Python.
#         """
#         self._scan_project()
#         converted_files = {}
#         for file_path in file_pathes:
#             converted_files[file_path] = self._convert_file(file_path)

#         return converted_files
    
