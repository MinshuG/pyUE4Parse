from UE4Parse.BinaryReader import BinaryStream


def concat(*args):
    s = ""
    for a in args:
        for b in a:
            s += str(b)
    c = int(s)
    return c


def toint(byte) -> int:
    return int.from_bytes(byte, "little", signed=False)


class FIoStoreTocCompressedBlockEntry:
    OffsetBits = 40
    OffsetMask = (1 << OffsetBits) - 1
    SizeBits = 24
    SizeMask = (1 << SizeBits) - 1
    SizeShift = 8
    # Data: int

    # 5 bytes offset, 3 bytes for size / uncompressed size and 1 byte for compression method.
    def __init__(self, reader: BinaryStream):
        self.offset = reader.readBytes(5)
        self.size = reader.readBytes(3)
        self.uncompressed_size = reader.readBytes(3)
        self.compression_method = reader.readBytes(1)
        # data = concat(offset, size, uncompressed_size, compression_method)

    @property
    def CompressedSize(self):
        return toint(self.size)
        # Size = self.Data + 1
        # return (Size >> self.SizeShift) & self.SizeMask

    @property
    def UncompressedSize(self):
        return toint(self.uncompressed_size)
        # uncompressedSize = self.Data + 2
        # return uncompressedSize & self.SizeMask

    @property
    def CompressionMethodIndex(self):
        return toint(self.compression_method)
        # Index = self.Data + 2
        # return Index >> self.SizeBits

    @property
    def Offset(self):
        return toint(self.offset)
        # return self.Data & self.OffsetMask
