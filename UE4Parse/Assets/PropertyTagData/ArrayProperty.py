from UE4Parse import Logger

from UE4Parse.Assets import PropertyTagData
from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Assets.Objects.FPropertyTag import FPropertyTag

logger = Logger.get_logger(__name__)

class ArrayProperty:
    Value: list
    position: int

    def __init__(self, reader: BinaryStream, tag: FPropertyTag):
        self.position = reader.base_stream.tell()
        self.Value = []
        self.ArrayPropertyReader(reader, tag)

    def GetValue(self):
        return [x.GetValue() for x in self.Value]

    def ArrayPropertyReader(self, reader: BinaryStream, tag) -> list:
        InnerType = tag.InnerType

        length = reader.readInt32()
        if reader.has_unversioned_properties:
            InnerTag = tag.InnerData
            InnerType = tag.InnerType
        elif InnerType.string == "StructProperty" or InnerType.string == "ArrayProperty":
            InnerTag = FPropertyTag(reader)
        else:
            InnerTag = None
 
        for i in range(length):
            try:
                val = PropertyTagData.BaseProperty.ReadAsObject(reader, InnerTag, InnerType,
                                                                PropertyTagData.BaseProperty.ReadType.ARRAY)
                self.Value.append(val)
            except Exception as e:
                raise e
                # logger.warn(f"Failed to read ArrayProperty of type {InnerType} at ${reader.position} index {i}, {e}")
