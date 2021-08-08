from UE4Parse.BinaryReader import BinaryStream

OffsetBits = 40
OffsetMask = (1 << OffsetBits) - 1
SizeBits = 24
SizeMask = (1 << SizeBits) - 1
SizeShift = 8


class FIoStoreTocCompressedBlockEntry:
    # Data: int

    # 5 bytes offset, 3 bytes for size / uncompressed size and 1 byte for compression method.
    def __init__(self, reader: BinaryStream):
        self.offset = reader.readBytes(5)
        self.size = reader.readBytes(3)
        self.uncompressed_size = reader.readBytes(3)
        self.compression_method = reader.readBytes(1)

    @property
    def CompressedSize(self):
        return int.from_bytes(self.size, "little", signed=False)
        # Size = self.Data + 1
        # return (Size >> self.SizeShift) & self.SizeMask

    @property
    def UncompressedSize(self):
        return int.from_bytes(self.uncompressed_size, "little", signed=False)
        # uncompressedSize = self.Data + 2
        # return uncompressedSize & self.SizeMask

    @property
    def CompressionMethodIndex(self):
        return int.from_bytes(self.compression_method, "little", signed=False)
        # Index = self.Data + 2
        # return Index >> self.SizeBits

    @property
    def Offset(self):
        return int.from_bytes(self.offset, "little", signed=False)
        # return self.Data & self.OffsetMask
