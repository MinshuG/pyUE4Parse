from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Assets.Objects.FPropertyTag import FPropertyTag
from UE4Parse.Assets.Objects.FName import FName


class EnumProperty:
    position: int
    Value: FName

    def __init__(self, reader: BinaryStream, tag: FPropertyTag, readType):
        self.position = reader.base_stream.tell()
        from .BaseProperty import ReadType

        if readType == ReadType.ZERO: #ZERO
            self.Value = FName(self.IndexToEnum(reader, tag, 0))
        elif reader.has_unversioned_properties and readType == ReadType.NORMAL:
            byteValue = 0
            innerType = getattr(tag, "InnerType", None)
            if innerType is not None:
                from .BaseProperty import ReadAsValue
                byteValue = ReadAsValue(reader, tag.InnerData, innerType, 0)
            else:
                byteValue = reader.readByteToInt()

            self.Value = FName(self.IndexToEnum(reader, tag, byteValue))
        else:
            self.Value = reader.readFName()

    def GetValue(self):
        return self.Value.GetValue()

    def IndexToEnum(self, reader: BinaryStream, tag: FPropertyTag, index: int):
        name = tag.EnumName
        if name is None:
            return str(index)
        elif name is not None and not reader.has_unversioned_properties:
            name_entry = str(reader.NameMap[index])
            if "::" in name_entry:
                return name_entry
            return str(name) + "::" + name_entry

        if reader.has_unversioned_properties:
            enumVals = reader.getmappings().get_enum(name.string)
            return tag.EnumName.string + "::" + enumVals[index]
