from UE4Parse.Assets import PropertyTagData
from UE4Parse.BinaryReader import BinaryStream


class MapProperty:
    position: int
    Value: dict = {}

    def __init__(self, reader: BinaryStream, tag):
        # raise NotImplementedError("Map Prop")
        self.position = reader.base_stream.tell()
        NumKeysToRemove = reader.readInt32()

        if NumKeysToRemove != 0:
            for _ in range(NumKeysToRemove):
                PropertyTagData.BaseProperty.ReadAsValue(reader, tag, tag.InnerType,
                                                         PropertyTagData.BaseProperty.ReadType.MAP)

        NumEntries = reader.readInt32()
        data = {}
        for _ in range(NumEntries):
            key = str(PropertyTagData.BaseProperty.ReadAsValue(reader, tag, tag.InnerType,
                                                               PropertyTagData.BaseProperty.ReadType.MAP))
            value = PropertyTagData.BaseProperty.ReadAsObject(reader, tag, tag.ValueType,
                                                              PropertyTagData.BaseProperty.ReadType.MAP)

            data[key] = value  # formatting tho
        self.Value = data

    def GetValue(self) -> dict:
        Dict: dict = {}
        for key, value in self.Value.items():
            Dict[key] = value.GetValue()
        return Dict
