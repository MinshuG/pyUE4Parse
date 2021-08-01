from UE4Parse.BinaryReader import BinaryStream
from .SoftObjectProperty import SoftObjectProperty


class LazyObjectProperty:
    Value: SoftObjectProperty

    def __init__(self, reader: BinaryStream, readType):
        self.Value = SoftObjectProperty(reader, readType)

    def GetValue(self):
        return self.Value.GetValue()
