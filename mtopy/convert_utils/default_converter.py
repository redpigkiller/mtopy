from abc import ABC, ABCMeta, abstractmethod
import ast
from typing import *

from ..converter import MatlabTypeConverter


class DefaultConverter(MatlabTypeConverter):
    def create_mat(self, elements: list[list[ast.AST]]) -> ast.AST:
        return ast.Call(
            func=ast.Attribute(value=ast.Name(id='np', ctx=ast.Load()), attr='array', ctx=ast.Load()),
            args=[ast.List(elts=[ast.List(elts=row, ctx=ast.Load()) for row in elements], ctx=ast.Load())],
            keywords=[]
        )
    
    def access_mat(self, identifier: ast.AST, arguments: list[ast.AST]) -> ast.AST:
        if len(arguments) == 1:
            arguments = arguments[0]
        elif len(arguments) > 1:
            arguments = ast.Tuple(elts=arguments)
        return ast.Subscript(value=identifier, slice=arguments)
    
    def create_cell(self, elements: list[list[ast.AST]]) -> ast.AST:
        return ast.List(elts=[ast.List(elts=row, ctx=ast.Load()) for row in elements], ctx=ast.Load())
    
    def access_cell(self, identifier: ast.AST, arguments: list[ast.AST]) -> ast.AST:
        if len(arguments) == 1:
            arguments = arguments[0]
        elif len(arguments) > 1:
            arguments = ast.Tuple(elts=arguments)
        return ast.Subscript(value=identifier, slice=arguments)
    
    def create_struct(self, elements: list[list[ast.AST]]) -> ast.AST:
        return None
    
    def access_struct(self, identifier: ast.AST, arguments: list[ast.AST]) -> ast.AST:
        struct_element = identifier
        for arg in arguments:
            if isinstance(arg, ast.Name):
                arg = ast.Constant(value=arg.id)
            struct_element = ast.Subscript(value=struct_element, slice=arg, ctx=ast.Load())
        return struct_element
    
    def convert_func(self, func: ast.AST, arguments: list[ast.AST]) -> ast.AST:
        return ast.Call(
            func=func,
            args=arguments if arguments else [],
            keywords=[]
        )
    
    def arange(self, start: ast.AST, stop: list[ast.AST], step: Optional[list[ast.AST]]=None) -> ast.AST:
        func_args = [start, stop]
        if step is not None:
            func_args.append(step)
        else:
            step = ast.Constant(value=1)
        func_args[1] = ast.BinOp(left=stop, op=ast.Add(), right=step)

        return ast.Call(
            func=ast.Attribute(value=ast.Name(id='np', ctx=ast.Load()), attr='arange', ctx=ast.Load()),
            args=func_args,
            keywords=[]
        )
    
    def multiplication(self, left: ast.AST, right: list[ast.AST]) -> ast.AST:
        return ast.BinOp(left=left, op=ast.Mult(), right=right)

    def right_division(self, left: ast.AST, right: list[ast.AST]) -> ast.AST:
        return ast.BinOp(left=left, op=ast.Div(), right=right)
    
    def left_division(self, left: ast.AST, right: list[ast.AST]) -> ast.AST:
        return self.right_division(right, left)
    
    def matrix_multiplication(self, left: ast.AST, right: list[ast.AST]) -> ast.AST:
        return ast.BinOp(left=left, op=ast.MatMult(), right=right)
    
    def matrix_right_division(self, left: ast.AST, right: list[ast.AST]) -> ast.AST:
        if isinstance(left, ast.Constant) or isinstance(right, ast.Constant):
            return self.right_division(left, right)
        else:
            return self.matrix_left_division(
                left=self.transpose(left),
                right=self.transpose(right)
            )
    
    def matrix_left_division(self, left: ast.AST, right: list[ast.AST]) -> ast.AST:
        if isinstance(left, ast.Constant) or isinstance(right, ast.Constant):
            return self.left_division(left, right)
        else:
            return ast.Call(
                func=ast.Attribute(
                    value=ast.Attribute(
                        value=ast.Name(id='np', ctx=ast.Load()),
                        attr='linalg',
                        ctx=ast.Load()
                    ),
                    attr='lstsq',
                    ctx=ast.Load()
                ),
                args=[left, right],
                keywords=[]
            )
    
    def power(self, left: ast.AST, right: list[ast.AST]) -> ast.AST:
        return ast.BinOp(left=left, op=ast.Pow(), right=right)
    
    def matrix_power(self, left: ast.AST, right: list[ast.AST]) -> ast.AST:
        return ast.Call(
            func=ast.Attribute(
                value=ast.Attribute(
                    value=ast.Name(id='np', ctx=ast.Load()),
                    attr='linalg',
                    ctx=ast.Load()
                ),
                attr='matrix_power',
                ctx=ast.Load()
            ),
            args=[left, right],
            keywords=[]
        )
    
    def transpose(self, left: ast.AST) -> ast.AST:
        return ast.Attribute(value=left, attr='T', ctx=ast.Load())
    
    def hermitian(self, left: ast.AST) -> ast.AST:
        return ast.Attribute(
            value=ast.Call(
                func=ast.Attribute(
                    value=left,
                    ctx=ast.Load(),
                    attr='conj'
                ),
                args=[],
                keywords=[]
            ),
            attr='T',
            ctx=ast.Load()
        )