from enum import Enum
from typing import List

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.IO.IoObjects.FIoStoreTocCompressedBlockEntry import FIoStoreTocCompressedBlockEntry
from UE4Parse.Assets.Objects.FGuid import FGuid
from UE4Parse.PakFile.PakObjects.FSHAHash import FSHAHash


class EIoContainerFlags(Enum):
    _None = 0
    Compressed = (1 << 0)
    Encrypted = (1 << 1)
    Signed = (1 << 2)
    Indexed = (1 << 3)


class FFileIoStoreContainerFile:
    FileHandle: BinaryStream
    CompressionBlockSize: int
    CompressionMethods: List[str]
    CompressionBlocks: List[FIoStoreTocCompressedBlockEntry]
    EncryptionKeyGuid: FGuid
    EncryptionKey: bytes
    ContainerFlags: EIoContainerFlags
    BlockSignatureHashes: FSHAHash
    MountPoint: str

