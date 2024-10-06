import json
from typing import *
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from functools import reduce
import operator

from . import tree as Tree

class SymbolType(str, Enum):
    """
    A simple symboltype, 
    """
    FUNC = auto()
    VAR = auto()
    UNK = auto()

def get_dict_by_path(root, items):
    """Access a nested object in root by item sequence."""
    return reduce(operator.getitem, items, root)

class SymbolTable:
    def __init__(self, cwd: Optional[str]=None) -> None:
        # Record file names in the added path, must be function!
        self._addpath_scope = {}

        # Record file names in the same folder, must be function!
        self._dir_scope = {}
        
        # Record the symbols in the current file, a nested dict
        self._currfile_scope = {}
        self._currfile_scope_index = []

        if cwd is not None:
            self._cwd = Path(cwd)
            for f in self._cwd.glob("*.m"):
                self._dir_scope[f.stem] = f.absolute()
        else:
            self._cwd = None

    def cd(self, cd_cmd: str) -> None:
        if self._cwd is not None:
            self._cwd = self._cwd / Path(cd_cmd)
            self._dir_scope = {}
            for f in self._cwd.glob("*.m"):
                self._dir_scope[f.stem] = f.absolute()

    def add_path(self, path: str|list[str]) -> None:
        if isinstance(path, str):
            path = [path]

        if self._cwd is not None:
            for p in path:
                new_path = self._cwd / Path(p)
                if not new_path.exists():
                    new_path = Path(p)
                    if not new_path.exists():
                        return
        else:
            for p in path:
                new_path = Path(p)
                if not new_path.exists():
                    return

        for f in new_path.rglob("*.m"):
            self._addpath_scope[f.stem] = f.absolute()

    def enter_scope(self, func_name: str) -> None:
        target_dict = get_dict_by_path(self._currfile_scope, self._currfile_scope_index)
        target_dict[func_name] = {}
        self._currfile_scope_index.append(func_name)

    def exit_scope(self) -> None:
        self._currfile_scope_index.pop()

    def add_symbol(self, name: str, typ: SymbolType) -> None:
        target_dict = get_dict_by_path(self._currfile_scope, self._currfile_scope_index)
        target_dict[name] = typ

    def lookup(self, name: str) -> SymbolType:
        for i in range(len(self._currfile_scope_index)):
            scope_path = self._currfile_scope_index[:len(self._currfile_scope_index)-i]
            target_dict = get_dict_by_path(self._currfile_scope, scope_path)
            if name in target_dict:
                return target_dict[name]

        if name in self._currfile_scope:
            return self._currfile_scope[name]
        
        if name in self._dir_scope:
            return SymbolType.FUNC
        
        if name in self._addpath_scope:
            return SymbolType.FUNC

        return SymbolType.UNK

    def __str__(self) -> str:
        return json.dumps(self._currfile_scope, sort_keys=False, indent=4)


