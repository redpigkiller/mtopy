from abc import ABC, ABCMeta, abstractmethod
import ast
from typing import *

class MatlabTypeConverter(ABC):
    # #################### Create matlab's special datatype ####################
    @abstractmethod
    def create_mat(self, elements: list[list[ast.AST]]) -> ast.AST:
        pass

    @abstractmethod
    def create_cell(self, elements: list[list[ast.AST]]) -> ast.AST:
        pass

    @abstractmethod
    def create_struct(self, elements: list[list[ast.AST]]) -> ast.AST:
        pass

    # #################### Access matlab's special datatype ####################
    @abstractmethod
    def access_mat(self, identifier: ast.AST, arguments: list[ast.AST]) -> ast.AST:
        pass

    @abstractmethod
    def access_cell(self, identifier: ast.AST, arguments: list[ast.AST]) -> ast.AST:
        pass

    @abstractmethod
    def access_struct(self, identifier: ast.AST, arguments: list[ast.AST]) -> ast.AST:
        pass

    # #################### Convert matlab's special functions ####################
    @abstractmethod
    def arange(self, start: ast.AST, stop: list[ast.AST], step: list[ast.AST]) -> ast.AST:
        pass
    
    @abstractmethod
    def convert_call(self, func: ast.AST, arguments: list[ast.AST]) -> ast.AST:
        pass

