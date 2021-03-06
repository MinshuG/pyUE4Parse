from UE4Parse.Textures.Objects.FTexture2DMipMap import FTexture2DMipMap
from UE4Parse.Objects.EPixelFormat import EPixelFormat
from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.PakFile.PakObjects.EPakVersion import EPakVersion
from UE4Parse.Globals import FGame
from typing import List


class FTexturePlatformData:
    SizeX: int
    SizeY: int
    NumSlices: int
    PixelFormat: EPixelFormat
    Mips: List[FTexture2DMipMap]
    VirtualData = None
    bIsVirtual = False
    FirstMipToSerialize: int

    def __init__(self, reader: BinaryStream, ubulk: BinaryStream, ubulkOffset: int):
        self.SizeX = reader.readInt32()
        self.SizeY = reader.readInt32()
        self.NumSlices = reader.readInt32()  # 1 for normal textures

        self.PixelFormat = EPixelFormat[reader.readFString()]
        self.Serialize(reader, ubulk, ubulkOffset)

    def Serialize(self, reader: BinaryStream, ubulk: BinaryStream, ubulkOffset: int):
        self.FirstMipToSerialize = reader.readInt32() - 1
        self.Mips = reader.readTArray_W_Arg(FTexture2DMipMap, reader, ubulk, ubulkOffset)
        if FGame.Version.value > EPakVersion.FNAME_BASED_COMPRESSION_METHOD.value or FGame.SubVersion == 1:
            self.bIsVirtual = reader.readInt32() != 0
            if self.bIsVirtual:
                raise NotImplementedError("Virtual Textures ar not Not implemented")

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
