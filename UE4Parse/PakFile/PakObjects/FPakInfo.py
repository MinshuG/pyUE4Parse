from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Objects.FGuid import FGuid
from UE4Parse.PakFile.PakObjects.EPakVersion import EPakVersion
from UE4Parse.PakFile.PakObjects.FSHAHash import FSHAHash


class PakInfo:
    PAK_FILE_MAGIC = 0x5A6F12E1
    COMPRESSION_METHOD_NAME_LEN = 32
    Version: EPakVersion = None
    SubVersion: int = None
    IndexOffset = None
    IndexSize = None
    IndexHash: FSHAHash = None
    bEncryptedIndex: bool = None
    EncryptionKeyGuid: FGuid = None
    CompressionMethods = None

    _SIZE = 4 * 2 + 8 * 2 + 20 + 1 + 16  # 61
    _SIZE8 = _SIZE + 4 * 32  # 189
    _SIZE8A = _SIZE8 + 32  # 221
    _SIZE9 = _SIZE8A + 1  # 222

    def __init__(self, reader: BinaryStream, FileSize: int) -> None:
        self.reader = reader
        Offsets_to_Try = [self._SIZE, self._SIZE8, self._SIZE8A, self._SIZE9]

        for Offset in Offsets_to_Try:
            if FileSize - Offset > 0:
                self.reader.seek(FileSize - Offset, 0)
                info = self.Info(self.reader, Offset)
                if info.Version != EPakVersion.INVALID:
                    return

        raise RuntimeError(f"Unknown Pak Format")

    def Info(self, reader: BinaryStream, offset):
        self.EncryptionKeyGuid = FGuid(reader).read()
        self.bEncryptedIndex = reader.readByte() != b'\x00'

        magic = reader.readUInt32()
        if magic != self.PAK_FILE_MAGIC:
            self.Version = EPakVersion.INVALID
            self.SubVersion = 0
            self.IndexOffset = 0
            self.IndexSize = 0
            self.IndexHash = FSHAHash
            self.CompressionMethods = None
            return self

        self.Version = EPakVersion(reader.readInt32())

        # FGame.Version = self.Version
        # FGame.SubVersion = self.SubVersion

        self.SubVersion = 1 if offset == self._SIZE8A and self.Version == EPakVersion.FNAME_BASED_COMPRESSION_METHOD else 0
        self.IndexOffset = reader.readInt64()
        self.IndexSize = reader.readInt64()
        self.IndexHash = FSHAHash(reader)
        if self.Version == EPakVersion.FROZEN_INDEX:
            reader.readByte()  # bIndexIsFrozen

        if self.Version.value < EPakVersion.FNAME_BASED_COMPRESSION_METHOD.value:
            self.CompressionMethods = ["Zlib", "Gzip", "Oodle"]
        else:
            BufferSize: int = self.COMPRESSION_METHOD_NAME_LEN * 4
            Methods: bytes = reader.readBytes(BufferSize)
            MethodList = []
            for i in range(4):
                if int(Methods[i * self.COMPRESSION_METHOD_NAME_LEN]) != 0:
                    methods = Methods
                    byteIndex = i * self.COMPRESSION_METHOD_NAME_LEN
                    byteCount = self.COMPRESSION_METHOD_NAME_LEN

                    decoded = methods[byteIndex:byteCount].decode("utf-8")

                    MethodList.append(decoded)
            self.CompressionMethods = MethodList

        if self.Version.value < EPakVersion.INDEX_ENCRYPTION.value:
            self.bEncryptedIndex = False
        if self.Version.value < EPakVersion.ENCRYPTION_KEY_GUID.value:
            raise NotImplementedError("Encrypted Index pak")
            # EncryptionKeyGuid = FGuid(0u, 0u, 0u, 0u)

        return self
