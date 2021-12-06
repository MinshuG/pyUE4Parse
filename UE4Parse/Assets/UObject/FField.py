from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from UE4Parse.Assets.Objects.FName import FName
    from UE4Parse.Readers.FAssetReader import FAssetReader


class FField(object):
    Name: FName
    Flags: int

    def __init__(self):
        self.Name = FName("None", 0)
        self.Flags = 0

    def deserialize(self, reader: FAssetReader):
        self.Name = reader.readFName()
        self.Flags = reader.readUInt32()

    def serialize_single_field(self, reader: FAssetReader) -> Optional['FField']:
        property_field_name = reader.readFName()
        if not property_field_name.isNone:
            field = self.construct(property_field_name)
            field.deserialize(reader)
            return field
        return None

    @staticmethod
    def construct(field_type: FName) -> 'FField':
        raise NotImplementedError()

    def GetValue(self):
        return {
            "Name": self.Name.GetValue(),
            "Flags": self.Flags
        }
