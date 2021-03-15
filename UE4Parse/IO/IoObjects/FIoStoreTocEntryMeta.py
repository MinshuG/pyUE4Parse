from enum import Enum

from UE4Parse.BinaryReader import BinaryStream


class FIoStoreTocEntryMetaFlags(Enum):
    _None = 0
    Compressed = (1 << 0)
    MemoryMapped = (1 << 1)


class FIoChunkHash(object):
    Hash: bytes

    def __init__(self, reader: BinaryStream):
        self.Hash = reader.readBytes(32)


class FIoStoreTocEntryMeta:
    SIZE = 32 + 4

    ChunkHash: FIoChunkHash
    Flags: FIoStoreTocEntryMetaFlags

    def __init__(self, reader: BinaryStream):
        self.ChunkHash = FIoChunkHash(reader)
        self.Flags = FIoStoreTocEntryMetaFlags(reader.readByteToInt())
