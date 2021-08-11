from functools import singledispatchmethod
from typing import Union, TYPE_CHECKING, List, Dict, Optional, Tuple

from .DirectoryStorage import DirectoryStorage
from ..Common import GameFile
from ...IoObjects.FImportedPackage import FPackageId

if TYPE_CHECKING:
    from ...IO import FFileIoStoreReader
    from ...PakFile.PakReader import PakReader


class DirectoryStorageProvider:
    Storage: List[DirectoryStorage]
    IsCaseInsensitive: bool

    def __init__(self, is_case_insensitive: bool):
        self.IsCaseInsensitive = is_case_insensitive
        self.Storage = []

    def __iter__(self) -> Tuple[str, GameFile]:
        for storage in self.Storage:
            for k, v in storage.files.items():
                yield k, v

    def add_storage(self, storage: DirectoryStorage):
        self.Storage.append(storage)

    def add_index(self, index: Dict[str, GameFile], container: Union['FFileIoStoreReader', 'PakReader']):
        self.add_storage(DirectoryStorage(index, container, self.IsCaseInsensitive))

    def resolve_relative_path(self, path: str):
        for storage in self.Storage:
            result = storage.get_full_path(path)
            if result is not None:
                return result
        return None

    @singledispatchmethod
    def get(self, path) -> Optional[GameFile]:
        for storage in self.Storage:
            result = storage.try_get(path)
            if result is not None:
                return result
        return None

    @get.register
    def _(self, id: FPackageId) -> Optional[GameFile]:
        for storage in self.Storage:
            result = storage.try_get(id)
            if result is not None:
                return result
        return None
