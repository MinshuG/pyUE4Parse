from UE4Parse import PropertyTagData
from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Objects.FPropertyTag import FPropertyTag
from Usmap.Objects.FPropertyTag import FPropertyTag as usmapTag

class ArrayProperty:
    Value: list
    position: int

    def __init__(self, reader: BinaryStream, tag: FPropertyTag):
        self.position = reader.base_stream.tell()
        self.Value = self.ArrayPropertyReader(reader, tag)

    def GetValue(self):
        vals = []
        for val in self.Value:
            vals.append(val.GetValue())
        return vals

    def ArrayPropertyReader(self, reader: BinaryStream, tag) -> list:
        InnerType = tag.InnerType

        length = reader.readInt32()
        Value = []
        if reader.has_unversioned_properties:
            InnerTag = tag.InnerData
            InnerType = tag.InnerType
        elif InnerType.string == "StructProperty" or InnerType.string == "ArrayProperty":
            InnerTag = FPropertyTag(reader)
        else:
            InnerTag = None
        pos = reader.base_stream.tell()
 
        for _ in range(length):
            val = PropertyTagData.BaseProperty.ReadAsObject(reader, InnerTag, InnerType,
                                                            PropertyTagData.BaseProperty.ReadType.ARRAY)
            Value.append(val)
        return Value
