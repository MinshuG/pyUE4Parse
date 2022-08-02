from typing import List
from UE4Parse.Assets import PropertyTagData
from UE4Parse.BinaryReader import BinaryStream


class SetProperty:
    Value: List[object]

    def __init__(self, reader: BinaryStream, Tag, readType):
        self.Value = []
        if readType.value == 3: return

        NumKeystoRemove = reader.readInt32()
        for _ in range(NumKeystoRemove):
            PropertyTagData.BaseProperty.ReadAsObject(reader, Tag, Tag.Type,
                                                      PropertyTagData.BaseProperty.ReadType.ARRAY)
        Entries = reader.readInt32()
        for _ in range(Entries):
            value = PropertyTagData.BaseProperty.ReadAsObject(reader, Tag, Tag.InnerType,
                                                              PropertyTagData.BaseProperty.ReadType.ARRAY)
            self.Value.append(value)

    def GetValue(self):
        return [v.GetValue() for v in self.Value]
