from UE4Parse.Assets.Objects.FGuid import FGuid
import io
import os
import time
from typing import Dict, Optional

from UE4Parse import Logger
from UE4Parse.BinaryReader import BinaryStream, Align
from UE4Parse.Encryption import FAESKey
from UE4Parse.Exceptions.Exceptions import InvalidEncryptionKey
from UE4Parse.IO.IoObjects.EIoStoreTocReadOptions import EIoStoreTocReadOptions
from UE4Parse.IO.IoObjects.FFileIoStoreContainerFile import FFileIoStoreContainerFile
from UE4Parse.IO.IoObjects.FIoChunkId import FIoChunkId
from UE4Parse.IO.IoObjects.FIoDirectoryIndexHandle import FIoDirectoryIndexHandle
from UE4Parse.IO.IoObjects.FIoDirectoryIndexResource import FIoDirectoryIndexResource
from UE4Parse.IO.IoObjects.FIoOffsetAndLength import FIoOffsetAndLength
from UE4Parse.IO.IoObjects.FIoStoreEntry import FIoStoreEntry
from UE4Parse.IO.IoObjects.FIoStoreTocHeader import FIoContainerId
from UE4Parse.IO.IoObjects.FIoStoreTocResource import FIoStoreTocResource
from UE4Parse.Assets.Objects.Decompress import Decompress


CrytoAval = True
try:
    from Crypto.Cipher import AES
except ImportError:
    CrytoAval = False

logger = Logger.get_logger(__name__)


class FFileIoStoreReader:
    FileName: str
    Directory: str
    TocResource: FIoStoreTocResource
    Toc: Dict[str, FIoOffsetAndLength]
    ContainerFile: FFileIoStoreContainerFile
    ContainerId: FIoContainerId

    _directory_index: FIoDirectoryIndexResource
    aeskey: FAESKey = None
    caseinSensitive: bool

    # @profile
    def __init__(self, dir_: str, tocStream: BinaryStream, containerStream: BinaryStream, caseinSensitive: bool = True,
                 tocReadOptions: EIoStoreTocReadOptions = EIoStoreTocReadOptions.ReadDirectoryIndex):
        """
        :param dir_:
        :param tocStream:
        :param containerStream:
        :param caseinSensitive:
        :param tocReadOptions:
        """
        self.FileName = os.path.basename(dir_)
        self.Directory = dir_
        self.caseinSensitive = caseinSensitive
        self.ContainerFile = FFileIoStoreContainerFile()
        self.ContainerFile.FileHandle = containerStream
        self.TocResource = FIoStoreTocResource(tocStream, tocReadOptions)
        conUncompressedSize = self.TocResource.Header.TocCompressedBlockEntryCount * self.TocResource.Header.CompressionBlockSize \
            if self.TocResource.Header.TocCompressedBlockEntryCount > 0 else containerStream.size

        self.Toc = {}
        for i in range(self.TocResource.Header.TocEntryCount):
            chunkOffsetLength = self.TocResource.ChunkOffsetLengths[i]
            a = chunkOffsetLength.GetOffset + chunkOffsetLength.GetLength > conUncompressedSize
            if a:
                raise Exception("TocEntry out of container bounds")
            self.Toc[self.TocResource.ChunkIds[i]] = chunkOffsetLength

        self.ContainerFile.CompressionMethods = self.TocResource.CompressionMethods
        self.ContainerFile.CompressionBlockSize = self.TocResource.Header.CompressionBlockSize
        self.ContainerFile.CompressionBlocks = self.TocResource.CompressionBlocks
        self.ContainerFile.ContainerFlags = self.TocResource.Header.ContainerFlags
        self.ContainerFile.EncryptionKeyGuid = self.TocResource.Header.EncryptionKeyGuid
        self.ContainerFile.BlockSignatureHashes = self.TocResource.ChunkBlockSignatures
        self.ContainerId = self.TocResource.Header.ContainerId

        self._directoryIndexBuffer = self.TocResource.DirectoryIndexBuffer  # TODO no
        # del self.TocResource.ChunkIds

    def get_encryption_key_guid(self) -> FGuid:
        return self.TocResource.Header.EncryptionKeyGuid

    def get_mount_point(self):
        return self.ContainerFile.MountPoint

    @property
    def IsValidIndex(self):
        return len(self._directory_index.DirectoryEntries) > 0

    @property
    def HasDirectoryIndex(self):
        return len(self.TocResource.DirectoryIndexBuffer) != 0

    @property
    def IsEncrypted(self):
        return self.TocResource.Header.is_encrypted()

    # @profile
    def ReadDirectoryIndex(self, key: Optional[FAESKey] = None):
        self.aeskey = key
        starttime = time.time()
        if self.HasDirectoryIndex:
            if not self.IsEncrypted:
                IndexReader = BinaryStream(io.BytesIO(self._directoryIndexBuffer), len(self._directoryIndexBuffer))
            else:
                if not CrytoAval:
                    raise ImportError(
                        "Failed to Import \"pycryptodome\", Index is Encrypted it is required for decryption.")
                if self.aeskey is None:
                    raise InvalidEncryptionKey("Index is Encrypted and Key was not provided.")

                IndexReader = BinaryStream(io.BytesIO(self.aeskey.decrypt(self._directoryIndexBuffer)),
                                           len(self._directoryIndexBuffer))

                stringLen = IndexReader.readInt32()
                if stringLen > 512 or stringLen < -512:
                    raise ValueError(f"Provided key didn't work with {self.FileName}")
                if stringLen < 0:
                    IndexReader.base_stream.seek((stringLen - 1) * 2, 1)
                    if IndexReader.readUInt16() != 0:
                        raise ValueError(f"Provided key didn't work with {self.FileName}")
                else:
                    IndexReader.base_stream.seek(stringLen - 1, 1)
                    if int.from_bytes(IndexReader.readByte(), "little") != 0:
                        raise ValueError(f"Provided key didn't work with {self.FileName}")
                IndexReader.seek(0, 0)
            del self.TocResource.DirectoryIndexBuffer
            del self._directoryIndexBuffer

            self._directory_index = FIoDirectoryIndexResource(IndexReader, self.caseinSensitive)
            self.ContainerFile.MountPoint = self._directory_index.MountPoint
            firstEntry = self.GetChildDirectory(FIoDirectoryIndexHandle(FIoDirectoryIndexHandle.Root))

            tempFiles: Dict[str, FIoStoreEntry]
            Chunks: Dict[str, str]
            tempFiles, Chunks = self.ReadIndex("", firstEntry)  # TODO use Chunks IDs

            time_taken = round(time.time() - starttime, 2)
            logger.info("{} contains {} files, mount point: {}, version: {}, in: {}s".format
                        (self.FileName, len(tempFiles), self._directory_index.MountPoint, self.TocResource.Header.Version, time_taken))

            del self._directory_index
            return tempFiles, Chunks

    def GetChildDirectory(self, directory: FIoDirectoryIndexHandle):
        return FIoDirectoryIndexHandle(
            self.GetDirectoryEntry(directory).FirstChildEntry) if directory.isValid() else FIoDirectoryIndexHandle()

    def GetNextDirectory(self, directory: FIoDirectoryIndexHandle):
        if directory.isValid() and self.IsValidIndex:
            return FIoDirectoryIndexHandle(self.GetDirectoryEntry(directory).NextSiblingEntry)
        else:
            return FIoDirectoryIndexHandle()

    def GetFile(self, directory: FIoDirectoryIndexHandle):
        if directory.isValid() and self.IsValidIndex:
            return FIoDirectoryIndexHandle(self.GetDirectoryEntry(directory).FirstFileEntry)

    def GetNextFile(self, file: FIoDirectoryIndexHandle):
        if file.isValid() and self.IsValidIndex:
            return FIoDirectoryIndexHandle(self.GetFileEntry(file).NextFileEntry)

    def GetDirectoryName(self, directory: FIoDirectoryIndexHandle):
        if directory.isValid() and self.IsValidIndex:
            index = self.GetDirectoryEntry(directory).Name
            return self._directory_index.StringTable[index]

    def GetFileName(self, file: FIoDirectoryIndexHandle):
        if file.isValid() and self.IsValidIndex:
            index = self.GetFileEntry(file).Name
            return self._directory_index.StringTable[index]

    def GetFileData(self, file: FIoDirectoryIndexHandle):
        if file.isValid() and self.IsValidIndex:
            return self._directory_index.FileEntries[file.ToIndex()].UserData
        else:
            return 0

    def GetDirectoryEntry(self, directory: FIoDirectoryIndexHandle):
        return self._directory_index.DirectoryEntries[directory.ToIndex()]

    def GetFileEntry(self, file: FIoDirectoryIndexHandle):
        return self._directory_index.FileEntries[file.ToIndex()]

    def ReadIndex(self, directoryName: str, dir: FIoDirectoryIndexHandle):
        outfile = {}
        outchunk = {}
        while dir.isValid():
            sub_dir_name = f"{directoryName}{self.GetDirectoryName(dir)}/"
            file = self.GetFile(dir)
            while file.isValid():
                name = self.GetFileName(file)
                path = sub_dir_name + name  # self._directory_index.MountPoint +
                data = self.GetFileData(file)  # UseData
                entry = FIoStoreEntry(self, data, path)
                outchunk[entry.ChunkId] = path
                outfile[path] = entry
                file = self.GetNextFile(file)

            childoutfile, childoutchunk = self.ReadIndex(sub_dir_name, self.GetChildDirectory(dir), )
            outfile.update(childoutfile)
            outchunk.update(childoutchunk)
            dir = self.GetNextDirectory(dir)

        return outfile, outchunk
 
    def Read(self, chunkid: FIoChunkId) -> BinaryStream:
        offsetAndLength: FIoOffsetAndLength = self.Toc[chunkid]
        compressionBlockSize = self.TocResource.Header.CompressionBlockSize
        firstBlockIndex = int(offsetAndLength.GetOffset / compressionBlockSize)
        lastBlockIndex = int((Align(offsetAndLength.GetOffset + offsetAndLength.GetLength,
                                    compressionBlockSize) - 1) / compressionBlockSize)
        offsetInBlock = int(offsetAndLength.GetOffset % compressionBlockSize)

        remaining_size = offsetAndLength.GetLength
        containerStream = self.ContainerFile.FileHandle
        dst: bytes = b""
        # i = firstBlockIndex # BlockIndex
        for i in range(firstBlockIndex,
                       lastBlockIndex + 1):  # if firstBlockIndex == lastBlockIndex: lastBlockIndex -= 1 ??
            compressionBlock = self.TocResource.CompressionBlocks[i]
            rawSize = Align(compressionBlock.CompressedSize, AES.block_size)
            uncompressedSize = compressionBlock.UncompressedSize

            containerStream.seek(compressionBlock.Offset, 0)
            compressedBuffer: bytes = containerStream.readBytes(rawSize)

            if self.TocResource.Header.is_encrypted():
                compressedBuffer = self.aeskey.decrypt(compressedBuffer)

            src: bytes
            if compressionBlock.CompressionMethodIndex == 0:
                src = compressedBuffer
            else:
                compressionMethod = self.TocResource.CompressionMethods[compressionBlock.CompressionMethodIndex - 1]
                src = Decompress(compressedBuffer, compressionMethod, uncompressedSize)

            sizeInBlock = int(min(compressionBlockSize - offsetInBlock, remaining_size))
            dst += src[offsetInBlock:offsetInBlock + sizeInBlock]
            remaining_size -= sizeInBlock

        result = BinaryStream(dst)
        return result

    def DoesChunkExist(self, ChunkId: FIoChunkId):
        return ChunkId in self.Toc


if __name__ == "__main__":
        cas = r"C:\Program Files\Epic Games\Fortnite\FortniteGame\Content\Paks\pakchunk10_s15-WindowsClient.ucas"
        toc = r"C:\Program Files\Epic Games\Fortnite\FortniteGame\Content\Paks\pakchunk10_s15-WindowsClient.utoc"
        FFileIoStoreReader(cas, BinaryStream(toc), BinaryStream(cas)).ReadDirectoryIndex()
