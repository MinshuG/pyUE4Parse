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
                # Must pass a ReadType, not the literal 0: the numeric inner
                # property readers (e.g. UInt16Property/UInt32Property for enums
                # with >256 members) do `readType.value`, which raises on an int.
                byteValue = ReadAsValue(reader, tag.InnerData, innerType, ReadType.NORMAL)
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
            # The mappings (.usmap) can be older than the game build, so an enum
            # may have gained members and `index` can be past the known list.
            # Fall back to "EnumName::<index>" instead of crashing the whole asset.
            # The enum width is unaffected, so this never desyncs the stream.
            enumVals = reader.getmappings().get_enum(name.string)
            label = None
            if enumVals is not None:
                try:
                    label = enumVals[index]
                except (IndexError, KeyError, TypeError):
                    label = None
            if label is None:
                label = str(index)
            return name.string + "::" + label
