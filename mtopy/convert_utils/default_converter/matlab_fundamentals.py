import ast

from .utility import construct_attribute_call_ast

class MatlabFundamentals:
    """Generates AST nodes for MATLAB-like functions"""
    
    def clc(self, args: list[ast.AST]) -> ast.AST:
        return ast.Constant(value="# clc")
    
    def close(self, args: list[ast.AST]) -> ast.AST:
        return ast.Constant(value="# close")
    
    def clear(self, args: list[ast.AST]) -> ast.AST:
        return ast.Constant(value="# clear")

    def zeros(self, args: list[ast.AST]) -> ast.AST:
        """Generate AST for numpy.zeros() call"""
        args = [ast.Tuple(elts=args, ctx=ast.Load())]
        return construct_attribute_call_ast(["np", "zeros"], args)
    
    def ones(self, args: list[ast.AST]) -> ast.AST:
        """Generate AST for numpy.ones() call"""
        args = [ast.Tuple(elts=args, ctx=ast.Load())]
        return construct_attribute_call_ast(["np", "ones"], args)
    
    def ndims(self, args: list[ast.AST]) -> ast.AST:
        """Generate AST for numpy.ndim attribute access"""
        assert len(args) == 1, "ndims takes exactly one argument"
        return ast.Attribute(value=args[0], attr="ndim", ctx=ast.Load())
    
    def size(self, args: list[ast.AST]) -> ast.AST:
        """Generate AST for numpy.shape attribute access or indexing"""
        assert len(args) >= 1 and len(args) <= 2, "size takes one or two arguments"
        
        # Get the shape attribute
        shape_attr = ast.Attribute(value=args[0], attr="shape", ctx=ast.Load())
        
        # If a dimension is specified, return that specific dimension
        if len(args) == 2:
            # Subtract 1 from the dimension index (MATLAB is 1-based, Python is 0-based)
            adjusted_index = ast.BinOp(
                left=args[1],
                op=ast.Sub(),
                right=ast.Constant(value=1)
            )
            return ast.Subscript(
                value=shape_attr,
                slice=adjusted_index,
                ctx=ast.Load()
            )
        
        return shape_attr
    
    def length(self, args: list[ast.AST]) -> ast.AST:
        """Generate AST for computing maximum dimension length"""
        assert len(args) == 1, "length takes exactly one argument"
        
        # Get shape attribute
        shape_attr = ast.Attribute(value=args[0], attr="shape", ctx=ast.Load())
        
        # Create max() call
        return self._construct_attribute_call_ast(["max"], [shape_attr])
    
    def eye(self, args: list[ast.AST]) -> ast.AST:
        """Generate AST for numpy.eye() call"""
        return self._construct_attribute_call_ast(["np", "eye"], args)
    
    def linspace(self, args: list[ast.AST]) -> ast.AST:
        """Generate AST for numpy.linspace() call"""
        return self._construct_attribute_call_ast(["np", "linspace"], args)
    
    # def reshape(self, args: list[ast.AST]) -> ast.AST:
    #     """Generate AST for numpy.reshape() call"""
    #     assert len(args) >= 2, "reshape requires at least two arguments"
    #     array = args[0]
    #     shape_args = args[1:]
        
    #     if len(shape_args) == 1:
    #         new_shape = shape_args[0]
    #     else:
    #         new_shape = ast.Tuple(elts=shape_args, ctx=ast.Load())
        
    #     return self._construct_attribute_call_ast(
    #         ["np", "reshape"],
    #         [array, new_shape]
    #     )
    
    # def repmat(self, args: list[ast.AST]) -> ast.AST:
    #     """Generate AST for numpy.tile() call"""
    #     assert len(args) >= 2, "repmat requires at least two arguments"
    #     array = args[0]
    #     reps = args[1:]
        
    #     if len(reps) == 1:
    #         reps_tuple = reps[0]
    #     else:
    #         reps_tuple = ast.Tuple(elts=reps, ctx=ast.Load())
        
    #     return self._construct_attribute_call_ast(
    #         ["np", "tile"],
    #         [array, reps_tuple]
    #     )

    # def disp(self, args: list[ast.AST]) -> ast.AST:
    #     return self._construct_attribute_call_ast(['print'], args)

    # def mat2str(self, args: list[ast.AST]) -> ast.AST:
    #     return self._construct_attribute_call_ast(['np', 'array2string'], args)
    
    # def num2str(self, args: list[ast.AST]) -> ast.AST:
    #     return self._construct_attribute_call_ast(['str'], args)

    # def strcmp(self, args: list[ast.AST]) -> ast.AST:
    #     """Generate AST for string comparison (str1 == str2)"""
    #     assert len(args) == 2, "strcmp takes exactly two arguments"
    #     return ast.Compare(
    #         left=args[0],
    #         ops=[ast.Eq()],
    #         comparators=[args[1]]
    #     )
    
    # def strcmpi(self, args: list[ast.AST]) -> ast.AST:
    #     """Generate AST for case-insensitive string comparison"""
    #     assert len(args) == 2, "strcmpi takes exactly two arguments"
    #     # Convert both strings to lower case before comparison
    #     lower1 = ast.Call(
    #         func=ast.Attribute(value=args[0], attr='lower', ctx=ast.Load()),
    #         args=[], keywords=[]
    #     )
    #     lower2 = ast.Call(
    #         func=ast.Attribute(value=args[1], attr='lower', ctx=ast.Load()),
    #         args=[], keywords=[]
    #     )
    #     return ast.Compare(
    #         left=lower1,
    #         ops=[ast.Eq()],
    #         comparators=[lower2]
    #     )
    
    # def error(self, args: list[ast.AST]) -> ast.AST:
    #     """Generate AST for raising an error"""
    #     assert len(args) >= 1, "error takes at least one argument"
    #     return ast.Raise(
    #         exc=ast.Call(
    #             func=ast.Name(id='RuntimeError', ctx=ast.Load()),
    #             args=args,
    #             keywords=[]
    #         ),
    #         cause=None
    #     )
    
    # def warning(self, args: list[ast.AST]) -> ast.AST:
    #     """Generate AST for warning message"""
    #     assert len(args) >= 1, "warning takes at least one argument"
    #     return self._construct_attribute_call_ast(
    #         ['warnings', 'warn'],
    #         args
    #     )
    
    # def uint8(self, args: list[ast.AST]) -> ast.AST:
    #     """Generate AST for uint8 conversion"""
    #     assert len(args) == 1, "uint8 takes exactly one argument"
    #     return self._construct_attribute_call_ast(
    #         ['np', 'uint8'],
    #         args
    #     )
    
    # def bitset(self, args: list[ast.AST]) -> ast.AST:
    #     """Generate AST for setting a bit
    #     Note: MATLAB's bitset is 1-based, need to adjust index"""
    #     assert len(args) >= 2, "bitset takes at least two arguments"
    #     value, bit = args[:2]
    #     # Adjust for 0-based indexing
    #     adjusted_bit = ast.BinOp(
    #         left=bit,
    #         op=ast.Sub(),
    #         right=ast.Constant(value=1)
    #     )
    #     # Create: value | (1 << (bit - 1))
    #     return ast.BinOp(
    #         left=value,
    #         op=ast.BitOr(),
    #         right=ast.BinOp(
    #             left=ast.Constant(value=1),
    #             op=ast.LShift(),
    #             right=adjusted_bit
    #         )
    #     )
    
    # def fullfile(self, args: list[ast.AST]) -> ast.AST:
    #     """Generate AST for path joining using pathlib"""
    #     assert len(args) >= 1, "fullfile takes at least one argument"
    #     return self._construct_attribute_call_ast(
    #         ['pathlib', 'Path'],
    #         [args[0]]
    #     ).joinpath(*args[1:])
    
    # def fprintf(self, args: list[ast.AST]) -> ast.AST:
    #     """Generate AST for fprintf
    #     Note: MATLAB's fprintf can write to file or stdout"""
    #     assert len(args) >= 1, "fprintf takes at least one argument"
    #     if isinstance(args[0], ast.Constant) and isinstance(args[0].value, str):
    #         # stdout case
    #         return self._construct_attribute_call_ast(
    #             ['print'],
    #             args,
    #             [ast.keyword(arg='end', value=ast.Constant(value=''))]
    #         )
    #     else:
    #         # file case
    #         file_obj = args[0]
    #         format_str = args[1]
    #         format_args = args[2:]
    #         return ast.Call(
    #             func=ast.Attribute(value=file_obj, attr='write', ctx=ast.Load()),
    #             args=[
    #                 ast.Call(
    #                     func=ast.Attribute(
    #                         value=format_str,
    #                         attr='format',
    #                         ctx=ast.Load()
    #                     ),
    #                     args=format_args,
    #                     keywords=[]
    #                 )
    #             ],
    #             keywords=[]
    #         )
    
    # def sprintf(self, args: list[ast.AST]) -> ast.AST:
    #     """Generate AST for sprintf"""
    #     assert len(args) >= 1, "sprintf takes at least one argument"
    #     format_str = args[0]
    #     format_args = args[1:]
    #     return ast.Call(
    #         func=ast.Attribute(
    #             value=format_str,
    #             attr='format',
    #             ctx=ast.Load()
    #         ),
    #         args=format_args,
    #         keywords=[]
    #     )
    
    # def load(self, args: list[ast.AST]) -> ast.AST:
    #     """Generate AST for loading data
    #     Note: This assumes .mat files are handled by scipy.io.loadmat
    #           and other files by numpy.load"""
    #     assert len(args) >= 1, "load takes at least one argument"
    #     filename = args[0]
        
    #     # Check if file ends with .mat
    #     is_mat_file = ast.Call(
    #         func=ast.Attribute(
    #             value=ast.Str(s=str(filename)),
    #             attr='endswith',
    #             ctx=ast.Load()
    #         ),
    #         args=[ast.Str(s='.mat')],
    #         keywords=[]
    #     )
        
    #     return ast.IfExp(
    #         test=is_mat_file,
    #         body=self._construct_attribute_call_ast(
    #             ['scipy', 'io', 'loadmat'],
    #             args
    #         ),
    #         orelse=self._construct_attribute_call_ast(
    #             ['np', 'load'],
    #             args
    #         )
    #     )
    
    # def save(self, args: list[ast.AST]) -> ast.AST:
    #     """Generate AST for saving data
    #     Note: Similar to load, handles .mat files differently"""
    #     assert len(args) >= 2, "save takes at least two arguments"
    #     filename = args[0]
        
    #     is_mat_file = ast.Call(
    #         func=ast.Attribute(
    #             value=ast.Str(s=str(filename)),
    #             attr='endswith',
    #             ctx=ast.Load()
    #         ),
    #         args=[ast.Str(s='.mat')],
    #         keywords=[]
    #     )
        
    #     return ast.IfExp(
    #         test=is_mat_file,
    #         body=self._construct_attribute_call_ast(
    #             ['scipy', 'io', 'savemat'],
    #             args
    #         ),
    #         orelse=self._construct_attribute_call_ast(
    #             ['np', 'save'],
    #             args
    #         )
    #     )
    
    # def mkdir(self, args: list[ast.AST]) -> ast.AST:
    #     """Generate AST for creating directories"""
    #     assert len(args) >= 1, "mkdir takes at least one argument"
    #     return ast.Call(
    #         func=ast.Attribute(
    #             value=ast.Call(
    #                 func=ast.Name(id='Path', ctx=ast.Load()),
    #                 args=[args[0]],
    #                 keywords=[]
    #             ),
    #             attr='mkdir',
    #             ctx=ast.Load()
    #         ),
    #         args=[],
    #         keywords=[
    #             ast.keyword(arg='parents', value=ast.Constant(value=True)),
    #             ast.keyword(arg='exist_ok', value=ast.Constant(value=True))
    #         ]
    #     )
    
    # def exist(self, args: list[ast.AST]) -> ast.AST:
    #     """Generate AST for checking existence
    #     Note: MATLAB's exist is more complex, this covers file/directory case"""
    #     assert len(args) >= 1, "exist takes at least one argument"
    #     return ast.Call(
    #         func=ast.Attribute(
    #             value=ast.Call(
    #                 func=ast.Name(id='Path', ctx=ast.Load()),
    #                 args=[args[0]],
    #                 keywords=[]
    #             ),
    #             attr='exists',
    #             ctx=ast.Load()
    #         ),
    #         args=[],
    #         keywords=[]
    #     )
    
    # def join(self, args: list[ast.AST]) -> ast.AST:
    #     """Generate AST for string joining"""
    #     assert len(args) >= 1, "join takes at least one argument"
    #     return ast.Call(
    #         func=ast.Attribute(
    #             value=args[0],
    #             attr='join',
    #             ctx=ast.Load()
    #         ),
    #         args=args[1:],
    #         keywords=[]
    #     )
    
    # def string(self, args: list[ast.AST]) -> ast.AST:
    #     """Generate AST for string conversion"""
    #     assert len(args) >= 1, "string takes at least one argument"
    #     return ast.Call(
    #         func=ast.Name(id='str', ctx=ast.Load()),
    #         args=args,
    #         keywords=[]
    #     )
    
    # def datetime(self, args: list[ast.AST]) -> ast.AST:
    #     """Generate AST for datetime creation
    #     Note: Behavior differs between MATLAB and Python datetime"""
    #     return self._construct_attribute_call_ast(
    #         ['datetime', 'datetime'],
    #         args
    #     )
    
    # def tic(self, args: list[ast.AST]) -> ast.AST:
    #     """Generate AST for starting a timer"""
    #     return self._construct_attribute_call_ast(
    #         ['time', 'perf_counter'],
    #         []
    #     )
    
    # def toc(self, args: list[ast.AST]) -> ast.AST:
    #     """Generate AST for stopping a timer and getting elapsed time
    #     Note: Requires storing the tic time in a variable"""
    #     assert len(args) == 1, "toc takes exactly one argument (the tic time)"
    #     return ast.BinOp(
    #         left=self._construct_attribute_call_ast(
    #             ['time', 'perf_counter'],
    #             []
    #         ),
    #         op=ast.Sub(),
    #         right=args[0]
    #     )
    
    # def isfile(self, args: list[ast.AST]) -> ast.AST:
    #     """Generate AST for checking if path is a file"""
    #     assert len(args) == 1, "isfile takes exactly one argument"
    #     return ast.Call(
    #         func=ast.Attribute(
    #             value=ast.Call(
    #                 func=ast.Name(id='Path', ctx=ast.Load()),
    #                 args=[args[0]],
    #                 keywords=[]
    #             ),
    #             attr='is_file',
    #             ctx=ast.Load()
    #         ),
    #         args=[],
    #         keywords=[]
    #     )
    
    # def squeeze(self, args: list[ast.AST]) -> ast.AST:
    #     """Generate AST for removing singleton dimensions"""
    #     assert len(args) >= 1, "squeeze takes at least one argument"
    #     return self._construct_attribute_call_ast(
    #         ['np', 'squeeze'],
    #         args
    #     )