from UE4Parse.Objects.Structs.UScriptStruct import UScriptStruct
from UE4Parse.BinaryReader import BinaryStream


class StructProperty:
    position: int
    Value = None

    def __init__(self, reader: BinaryStream, tag) -> None:
        self.position = reader.base_stream.tell()
        self.Value = UScriptStruct(reader, tag.StructName.string)

    def GetValue(self):
        return self.Value.GetValue()
