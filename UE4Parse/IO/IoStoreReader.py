from UE4Parse.Assets.Objects.FGuid import FGuid
import io
import os
import time
from typing import Callable, Dict, Optional

from UE4Parse import Logger
from UE4Parse.BinaryReader import BinaryStream, Align
from UE4Parse.Encryption import FAESKey
from UE4Parse.Exceptions.Exceptions import InvalidEncryptionKey
from UE4Parse.IO.IoObjects.EIoStoreTocReadOptions import EIoStoreTocReadOptions
from UE4Parse.IO.IoObjects.FFileIoStoreContainerFile import FFileIoStoreContainerFile
from UE4Parse.IO.IoObjects.FIoChunkId import FIoChunkId
from UE4Parse.IO.IoObjects.FIoContainerHeader import FIoContainerHeader
from UE4Parse.IO.IoObjects.FIoDirectoryIndexHandle import FIoDirectoryIndexHandle
from UE4Parse.IO.IoObjects.FIoDirectoryIndexResource import FIoDirectoryIndexResource
from UE4Parse.IO.IoObjects.FIoOffsetAndLength import FIoOffsetAndLength
from UE4Parse.IO.IoObjects.FIoStoreEntry import FIoStoreEntry
from UE4Parse.IO.IoObjects.FIoStoreTocHeader import FIoContainerId
from UE4Parse.IO.IoObjects.FIoStoreTocResource import FIoStoreTocResource
from UE4Parse.Assets.Objects.Decompress import Decompress
from UE4Parse.IoObjects.EIoChunkType import EIoChunkType5
from UE4Parse.Versions import EUEVersion

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
    Toc: Dict[FIoChunkId, FIoOffsetAndLength]
    ContainerFile: FFileIoStoreContainerFile
    ContainerId: FIoContainerId
    ContainerHeader: Optional[FIoContainerHeader]

    _directory_index: FIoDirectoryIndexResource
    aeskey: FAESKey = None
    caseinSensitive: bool
    _ue_version: EUEVersion

    def __init__(self, dir_: str, tocStream: BinaryStream, streamOpenFunc: Callable[[int], BinaryStream], ue_version: EUEVersion, caseinSensitive: bool = True,
                 tocReadOptions: EIoStoreTocReadOptions = EIoStoreTocReadOptions.ReadDirectoryIndex):
        """
        :param dir_:
        :param tocStream:
        :param streamOpenFunc:
        :param caseinSensitive:
        :param tocReadOptions:
        """
        self.FileName = os.path.basename(dir_)

        self.Directory = dir_
        self.caseinSensitive = caseinSensitive
        self.ContainerFile = FFileIoStoreContainerFile()
        
        self.TocResource = FIoStoreTocResource(tocStream, tocReadOptions)
        tocStream.close()

        containerStreams: BinaryStream = []
        if self.TocResource.Header.PartitionCount <= 1:
            containerStreams.append(streamOpenFunc(dir_.replace(".utoc", ".ucas")))
        else:
            for i in range(self.TocResource.Header.PartitionCount):
                name = dir_.replace(".utoc", f"_s{i}.ucas") if i > 0 else dir_.replace(".utoc", ".ucas")
                containerStreams.append(streamOpenFunc(name))

        self.ContainerFile.FileHandles = containerStreams
        self._ue_version = ue_version

        self.Toc = {}
        for i in range(self.TocResource.Header.TocEntryCount):
            chunkOffsetLength = self.TocResource.ChunkOffsetLengths[i]
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
        if self.HasDirectoryIndex:
            self.ContainerHeader = self.ReadContainerHeader()
        else:
            self.ContainerHeader = None

    def get_encryption_key_guid(self) -> FGuid:
        return self.TocResource.Header.EncryptionKeyGuid

    def get_mount_point(self):
        return self.ContainerFile.MountPoint

    def close(self):
        self.ContainerFile.FileHandle.close()

    @property
    def IsValidIndex(self):
        return len(self._directory_index.DirectoryEntries) > 0

    @property
    def HasDirectoryIndex(self):
        return len(self.TocResource.DirectoryIndexBuffer) != 0

    @property
    def IsEncrypted(self):
        return self.TocResource.Header.is_encrypted()

    def ReadContainerHeader(self):
        if self._ue_version >= EUEVersion.GAME_UE5_0:
            headerChunkId = FIoChunkId().construct(self.TocResource.Header.ContainerId.Id, 0,
                                                   EIoChunkType5.ContainerHeader)
            reader = self.Read(headerChunkId)
            return FIoContainerHeader(reader, self._ue_version)

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

                string_len = IndexReader.readInt32()
                if string_len > 512 or string_len < -512:
                    raise InvalidEncryptionKey(f"Provided key didn't work with {self.FileName}")
                if string_len < 0:
                    IndexReader.base_stream.seek((string_len - 1) * 2, 1)
                    if IndexReader.readUInt16() != 0:
                        raise InvalidEncryptionKey(f"Provided key didn't work with {self.FileName}")
                else:
                    IndexReader.base_stream.seek(string_len - 1, 1)
                    if int.from_bytes(IndexReader.readByte(), "little") != 0:
                        raise InvalidEncryptionKey(f"Provided key didn't work with {self.FileName}")
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
                data = self.GetFileData(file)  # UserData
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
        dst: bytes = b""
        # i = firstBlockIndex # BlockIndex
        for i in range(firstBlockIndex,
                       lastBlockIndex + 1):  # if firstBlockIndex == lastBlockIndex: lastBlockIndex -= 1 ??
            compressionBlock = self.TocResource.CompressionBlocks[i]
            rawSize = Align(compressionBlock.CompressedSize, AES.block_size)
            uncompressedSize = compressionBlock.UncompressedSize

            partition_index = int(compressionBlock.Offset / self.TocResource.Header.PartitionSize)
            partition_offset = compressionBlock.Offset % self.TocResource.Header.PartitionSize
            containerStream = self.ContainerFile.FileHandles[partition_index]
            containerStream.seek(partition_offset, 0)

            compressedBuffer: bytes = containerStream.readBytes(rawSize)

            if self.TocResource.Header.is_encrypted():
                if self.aeskey is None:
                    raise InvalidEncryptionKey(f"AES key was not provided for {self.FileName}({self.get_encryption_key_guid()})")
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
