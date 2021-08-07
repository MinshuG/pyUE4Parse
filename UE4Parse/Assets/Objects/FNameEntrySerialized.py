# from UE4Parse.BinaryReader import BinaryStream # circular

from UE4Parse.Versions.EUnrealEngineObjectUE4Version import EUnrealEngineObjectUE4Version


class FSerializedNameHeader:
    data: bytearray = bytearray()

    @property
    def IsUtf16(self):
        return (self.data[0] & 0x80) != 0

    def __len__(self):
        return ((self.data[0] & 0x7F) << 8) + self.data[1]

    def __init__(self, reader):
        self.data = bytearray(reader.readBytes(2))


class FNameEntrySerialized:
    Name: str

    def __init__(self, reader=None):
        if reader is None:
            return
        if isinstance(reader, str):
            self.Name = reader
            return

        self.Name = reader.readFString()
        if not reader.PackageReader.PackageFileSummary.FileVersionUE4.value >= EUnrealEngineObjectUE4Version.VER_UE4_NAME_HASHES_SERIALIZED.value:
            reader.seek(4)

    @staticmethod
    def LoadNameBatch(outNames: list, outHashes: list, namereader, hashreader):
        hashDataIt = hashreader.readUInt64()
        hashCount = int(hashreader.size / 8 - 1)

        for _ in range(hashCount):
            outHashes.append(hashreader.readUInt64())
            outNames.append(FNameEntrySerialized.LoadNameHeader(namereader))

    @staticmethod
    def LoadNameHeader(reader):
        header = FSerializedNameHeader(reader)

        length = len(header)
        if header.IsUtf16:
            utfdata = reader.readBytes(length * 2)
            return FNameEntrySerialized(utfdata.decode("utf-8"))
        else:
            return FNameEntrySerialized(reader.readBytes(length).decode("utf-8"))

    def __str__(self):
        return self.Name
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(Name={self.Name})"

    def GetValue(self):
        return self.Name
