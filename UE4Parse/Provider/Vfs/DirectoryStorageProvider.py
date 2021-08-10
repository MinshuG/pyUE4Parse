from typing import Union, TYPE_CHECKING, List, Dict, Optional

from .DirectoryStorage import DirectoryStorage
from ..Common import GameFile

if TYPE_CHECKING:
    from ...IO import FFileIoStoreReader
    from ...PakFile.PakReader import PakReader


class DirectoryStorageProvider:
    Storage: List[DirectoryStorage]
    IsCaseInsensitive: bool

    def __init__(self, is_case_insensitive: bool):
        self.IsCaseInsensitive = is_case_insensitive
        self.Storage = []

    def add_storage(self, storage: DirectoryStorage):
        self.Storage.append(storage)

    def add_index(self, index: Dict[str, GameFile], container: Union['FFileIoStoreReader', 'PakReader']):
        self.add_storage(DirectoryStorage(index, container, self.IsCaseInsensitive))

    def get(self, path) -> Optional[GameFile]:
        for storage in self.Storage:
            result = storage.try_get(path)
            if result is not None:
                return result
        return None
