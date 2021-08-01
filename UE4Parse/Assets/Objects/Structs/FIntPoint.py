from UE4Parse.BinaryReader import BinaryStream


class FIntPoint:
    position: int
    X: int
    Y: int

    def __init__(self, reader: BinaryStream) -> None:
        self.position = reader.base_stream.tell()
        self.X = reader.readInt32()
        self.Y = reader.readInt32()

    def GetValue(self):
        return {
            "X": self.X,
            "Y": self.Y
        }
