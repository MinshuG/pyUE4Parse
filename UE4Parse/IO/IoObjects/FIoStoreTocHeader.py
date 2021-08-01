from enum import IntEnum, auto

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Exceptions import Exceptions
from UE4Parse.IO.IoObjects.FFileIoStoreContainerFile import EIoContainerFlags
from UE4Parse.Assets.Objects.FGuid import FGuid


class EIoStoreTocVersion(IntEnum):
    Invalid = 0
    Initial = auto()
    DirectoryIndex = auto()
    PartitionSize = auto()
    LatestPlusOne = auto()
    Latest = LatestPlusOne - 1


class FIoContainerId:
    Id: int

    def __init__(self, reader: BinaryStream):
        self.Id = reader.readUInt64()


class FIoStoreTocHeader:
    _TocMagic = "-==--==--==--==-"
    Version: EIoStoreTocVersion
    Reserved0: bytes
    Reserved1: bytes
    TocHeaderSize: int
    TocEntryCount: int
    TocCompressedBlockEntryCount: int
    TocCompressedBlockEntrySize: int
    CompressionMethodNameCount: int
    CompressionMethodNameLength: int
    CompressionBlockSize: int
    DirectoryIndexSize: int
    PartitionCount: int
    ContainerId: FIoContainerId
    EncryptionKeyGuid: FGuid
    ContainerFlags: int
    Reserved3: bytes
    Reserved4: int
    Reserved5: int
    PartitionSize: int

    def __init__(self, reader: BinaryStream):
        magic = reader.readBytes(16)
        if magic != bytes(self._TocMagic, "utf-8"):
            raise Exceptions.InvalidMagic("invalid utoc magic")

        self.Version = EIoStoreTocVersion(reader.readByteToInt())
        self.Reserved0 = reader.readByte()
        self.Reserved1 = reader.readUInt16()
        self.TocHeaderSize = reader.readUInt32()
        self.TocEntryCount = reader.readUInt32()
        self.TocCompressedBlockEntryCount = reader.readUInt32()
        self.TocCompressedBlockEntrySize = reader.readUInt32()
        self.CompressionMethodNameCount = reader.readUInt32()
        self.CompressionMethodNameLength = reader.readUInt32()
        self.CompressionBlockSize = reader.readUInt32()
        self.DirectoryIndexSize = reader.readUInt32()
        self.PartitionCount = reader.readUInt32()
        self.ContainerId = FIoContainerId(reader)
        self.EncryptionKeyGuid = FGuid(reader)
        self.ContainerFlags = reader.readByteToInt()
        try:
            self.ContainerFlags = EIoContainerFlags(self.ContainerFlags).value
        except: pass
        self.Reserved3 = reader.readByteToInt()
        self.Reserved4 = reader.readUInt16()
        self.Reserved5 = reader.readUInt32()
        self.PartitionSize = reader.readUInt64()

    def is_encrypted(self) -> bool:
        return self.ContainerFlags & (1 << 1) != 0

    def is_signed(self) -> bool:
        return self.ContainerFlags & (1 << 2) != 0