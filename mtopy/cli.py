from argparse import ArgumentParser
from pathlib import Path

from mtopy import MatlabToPythonConverter

def main():
    parser = ArgumentParser(prog="mtopy", description='Simple program that converting matlab to python')

    parser.add_argument('-f', '--file', required=True, help='path of a single file or project main file')
    parser.add_argument('-p', '--project', action='store_true', help='consider the files in the same folder (only used for single file)')
    parser.add_argument('-o', '--output', required=True, help='path of the output file or folder')

    args = parser.parse_args()

    converter = MatlabToPythonConverter()

    path = Path(args.file)

    if path.is_file():
        if args.project:
            out_path = Path(args.output)
            converter.convert_project(path, out_path)

        else:
            print(f"Process single file: {path}")
            out_path = Path(args.output)
            out_path = out_path.with_suffix('.py')
            converter.convert_file(path, out_path)
            print(f"Save to: {out_path}")

    elif path.is_dir():
        parser.error("-f only accept the path of a single file or project main file")

    else:
        parser.error(f"File {path} does not exist")

if __name__ == '__main__':
    main()