from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.IoObjects.FMinimalName import FMinimalName
from UE4Parse.IoObjects.FPackageObjectIndex import FPackageObjectIndex


class FScriptObjectEntry:
    ObjectName: FMinimalName
    GlobalIndex: FPackageObjectIndex
    OuterIndex: FPackageObjectIndex
    CDOClassIndex: FPackageObjectIndex

    def __init__(self, reader: BinaryStream, nameMap):
        self.ObjectName = FMinimalName(reader, nameMap)
        self.GlobalIndex = FPackageObjectIndex(reader)
        self.OuterIndex = FPackageObjectIndex(reader)
        self.CDOClassIndex = FPackageObjectIndex(reader)
