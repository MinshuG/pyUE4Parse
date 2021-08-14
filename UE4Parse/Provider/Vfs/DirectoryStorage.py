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


def convert_path(path):
    path = path.split("/")
    content_index = -1
    for i, x in enumerate(path[::-1]):
        if x == "Content":
            content_index = i - (len(path) - 1)
            break
    path = path[abs(content_index) - 1:]
    b_rcontent = True
    fixed_path = [""]
    for x in path:
        if x == "Content" and b_rcontent:
            b_content = False
            continue
        fixed_path.append(x)

    return "/".join(fixed_path).rstrip(".umap").rstrip(".uasset")


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
    def files(self):
        return self._files

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

            path = remove_slash(os.path.join(self._container.get_mount_point() , path_no_ext))
            self._files[path] = IndexEntry
            # if not os.path.splitext(IndexEntry.Name)[0] == path:  # hmm
            #     path_ = path
            if re.search(r"/Plugins/GameFeatures/.*/Content/", path):
                path_ = convert_path(path)
                self._raw_names[path_] = path
            # else:
            #     path_ = IndexEntry.Name
            #
            # self._raw_names[path_] = path

    def get_full_path(self, path: str) -> Optional[str]:
        return self._raw_names.get(path)

    @singledispatchmethod
    def try_get(self, path: str, default=None) -> Optional[str]:
        if out := self._files.get(path.lower() if self.IsCaseInsensitive else path, None):
            return out
        elif out := self._raw_names.get(path):
            return self.try_get(out, default)
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
