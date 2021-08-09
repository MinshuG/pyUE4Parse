from typing import Tuple

from UE4Parse.Assets.Objects.FPackageIndex import FPackageIndex
from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Assets.Exports.UObjects import UObject
from UE4Parse.Assets.Exports.ExportRegistry import register_export
from UE4Parse.Assets.Objects.URL import FURL


@register_export
class ULevel(UObject):
    URL: FURL
    Actors: Tuple[FPackageIndex]
    Model: FPackageIndex
    ModelComponents: Tuple[FPackageIndex]
    LevelScriptActor: FPackageIndex
    NavListStart: FPackageIndex
    NavListEnd: FPackageIndex

    def __init__(self, reader: BinaryStream):
        super().__init__(reader)

    def deserialize(self, validpos):
        super().deserialize(validpos)
        reader = self.reader

        self.Actors = reader.readTArray(FPackageIndex, reader)
        self.URL = FURL(reader)
        self.Model = FPackageIndex(reader)
        self.ModelComponents = reader.readTArray(FPackageIndex, reader)
        self.LevelScriptActor = FPackageIndex(reader)
        self.NavListStart = FPackageIndex(reader)
        self.NavListEnd = FPackageIndex(reader)
        # rest later
