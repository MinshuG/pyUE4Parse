from enum import IntEnum
from typing import List, Tuple

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.IO.IoObjects.EIoStoreTocReadOptions import EIoStoreTocReadOptions
from UE4Parse.IO.IoObjects.FFileIoStoreContainerFile import EIoContainerFlags
from UE4Parse.IO.IoObjects.FIoChunkId import FIoChunkId
from UE4Parse.IO.IoObjects.FIoOffsetAndLength import FIoOffsetAndLength
from UE4Parse.IO.IoObjects.FIoStoreTocCompressedBlockEntry import FIoStoreTocCompressedBlockEntry
from UE4Parse.IO.IoObjects.FIoStoreTocEntryMeta import FIoStoreTocEntryMeta
from UE4Parse.IO.IoObjects.FIoStoreTocHeader import FIoStoreTocHeader, EIoStoreTocVersion
from UE4Parse.PakFile.PakObjects.FSHAHash import FSHAHash


class EIoStoreTocReadOptions(IntEnum):
    Default = 0
    ReadDirectoryIndex = 1 << 0
    ReadTocMeta = 1 << 1
    ReadAll = ReadDirectoryIndex | ReadTocMeta


class FIoStoreTocResource:
    Header: FIoStoreTocHeader
    ChunkIds: Tuple[FIoChunkId]
    ChunkOffsetLengths: Tuple[FIoOffsetAndLength]
    CompressionBlocks: Tuple[FIoStoreTocCompressedBlockEntry]
    CompressionMethods: Tuple[str]
    ChunkBlockSignatures: Tuple[FSHAHash]
    DirectoryIndexBuffer: bytes = b""
    ChunkMetas: Tuple[FIoStoreTocEntryMeta]

    def __init__(self, tocStream: BinaryStream, readOptions: EIoStoreTocReadOptions = EIoStoreTocReadOptions.Default):
        reader = tocStream
        self.Header = FIoStoreTocHeader(reader)
        reader.seek(self.Header.TocHeaderSize, 0)

        # total_toc_size = reader.size - self.Header.TocHeaderSize
        # toc_meta_size = self.Header.TocEntryCount * FIoStoreTocEntryMeta.SIZE
        # default_toc_size = total_toc_size - self.Header.DirectoryIndexSize - toc_meta_size
        # toc_size = default_toc_size
        # if readOptions.value == EIoStoreTocReadOptions.ReadTocMeta.value:
        #     toc_size = total_toc_size
        # elif readOptions.value == EIoStoreTocReadOptions.ReadDirectoryIndex.value:
        #     toc_size = default_toc_size + self.Header.DirectoryIndexSize

        self.ChunkIds = tuple(FIoChunkId(reader) for x in range(self.Header.TocEntryCount))
        
        self.ChunkOffsetLengths = tuple([FIoOffsetAndLength(reader) for x in range(self.Header.TocEntryCount)])

        self.CompressionBlocks = tuple(FIoStoreTocCompressedBlockEntry(reader) for x in range(self.Header.TocCompressedBlockEntryCount))  # can this be optimized more?

        self.CompressionMethods = tuple(reader.readBytes(self.Header.CompressionMethodNameLength).rstrip(b'\x00').decode("utf-8") for x in range(self.Header.CompressionMethodNameCount))

        self.ChunkBlockSignatures = ()
        isSigned = self.Header.ContainerFlags & (1 << 2) != 0
        if isSigned:
            hash_size = reader.readInt32()
            reader.seek(hash_size * 2)  # hash

            self.ChunkBlockSignatures = tuple(FSHAHash(reader) for x in range(self.Header.TocCompressedBlockEntryCount))

        # Directory index
        if any([self.Header.Version.value >= EIoStoreTocVersion.DirectoryIndex.value,  # probably
               readOptions.value == EIoStoreTocReadOptions.ReadDirectoryIndex.value,
               self.Header.ContainerFlags == EIoContainerFlags.Indexed,
               self.Header.DirectoryIndexSize > 0]):
            self.DirectoryIndexBuffer = reader.readBytes(self.Header.DirectoryIndexSize)

        if readOptions == EIoStoreTocReadOptions.ReadTocMeta:
            self.ChunkMetas = tuple(FIoStoreTocEntryMeta(reader) for x in range(self.Header.TocEntryCount))
