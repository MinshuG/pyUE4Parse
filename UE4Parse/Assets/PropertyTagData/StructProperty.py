from UE4Parse.Assets.Objects.FName import FName
from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Assets.Objects.Structs.UScriptStruct import UScriptStruct


class StructProperty:
    position: int
    Value = None

    def __init__(self, reader: BinaryStream, tag, readType) -> None:
        self.position = reader.base_stream.tell()
        if readType.value == 1: # Map
            struct_name = "WeDon'tCare?"
        else:
            struct_name = tag.StructName.string if isinstance(tag.StructName, FName) else tag.StructName
        self.Value = UScriptStruct(reader, struct_name, readType).Struct

    def GetValue(self):
        return self.Value.GetValue()
