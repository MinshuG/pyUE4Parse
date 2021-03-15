from UE4Parse.BinaryReader import BinaryStream
from UE4Parse import PropertyTagData


class LazyObjectProperty:
    Value: PropertyTagData.SoftObjectProperty

    def __init__(self, reader: BinaryStream, readType):

        self.Value = PropertyTagData.SoftObjectProperty(reader, readType)

    def GetValue(self):
        return self.Value.GetValue()