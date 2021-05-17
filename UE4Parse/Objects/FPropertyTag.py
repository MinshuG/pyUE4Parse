from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Objects import FName
from UE4Parse.Objects.FGuid import FGuid


class FPropertyTag:
    ArrayIndex = 0
    position = 0
    BoolVal = 0
    EnumName: FName
    EnumType: FName
    HasPropertyGuid: bool = 0
    InnerType: FName
    Name: FName
    PropertyGuid: FGuid
    Size: int
    SizeOffset: int
    StructGuid: FGuid
    StructName: FName
    Type: FName
    ValueType: FName

    def __init__(self, reader: BinaryStream):
        self.Name = reader.readFName()
        if self.Name.isNone:
            return

        self.Type = reader.readFName()
        self.Size = reader.readInt32()
        self.ArrayIndex = reader.readInt32()

        self.position = reader.base_stream.tell()
        if self.Type.Number == 0:
            Type = self.Type.string
            if Type == "StructProperty":
                self.StructName = reader.readFName()
                self.StructGuid = FGuid(reader)
            elif Type == "BoolProperty":
                self.BoolVal = reader.readByteToInt()
            elif Type == "ByteProperty" or Type == "EnumProperty":
                self.EnumName = reader.readFName()
            elif Type == "ArrayProperty":
                self.InnerType = reader.readFName()
            elif Type == "SetProperty":
                self.InnerType = reader.readFName()
            elif Type == "MapProperty":
                self.InnerType = reader.readFName()
                self.ValueType = reader.readFName()

        HasPropertyGuid = reader.readByteToInt()
        if HasPropertyGuid != 0:
            FGuid(reader)
        self.end_pos = reader.tell()

    def __repr__(self):
        return f"< {self.Name.string} : {self.Type.string} >"
