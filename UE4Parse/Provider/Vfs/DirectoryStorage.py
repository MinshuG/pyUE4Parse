import os
import re
from functools import singledispatchmethod
from typing import Dict, Union, TYPE_CHECKING, Optional

from UE4Parse.IO.IoObjects import FIoStoreEntry
from UE4Parse.IoObjects.FImportedPackage import FPackageId

if TYPE_CHECKING:
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
    _container: Union['FFileIoStoreReader', 'PakReader']

    def __init__(self, index: Dict[str, 'GameFile'], container: Union['FFileIoStoreReader', 'PakReader'],
                 is_case_insensitive=False):
        self.IsCaseInsensitive = is_case_insensitive
        self._container = container
        self.process_index(index)

    @property
    def files(self) -> Dict[str, 'GameFile']:
        return self._files

    def get_container(self) -> Union['FFileIoStoreReader', 'PakReader']:
        return self._container

    def process_index(self, index: Dict[str, 'GameFile']):
        self._files: Dict[str, 'GameFile'] = {}
        for entry, IndexEntry in index.items():
            if entry.endswith((".uexp", ".ubulk", ".uptnl")):
                continue

            path_no_ext = os.path.splitext(entry)[0]
            uexp = path_no_ext + ".uexp"
            ubulk = path_no_ext + ".ubulk"
            uptnl = path_no_ext + ".uptnl"

            if uexp in index:
                IndexEntry.uexp = index[uexp]

            if ubulk in index:
                IndexEntry.ubulk = index[ubulk]

            if uptnl in index:
                IndexEntry.uptnl = index[uptnl]

            path = remove_slash(os.path.join(self._container.get_mount_point() , path_no_ext))
            if self.IsCaseInsensitive:
                self._files[path.lower()] = IndexEntry
            else:
                self._files[path] = IndexEntry

    @singledispatchmethod
    def try_get(self, path: str, default=None) -> Optional[str]:
        if out := self._files.get(path.lower() if self.IsCaseInsensitive else path, None):
            return out
        return default

    @try_get.register
    def _(self, id: FPackageId, default=None):
        for name, package in self._files.items():
            if isinstance(package, FIoStoreEntry):
                if id.Id == package.ChunkId.ChunkId:
                    return package
        return default

    def __str__(self):
        return f"{len(self._files)} files | {self._container.FileName} | Mounted to: {self._container.get_mount_point()}"

    def __repr__(self):
        return f"<{self.__str__()}>"
