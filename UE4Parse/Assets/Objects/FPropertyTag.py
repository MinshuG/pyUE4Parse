from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Assets.Objects.FName import FName
from UE4Parse.Versions.EUnrealEngineObjectUE4Version import UE4Versions
from UE4Parse.Assets.Objects.FGuid import FGuid

from Usmap import StructProps
from Usmap.Objects.FPropertyTag import FPropertyTag as UsmapTag

class FPropertyTag2:
    def __init__(self, **kwargs) -> None:
        for k,v in kwargs.items():
            setattr(self, k, v)

class FPropertyTag:
    ArrayIndex = 0
    position = 0
    BoolVal: int
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

    def __init__(self, reader: BinaryStream, propMappings: StructProps = None):
        if propMappings:
            propdata = propMappings.data

            self.Name = FName(propMappings.Name)            
            self.ArrayIndex = propMappings.ArraySize

            # data section
            for attr in ["EnumName", "InnerType", "StructName", "ValueType", "Type"]:
                val = getattr(propdata, attr, None)
                if val is None:
                    continue

                if attr == "InnerType":
                    self.InnerData = val #FPropertyTag2(**val)
                elif attr == "ValueType":
                    self.ValueData = val #FPropertyTag2(val)

                if isinstance(val, str):
                    val = FName(val)
                if isinstance(val, UsmapTag):
                    val = FName(val.Type)
                setattr(self, attr, val)
            return

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
                if reader.version >= UE4Versions.VER_UE4_STRUCT_GUID_IN_PROPERTY_TAG:
                    self.StructGuid = FGuid(reader)
            elif Type == "BoolProperty":
                self.BoolVal = reader.readByteToInt()
            elif Type == "ByteProperty" or Type == "EnumProperty":
                self.EnumName = reader.readFName()
            elif Type == "ArrayProperty":
                if reader.version >= UE4Versions.VAR_UE4_ARRAY_PROPERTY_INNER_TAGS:
                    self.InnerType = reader.readFName()
            elif Type == "SetProperty":
                if reader.version >= UE4Versions.VER_UE4_PROPERTY_TAG_SET_MAP_SUPPORT:
                    self.InnerType = reader.readFName()
            elif Type == "MapProperty":
                if reader.version >= UE4Versions.VER_UE4_PROPERTY_TAG_SET_MAP_SUPPORT:
                    self.InnerType = reader.readFName()
                    self.ValueType = reader.readFName()

        HasPropertyGuid = reader.readByteToInt()
        if HasPropertyGuid != 0:
            FGuid(reader)
        self.end_pos = reader.tell()

    def __repr__(self):
        return f"<{self.Name.string} : {self.Type.string}>"
