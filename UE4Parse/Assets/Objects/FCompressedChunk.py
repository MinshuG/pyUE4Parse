from UE4Parse.BinaryReader import BinaryStream


class FCompressedChunk:
    def __init__(self, reader: BinaryStream) -> None:
        self.CompressedSize = self.readInt32()
        self.CompressedOffset = self.readInt32()
        self.UncompressedSize = self.readInt32()
        self.UncompressedOffset = self.readInt32()

