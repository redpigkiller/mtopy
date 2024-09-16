from collections.abc import Generator

from parse_matlab_code import Parser, Tree



class MNodeVisitor:
    def __init__(self) -> None:
        pass

    def visiting(self, node: Tree.Node) -> Generator[Tree.Node]:
        

    def convert(self, node: Tree.Node, cwd: Optional[str]=None, symbol_table: Optional[SymbolTable]=None) -> Optional[ast.AST]:
        if isinstance(node, Tree.Program):
            return ast.Module(
                body=self._body_list_to_ast(node.body),
                type_ignores=[]
            )
        else:
            return None

    def _convert_tree(self, node: Tree.Node, ctx_typ=ast.Load()) -> Optional[ast.AST]:
        assert not isinstance(node, Tree.Program), "Nested tree is not allowed"

        try:
            # Terminal symbols
            if isinstance(node, Tree.Number):
                s = node.value.val
                if 'e' in s.lower():
                    return ast.Constant(value=float(s))
                elif '.' in s:
                    return ast.Constant(value=float(s))
                elif s.lower().startswith('0x'):
                    return ast.Constant(value=int(s, 16))
                else:
                    return ast.Constant(value=int(s))
                
            elif isinstance(node, Tree.ImagNumber):
                return ast.Constant(value=complex(0, float(node.value.val[:-1])))
            elif isinstance(node, Tree.String):
                return ast.Constant(value=str(node.value.val))
            elif isinstance(node, Tree.Identifier):
                return ast.Name(id=str(node.value.val), ctx=ctx_typ)
            elif isinstance(node, Tree.Ignore):
                return ast.Name(id='_', ctx=ctx_typ)
            elif isinstance(node, Tree.COLON):
                return ast.Slice()
            elif isinstance(node, (Tree.WhiteSpace, Tree.Comment, Tree.Ellipsis, Tree.EndOfLine)):
                return None
            
            elif isinstance(node, Tree.FunctionDefinition):
                func_body = self._body_list_to_ast(node.body)

                ret_var = [ast.arg(arg=self._convert_tree(param).id) for param in node.output_params]
                if len(ret_var) == 1:
                    func_body.append(ast.Return(value=ret_var[0]))
                elif len(ret_var) > 1:
                    func_body.append(ast.Return(value=ast.Tuple(elts=ret_var)))
                
                return ast.FunctionDef(
                    name=node.name.value.val,
                    args=ast.arguments(
                        posonlyargs=[],
                        args=[ast.arg(arg=self._convert_tree(param).id) for param in node.input_params],
                        kwonlyargs=[],
                        kw_defaults=[],
                        defaults=[]
                    ),
                    body=func_body,
                    decorator_list=[],
                    lineno=1
                )
            
            elif isinstance(node, Tree.AnonymousFunction):
                return ast.Lambda(
                    args=ast.arguments(
                        posonlyargs=[],
                        args=[ast.arg(arg=self._convert_tree(param).id) for param in node.parameters],
                        kwonlyargs=[],
                        kw_defaults=[],
                        defaults=[]
                    ),
                    body=self._convert_tree(node.body[0])  # Assuming single expression for lambda body
                )
            
            elif isinstance(node, Tree.IfStatement):
                return ast.If(
                    test=self._convert_tree(node.condition),
                    body=self._body_list_to_ast(node.then_body),
                    orelse=self._convert_elseif_chain(node.elseif_clauses, node.else_body)
                )
            
            elif isinstance(node, Tree.ForLoop):
                return ast.For(
                    target=self._convert_tree(node.identifier),
                    iter=self._convert_tree(node.expression),
                    body=self._body_list_to_ast(node.body),
                    orelse=[]
                )
            
            elif isinstance(node, Tree.ParforLoop):
                raise NotImplementedError("parfor not implemented")
            elif isinstance(node, Tree.SPMDStatement):
                raise NotImplementedError("spmd not implemented")
            
            elif isinstance(node, Tree.WhileLoop):
                return ast.While(
                    test=self._convert_tree(node.condition),
                    body=self._body_list_to_ast(node.body),
                    orelse=[]
                )
            
            elif isinstance(node, Tree.SwitchStatement):
                return self._convert_switch_to_if(node)
            
            elif isinstance(node, Tree.TryCatchStatement):
                return ast.Try(
                    body=self._body_list_to_ast(node.try_body),
                    handlers=[ast.ExceptHandler(
                        type=self._convert_tree(node.exception) if node.exception is not None else None,
                        name=None,
                        body=self._body_list_to_ast(node.catch_body)
                    )],
                    orelse=[],
                    finalbody=[]
                )
            
            elif isinstance(node, Tree.BreakStatement):
                return ast.Break()
            
            elif isinstance(node, Tree.ContinueStatement):
                return ast.Continue()
            
            elif isinstance(node, Tree.ReturnStatement):
                return ast.Return(value=None)  # MATLAB's 'return' doesn't specify a value
            
            elif isinstance(node, Tree.Assignment):
                # lineno = node.lvalue[-1].value.ln + 1
                lineno = 1
                return ast.Assign(
                    targets=[self._convert_tree(lval, ast.Store()) for lval in node.lvalue],
                    value=self._convert_tree(node.rvalue),
                    lineno=lineno
                )
            
            elif isinstance(node, Tree.FunctionCall):
                if node.arguments is not None:
                    arguments = [self._convert_tree(arg) for arg in node.arguments.indices if arg is not None]
                else:
                    arguments = None
                return self.config.converter.convert_func(
                    node.identifier.value.val,
                    arguments
                )
            
            elif isinstance(node, Tree.ArrayAccess):
                return self.config.converter.access_mat(
                    self._convert_tree(node.identifier),
                    [self._convert_tree(index) for index in node.arguments.indices],
                )
            
            elif isinstance(node, Tree.CellArrayAccess):
                return self.config.converter.access_cell(
                    self._convert_tree(node.identifier),
                    [self._convert_tree(index) for index in node.arguments.indices],
                )
            
            elif isinstance(node, Tree.StructAccess):
                return self.config.converter.access_struct(
                    self._convert_tree(node.identifier),
                    [self._convert_tree(arg) for arg in node.arguments]
                )
            
            elif isinstance(node, Tree.MatrixExpression):
                return self.config.converter.create_mat([[self._convert_tree(elem) for elem in row] for row in node.elements])
            
            elif isinstance(node, Tree.CellArrayExpression):
                return self.config.converter.create_cell([[self._convert_tree(elem) for elem in row] for row in node.elements])

            elif isinstance(node, Tree.ColonArray):
                return self.config.converter.arange(
                    start=self._convert_tree(node.start),
                    stop=self._convert_tree(node.stop),
                    step=self._convert_tree(node.step) if node.step else None,
                )
            
            elif isinstance(node, Tree.BinaryOperation):
                op = self._binop_map.get(node.operator, None)
                
                if op is not None:
                    return ast.BinOp(
                        left=self._convert_tree(node.left),
                        op=op,
                        right=self._convert_tree(node.right)
                    )
                else:
                    convert_func = getattr(self.config.converter, node.operator)
                    return convert_func(self._convert_tree(node.left), self._convert_tree(node.right))
            
            elif isinstance(node, Tree.UnaryOperation):
                op = self._binop_map.get(node.operator, None)
                if op is not None:
                    return ast.UnaryOp(
                        op=op,
                        operand=self._convert_tree(node.operand)
                    )
                else:
                    convert_func = getattr(self.config.converter, node.operator)
                    return convert_func(self._convert_tree(node.operand))
            
            raise NotImplementedError(f"Conversion not implemented for node type: {type(node)}")
            
        except MPTreeConversionError as e:
            raise MPTreeConversionError(e.message, e.node)
        
        except Exception as e:
            raise MPTreeConversionError(str(e), node)