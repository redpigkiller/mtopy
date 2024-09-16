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
    def convert_func(self, func: ast.AST, arguments: list[ast.AST]) -> ast.AST:
        pass

    @abstractmethod
    def arange(self, start: ast.AST, stop: list[ast.AST], step: list[ast.AST]) -> ast.AST:
        pass

    @abstractmethod
    def multiplication(self, left: ast.AST, right: list[ast.AST]) -> ast.AST:
        pass

    @abstractmethod
    def right_division(self, left: ast.AST, right: list[ast.AST]) -> ast.AST:
        pass
    
    @abstractmethod
    def left_division(self, left: ast.AST, right: list[ast.AST]) -> ast.AST:
        pass
    
    @abstractmethod
    def matrix_multiplication(self, left: ast.AST, right: list[ast.AST]) -> ast.AST:
        pass
    
    @abstractmethod
    def matrix_right_division(self, left: ast.AST, right: list[ast.AST]) -> ast.AST:
        pass
    
    @abstractmethod
    def matrix_left_division(self, left: ast.AST, right: list[ast.AST]) -> ast.AST:
        pass
    
    @abstractmethod
    def power(self, left: ast.AST, right: list[ast.AST]) -> ast.AST:
        pass
    
    @abstractmethod
    def matrix_power(self, left: ast.AST, right: list[ast.AST]) -> ast.AST:
        pass
    
    @abstractmethod
    def transpose(self, left: ast.AST) -> ast.AST:
        pass
    
    @abstractmethod
    def hermitian(self, left: ast.AST) -> ast.AST:
        pass