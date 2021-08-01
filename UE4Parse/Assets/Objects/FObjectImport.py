from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Assets.Objects.FName import FName
from UE4Parse.Assets.Objects.FPackageIndex import FPackageIndex


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

    def __str__(self):
        return self.ObjectName.GetValue()

    def GetValue(self):
        return {
            "ClassPackage": self.ClassPackage.GetValue(),
            "ClassName": self.ClassName.GetValue(),
            "OuterIndex": self.OuterIndex.GetValue(),
            "ObjectName": self.ObjectName.GetValue()
        }
