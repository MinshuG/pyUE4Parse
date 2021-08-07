from typing import Tuple

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Versions.EUEVersion import GAME_UE4, Versions
from UE4Parse.Assets.Objects.Structs.Box import FBox
from UE4Parse.Assets.Objects.Structs.Vector import FIntVector, FVector, FVector2D


class FDistanceFieldVolumeData:
    DistanceFieldVolume: Tuple[int]
    Size: FIntVector
    LocalBoundingBox: FBox
    MeshWasClosed: bool
    BuiltAsIfTwoSided: bool
    MeshwasPlane: bool
    CompressedDistanceFieldVolume: Tuple[int]
    DistanceMinMax: FVector

    def __init__(self, reader: BinaryStream):
        super().__init__()
        if reader.game >= GAME_UE4(16):
            self.CompressedDistanceFieldVolume = reader.readTArray(reader.readByteToInt)
            self.Size = FIntVector(reader)
            self.LocalBoundingBox = FBox(reader)
            self.DistanceMinMax = FVector(reader)
            self.MeshWasClosed = reader.readBool()
            self.BuiltAsIfTwoSided = reader.readBool()
            self.MeshwasPlane = reader.readBool()
            self.DistanceFieldVolume = []
        else:
            self.DistanceFieldVolume = reader.readTArray(reader.readUInt16)
            self.Size = FIntVector(reader)
            self.LocalBoundingBox = FBox(reader)
            self.MeshWasClosed = reader.readBool()
            self.BuiltAsIfTwoSided = reader.readBool() if reader.version >= Versions.VER_UE4_RENAME_CROUCHMOVESCHARACTERDOWN else False
            self.MeshwasPlane = reader.readBool() if reader.version >= Versions.VER_UE4_DEPRECATE_UMG_STYLE_ASSETS else False
            self.CompressedDistanceFieldVolume = []
            self.DistanceMinMax = FVector2D().construct(0, 0)
