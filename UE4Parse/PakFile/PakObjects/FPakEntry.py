from UE4Parse.Encryption.FAESKey import FAESKey
from UE4Parse.Exceptions.Exceptions import InvalidEncryptionKey
from UE4Parse.Assets.Objects import Decompress
from typing import Tuple, TYPE_CHECKING

from UE4Parse.BinaryReader import Align, BinaryStream
from UE4Parse.PakFile import ECompressionFlags
from UE4Parse.PakFile import EPakVersion
from UE4Parse.PakFile import FPakCompressedBlock
from UE4Parse.Provider.Common import GameFile

if TYPE_CHECKING:
    from UE4Parse.PakFile.PakReader import PakReader


class FPakEntry(GameFile):
    Flags: int = 0
    Flag_Encrypted = 0x01
    Flag_Deleted = 0x02
    _Encrypted: bool = None
    _Deleted = (Flags & Flag_Deleted) != 0
    # above 5 lines are useless ?

    Container: 'PakReader'
    Name: str = ""
    Offset: int = 0
    Size: int = 0
    UncompressedSize: int = 0

    CompressionBlocks: Tuple[FPakCompressedBlock]
    CompressionBlockSize: int = 0
    CompressionMethodIndex: int

    StructSize: int

    @property
    def Deleted(self):
        return self._Deleted

    @Deleted.setter
    def Deleted(self, value):
        self._Deleted = value

    @property
    def Encrypted(self):
        return (self.Flags & self.Flag_Encrypted) != 0 if self._Encrypted is None else self._Encrypted

    @Encrypted.setter
    def Encrypted(self, value):
        self._Encrypted = value

    def __init__(self, reader: BinaryStream, Version: EPakVersion = 0, SubVersion: int = 0,
                 pak: 'PakReader' = None):
        if reader is None:
            return
        self.CompressionBlocks = ()
        self.CompressionBlockSize = 0
        self.Flags = 0

        self.Container = pak

        name = reader.readFString()
        self.Name = name[1::] if name.startswith("/") else name

        StartOffset = reader.base_stream.tell()

        self.Offset = reader.readInt64()
        self.Size = reader.readInt64()
        self.UncompressedSize = reader.readInt64()

        if Version.value > EPakVersion.FNAME_BASED_COMPRESSION_METHOD.value:
            LegacyCompressionMethod = reader.readInt32()
            if LegacyCompressionMethod == ECompressionFlags.COMPRESS_None.value:
                self.CompressionMethodIndex = 0
            else:
                raise NotImplementedError("Compression not implemented")
        else:
            if Version.value == EPakVersion.FNAME_BASED_COMPRESSION_METHOD.value and SubVersion == 0:
                self.CompressionMethodIndex = reader.readByteToInt()
            else:
                self.CompressionMethodIndex = reader.readUInt32()

        if Version.value < EPakVersion.NO_TIMESTAMPS.value:
            reader.readInt64()  # Timestamp
        reader.readBytes(20)  # hash

        if Version.value >= EPakVersion.COMPRESSION_ENCRYPTION.value:
            if self.CompressionMethodIndex != 0:
                self.CompressionBlocks = reader.readTArray(FPakCompressedBlock, reader)
            self.Flags = reader.readByteToInt()
            self.CompressionBlockSize = reader.readUInt32()

        self.StructSize = reader.base_stream.tell() - StartOffset

    def get_data(self) -> BinaryStream:
        stream: BinaryStream = self.Container.reader
        key: FAESKey = self.Container.AesKey
        compression_method = self.Container.Info.CompressionMethods
        if self.CompressionMethodIndex == 0:
            stream.seek(self.Offset + self.StructSize, 0)
            if self.Encrypted:
                return BinaryStream(key.decrypt(stream.read()))
            else:
                data: bytes = stream.readBytes(self.UncompressedSize)
                return BinaryStream(data)
        else:
            return BinaryStream(self._decompress(stream, key, compression_method))

    def _decompress(self, stream: BinaryStream, key: FAESKey, compression_methods: list):
        compression_method = compression_methods[self.CompressionMethodIndex - 1]

        result = bytearray()
        if self.Encrypted:
            if key is None:
                raise InvalidEncryptionKey("File is Encrypted and Key was not provided.")

        block: FPakCompressedBlock
        for block in self.CompressionBlocks:
            stream.seek(self.Offset + block.CompressedStart)
            uncompressed_size = min(self.CompressionBlockSize, self.UncompressedSize - len(result))

            if self.Encrypted:
                buffer = stream.read(Align(self.CompressionBlockSize, key.block_size))
                buffer = key.decrypt(buffer)
            else:
                buffer = stream.read(Align(self.CompressionBlockSize, key.block_size))  # AES.block_size

            result += Decompress.Decompress(buffer, compression_method, uncompressed_size)
        return result

    @staticmethod
    def GetSize(PakVersion: EPakVersion, compressionMethod, CompressionBlocksCount):
        serialized_size = 8 + 8 + 8 + 20
        if PakVersion.value >= EPakVersion.FNAME_BASED_COMPRESSION_METHOD.value:
            serialized_size += 4
        else:
            serialized_size += 4  # Old CompressedMethod var from pre-FName based compression methods

        if PakVersion.value >= EPakVersion.COMPRESSION_ENCRYPTION.value:
            serialized_size += 1 + 4  # isEncrypted + compressionBlockSize
            if compressionMethod != 0:
                serialized_size += 8 * 2 * CompressionBlocksCount + 4  # FPakCompressedBlock + int32

        if PakVersion.value < EPakVersion.NO_TIMESTAMPS.value:
            serialized_size += 8  # timestamp

        return serialized_size
