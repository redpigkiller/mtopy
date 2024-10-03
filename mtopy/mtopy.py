import ast
from pathlib import Path
from typing import *

from .core.parser import Parser
from .core.mtree_to_pytree import MPTreeConverter
from .core.pytree_transformer import MPTreeTransformer
from .core import parser_error as ParserError
from .core import conversion_error as ConversionError
from .core.function_table import FunctionTable

from .convert_utils.default_converter import DefaultConverter


class MatlabToPythonConverter:
    def __init__(self):
        self._parser = Parser()
        self._converter = DefaultConverter()

        self.reset()

    def reset(self) -> None:
        self._func_table = FunctionTable()
        self._mptree_converter = MPTreeConverter(function_table=self._func_table)

    def convert_code(self, matlab_code: str) -> str:
        try:
            matlab_ast = self._parser.parse(matlab_code)
        except ParserError.NotImplementedFeatureError as e:
            print("NotImplementedFeatureError")
            return None
        except Exception as e:
            print('Parsing error: ', e)
            return None
        
        try:
            python_ast = self._mptree_converter.convert(matlab_ast)
        except ConversionError.NotImplementedConversionError as e:
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
    
    def convert_file(self, src_file_path: str, dest_file_path: str) -> None:
        self._func_table = FunctionTable(Path(src_file_path).parent)
        self._mptree_converter = MPTreeConverter(function_table=self._func_table)

        with open(Path(src_file_path), 'r') as f:
            matlab_code = f.read()

        python_code = self.convert_code(matlab_code)

        with open(Path(dest_file_path), 'w') as f:
            f.write(python_code)

    def convert_project(self, main_file_path: str, dest_folder: str) -> None:
        project_file_list = list(Path(main_file_path).parent.rglob("*.m"))
        project_file_list.insert(0, project_file_list.pop(project_file_list.index(Path(main_file_path))))

        self._func_table = FunctionTable(main_file_path)
        for matlab_file in project_file_list:
            self._mptree_converter = MPTreeConverter(function_table=self._func_table)

            with open(matlab_file, 'r', encoding='utf-8') as f:
                matlab_code = f.read()

            python_code = self.convert_code(matlab_code)

            self._func_table = self._mptree_converter.get_function_table()

            if python_code is None:
                print(f"Conversion failed for {matlab_file}")
                continue

            out_dir = Path(dest_folder) / matlab_file.relative_to(Path(main_file_path).parent)
            out_dir.parent.mkdir(parents=True, exist_ok=True)

            with open(out_dir.with_suffix('.py'), 'w') as f:
                f.write(python_code)
