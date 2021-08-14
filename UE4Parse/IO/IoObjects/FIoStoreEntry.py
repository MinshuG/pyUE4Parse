from typing import TYPE_CHECKING

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Provider.Common import GameFile

if TYPE_CHECKING:
    from UE4Parse.IO.IoObjects.FIoChunkId import FIoChunkId
    from UE4Parse.IO.IoObjects.FIoOffsetAndLength import FIoOffsetAndLength


class FIoStoreEntry(GameFile):
    Container = None  # FFileIoStoreReader
    UserData: int
    Name: str
    Size: int = -1
    CompressionMethodIndex: int

    Encrypted: bool = False
    ChunkId: 'FIoChunkId'
    OffsetLength: 'FIoOffsetAndLength'

    def CompressionMethodString(self) -> str:
        return "COMPRESS_" + self.Container.TocResource.CompressionMethods[
            self.CompressionMethodIndex - 1] if self.CompressionMethodIndex > 0 else "COMPRESS_None"

    @property
    def Offset(self) -> int:
        return self.OffsetLength.GetOffset

    @property
    def Length(self) -> int:
        return self.OffsetLength.GetLength

    @property
    def ContainerName(self) -> str:
        return self.Container.FileName[:-5] + ".utoc"

    @property
    def Encrypted(self) -> bool:
        return self.Container.TocResource.Header.is_encrypted()

    @property
    def OffsetLength(self) -> 'FIoOffsetAndLength':
        return self.Container.Toc[self.ChunkId]

    @property
    def ChunkId(self) -> 'FIoChunkId':
        return self.Container.TocResource.ChunkIds[self._userdata]

    def __init__(self, io_store, userdata: int, name: str):
        super().__init__()
        self.Container = io_store
        self._userdata = userdata

        self.Name = name.lower() if io_store.caseinSensitive else name

        # compressionBlockSize = ioStore.TocResource.Header.CompressionBlockSize
        # firstBlockIndex = int(self.Offset / compressionBlockSize) - 1
        # lastBlockIndex = int((Align(self.Offset + self.Length, compressionBlockSize) - 1) / compressionBlockSize)

        # for i in range(firstBlockIndex, lastBlockIndex):
        #     compressionBlock = ioStore.TocResource.CompressionBlocks[i]
        #     self.UncompressedSize += compressionBlock.UncompressedSize
        #     self.CompressionMethodIndex = compressionBlock.CompressionMethodIndex
        #
        #     rawSize = Align(compressionBlock.CompressedSize, 16)
        #     self.Size += rawSize
        #
        #     if ioStore.TocResource.Header.is_encrypted():
        #         self.Encrypted = True

    def get_data(self) -> BinaryStream:
        return self.Container.Read(self.ChunkId)
