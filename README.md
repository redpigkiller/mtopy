# mtopy
Convert Matlab code TO Python.
This project was created for learning purposes and as a fun side project in my spare time. It has not undergone extensive testing, and there are still many incomplete features (impractical to use). As such, please be aware that bugs or unfinished parts are to be expected.

## Usage

### Installation
Currently no installation package is provided. Clone this project to your local folder, and install it by running
```bash
pip install .
```

### Requirement
The [lark-parser](https://github.com/lark-parser/lark) is needed. 

### Run
```bash
usage: mtopy [-h] -f FILE [-p] -o OUTPUT

Simple program that converts matlab to python

options:
  -h, --help                       show this help message and exit
  -f FILE, --file FILE             path of a single file or project main file
  -p, --project                    consider the files in the same folder (only used for single file)
  -o OUTPUT, --output OUTPUT       path of the output file or folder
```

1. Convert a single file:
```bash
python -m mtopy -f input_file -o output_file
```
2. Convert a project:
```bash
python -m mtopy -f main_file_of_the_project -p -o output_folder
```

## How it works
The steps of the conversion are:
1. tokenizing matlab code
2. parse the tokenized matlab code, and generate the custom matlab parse tree
3. transform custom matlab parse tree to python AST; the transform function can use symbol table to record the variables that are assigned in the code
4. transform the python AST using both the symbol table and converter
5. unparse the python AST to python code

Step 3 needs a symbol table (optional) to record the variables and functions, so it can tell the matlab code: ``a()`` is a function call or array indexing. In addition, the ``cd`` and ``addpath`` would be considered in this step.

Step 4 needs a converter that converts the matlab function to the corresponding python function, if the numpy package is used, then ``sin()`` will be converted to ``np.sin()``.

## Others
To-do
1. Add more functions in converter
2. Improve error handling of parser, transformer, ...
