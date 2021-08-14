from UE4Parse.Versions.EUEVersion import EUEVersion, Versions
from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Assets.Objects.FByteBulkData import FByteBulkData


class FTexture2DMipMap:
    bCooked: bool
    SizeX: int
    SizeY: int
    SizeZ: int
    BulkData: FByteBulkData

    def __init__(self, reader: BinaryStream, ubulk: BinaryStream, bulkOffset: int) -> None:
        self.bCooked = reader.version >= Versions.VER_UE4_TEXTURE_SOURCE_ART_REFACTOR and reader.readBool()

        self.BulkData = FByteBulkData(reader, ubulk, bulkOffset)
        self.SizeX = reader.readInt32()
        self.SizeY = reader.readInt32()
        if reader.game >= EUEVersion.GAME_UE4_20:
            self.SizeZ = reader.readInt32()
        else:
            self.SizeZ = 1

        if reader.version >= Versions.VER_UE4_TEXTURE_DERIVED_DATA2 and not self.bCooked:
            derivedDataKey = reader.readFString()

    def GetValue(self):
        return {
            "IsCooked": self.bCooked,
            "Size": {
                "X": self.SizeX,
                "Y": self.SizeY,
                "Z": self.SizeZ
            }
        }
