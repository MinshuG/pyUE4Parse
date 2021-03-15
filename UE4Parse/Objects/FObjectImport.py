from UE4Parse.Objects.FName import FName
from UE4Parse.Objects.FPackageIndex import FPackageIndex
from UE4Parse.BinaryReader import BinaryStream


class FObjectImport:
    ClassPackage: FName
    ClassName: FName
    OuterIndex: FPackageIndex
    ObjectName: FName

    def __init__(self, reader: BinaryStream) -> None:
        self.ClassPackage = reader.readFName()
        self.ClassName = reader.readFName()
        self.OuterIndex = FPackageIndex(reader)
        self.ObjectName = reader.readFName()
