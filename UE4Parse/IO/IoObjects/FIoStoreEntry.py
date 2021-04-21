from UE4Parse.BinaryReader import Align
from UE4Parse.IO.IoObjects.FIoChunkId import FIoChunkId
from UE4Parse.IO.IoObjects.FIoOffsetAndLength import FIoOffsetAndLength


class FIoStoreEntry:
    ioStore = None  # FFileIoStoreReader
    UserData: int
    ContainerName: str
    Name: str
    Size: int = 0
    UncompressedSize: int = 0
    StructSize: int = 0
    CompressionMethodIndex: int

    Encrypted: bool = False
    ChunkId: FIoChunkId
    OffsetLength: FIoOffsetAndLength

    hasUbulk: bool = False
    hasUexp: bool = False

    def CompressionMethodString(self) -> str:
        return "COMPRESS_" + self.ioStore.TocResource.CompressionMethods[
            self.CompressionMethodIndex - 1] if self.CompressionMethodIndex > 0 else "COMPRESS_None"

    @property
    def Offset(self) -> int:
        return self.OffsetLength.GetOffset

    @property
    def Length(self) -> int:
        return self.OffsetLength.GetLength

    def __init__(self, ioStore, userdata: int, name: str):
        self.ioStore = ioStore

        self.ContainerName = ioStore.FileName
        self.ChunkId = ioStore.TocResource.ChunkIds[userdata]
        self.OffsetLength = ioStore.Toc[str(self.ChunkId.Id)]

        caseinSensitive = ioStore.caseinSensitive

        self.Name = name.lower() if caseinSensitive else name

        compressionBlockSize = ioStore.TocResource.Header.CompressionBlockSize
        firstBlockIndex = int(self.Offset / compressionBlockSize) - 1
        lastBlockIndex = int((Align(self.Offset + self.Length, compressionBlockSize) - 1) / compressionBlockSize)

        for i in range(firstBlockIndex, lastBlockIndex):
            compressionBlock = ioStore.TocResource.CompressionBlocks[i]
            self.UncompressedSize += compressionBlock.UncompressedSize
            self.CompressionMethodIndex = compressionBlock.CompressionMethodIndex

            rawSize = Align(compressionBlock.CompressedSize, 16)
            self.Size += rawSize

            if ioStore.TocResource.Header.is_encrypted():
                self.Encrypted = True

    def GetData(self):
        return self.ioStore.Read(self.ChunkId)
