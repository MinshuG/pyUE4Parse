from abc import ABC, abstractmethod
from enum import IntEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from UE4Parse.Assets.Objects.FGuid import FGuid
    from UE4Parse.Readers.FAssetReader import FAssetReader


class EUeBase(ABC):
    class Type(IntEnum): pass
    GUID: FGuid

    @abstractmethod
    def get(self, reader: FAssetReader):
        pass