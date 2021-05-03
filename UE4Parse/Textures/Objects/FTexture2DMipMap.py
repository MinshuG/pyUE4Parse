from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Objects.FByteBulkData import FByteBulkData


class FTexture2DMipMap:
    bCooked: bool
    SizeX: int
    SizeY: int
    SizeZ: int
    BulkData: FByteBulkData

    def __init__(self, reader: BinaryStream, ubulk: BinaryStream, bulkOffset: int) -> None:
        self.bCooked = reader.readInt32() != 0
        self.BulkData = FByteBulkData(reader, ubulk, bulkOffset)
        self.SizeX = reader.readInt32()
        self.SizeY = reader.readInt32()
        self.SizeZ = reader.readInt32()

    def GetValue(self):
        return {
            "IsCooked": self.bCooked,
            "Size": {
                "X": self.SizeX,
                "Y": self.SizeY,
                "Z": self.SizeZ
            }
        }
