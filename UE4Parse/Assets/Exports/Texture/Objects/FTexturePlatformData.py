from typing import List, Tuple

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Assets.Objects.EPixelFormat import EPixelFormat
from UE4Parse.Assets.Objects.EUEVersion import GAME_UE4
from UE4Parse.Assets.Exports.Texture.Objects.FTexture2DMipMap import FTexture2DMipMap


class FTexturePlatformData:
    SizeX: int
    SizeY: int
    NumSlices: int
    PixelFormat: EPixelFormat
    Mips: Tuple[FTexture2DMipMap]
    VirtualData = None
    bIsVirtual = False
    FirstMipToSerialize: int

    def __init__(self, reader: BinaryStream, ubulk: BinaryStream, ubulkOffset: int):
        self.deserialize(reader, ubulk, ubulkOffset)

    def deserialize(self, reader: BinaryStream, ubulk: BinaryStream, ubulkOffset: int):
        self.SizeX = reader.readInt32()
        self.SizeY = reader.readInt32()
        self.NumSlices = reader.readInt32()  # 1 for normal textures
        self.PixelFormat = EPixelFormat[reader.readFString()]

        self.FirstMipToSerialize = reader.readInt32()
        self.Mips = reader.readTArray(FTexture2DMipMap, reader, ubulk, ubulkOffset)
        if reader.game >= GAME_UE4(23):
            self.bIsVirtual = reader.readInt32() != 0
            if self.bIsVirtual:
                raise NotImplementedError("Virtual Textures are not implemented")

    def GetValue(self):
        return {
            "PixelFormat": self.PixelFormat.name,
            "FirstMip": self.FirstMipToSerialize,
            "NumSlices": self.NumSlices,
            "Size": {
                "X": self.SizeX,
                "Y": self.SizeY
            },
            "IsVirtual": self.bIsVirtual,
            "Mips": [x.GetValue() for x in self.Mips]
        }
