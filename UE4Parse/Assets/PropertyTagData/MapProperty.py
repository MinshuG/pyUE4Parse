from UE4Parse.Assets import PropertyTagData
from UE4Parse.BinaryReader import BinaryStream


class MapProperty:
    position: int
    Value: dict

    def __init__(self, reader: BinaryStream, tag, readType):
        self.position = reader.base_stream.tell()
        self.Value = {}
        if readType.value == 3: return

        NumKeysToRemove = reader.readInt32()

        for _ in range(NumKeysToRemove):
            PropertyTagData.BaseProperty.ReadAsValue(reader, tag, tag.InnerType,
                                                         PropertyTagData.BaseProperty.ReadType.MAP)

        NumEntries = reader.readInt32()
        for _ in range(NumEntries):
            inner_data = getattr(tag, "InnerData", None)
            value_data = getattr(tag, "ValueData", None)
            key = str(PropertyTagData.BaseProperty.ReadAsValue(reader, inner_data or tag, tag.InnerType,
                                                               PropertyTagData.BaseProperty.ReadType.MAP))
            value = PropertyTagData.BaseProperty.ReadAsObject(reader, value_data or tag, tag.ValueType,
                                                              PropertyTagData.BaseProperty.ReadType.MAP)

            self.Value[key] = value

    def GetValue(self) -> dict:
        Dict: dict = {}
        for key, value in self.Value.items():
            Dict[key] = value.GetValue()
        return Dict
