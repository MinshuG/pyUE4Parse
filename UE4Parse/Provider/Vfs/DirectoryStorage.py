import os
import typing
from typing import Dict, Union

if typing.TYPE_CHECKING:
    from UE4Parse.IO import FFileIoStoreReader
    from UE4Parse.PakFile.PakReader import PakReader
    from UE4Parse.Provider.Common import GameFile


def remove_slash(string):
    """removes / from starting of a string"""
    if string.startswith("/"):
        return string[1:]
    return string


class DirectoryStorage:
    IsCaseInsensitive: bool
    _files: Dict[str, 'GameFile']
    _raw_names: Dict[str, str]
    _container: typing.Union['FFileIoStoreReader', 'PakReader']

    def __init__(self, index: Dict[str, 'GameFile'], container: Union['FFileIoStoreReader', 'PakReader'] ,is_case_insensitive=False):
        self.IsCaseInsensitive = is_case_insensitive
        self._container = container
        self.process_index(index)

    def process_index(self, Index: Dict[str, 'GameFile']):
        self._files: Dict[str, 'GameFile'] = {}
        self._raw_names = {}
        for entry, IndexEntry in Index.items():
            if entry.endswith((".uexp", ".ubulk", ".uptnl")):
                continue

            path_no_ext = os.path.splitext(entry)[0]
            uexp = path_no_ext + ".uexp"
            ubulk = path_no_ext + ".ubulk"
            uptnl = path_no_ext + ".uptnl"

            if uexp in Index:
                IndexEntry.uexp = Index[uexp]

            if ubulk in Index:
                IndexEntry.ubulk = Index[ubulk]

            if uptnl in Index:
                IndexEntry.uptnl = Index[uptnl]

            path = remove_slash(path_no_ext)
            self._files[path] = IndexEntry
            self._raw_names[IndexEntry.Name] = path

    def try_get(self, path: str, default=None):
        if out := self._files.get(path.lower() if self.IsCaseInsensitive else path, None):
            return out
        elif out := self._raw_names.get(path):
            return self.try_get(out, default)
        return default

    def __str__(self):
        return f"<{len(self._files)} files | {self._container.FileName}>"
