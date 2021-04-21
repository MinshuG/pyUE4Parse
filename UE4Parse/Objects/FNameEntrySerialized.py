# from UE4Parse.BinaryReader import BinaryStream # circular
from UE4Parse.Objects.EUnrealEngineObjectUE4Version import EUnrealEngineObjectUE4Version


class FNameEntrySerialized:
    Name: str

    def __init__(self, reader):
        self.Name = reader.readFString()
        if not reader.PackageReader.PackageFileSummary.FileVersionUE4.value >= EUnrealEngineObjectUE4Version.VER_UE4_NAME_HASHES_SERIALIZED.value:
            reader.seek(4)

    def __str__(self):
        return self.Name

    def GetValue(self):
        return self.Name
