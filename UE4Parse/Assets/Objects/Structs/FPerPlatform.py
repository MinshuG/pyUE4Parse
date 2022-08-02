from UE4Parse.Assets.Objects.Common import StructInterface
from UE4Parse.BinaryReader import BinaryStream


class FPerPlatform(StructInterface):
    def __init__(self):
        pass

    def GetValue(self):
        return {
            "Cooked": self.Cooked,
            "Value": self.Value
        }


class FPerPlatformInt(FPerPlatform):
    Cooked: bool
    Value: int

    def __init__(self, reader: BinaryStream):
        super().__init__()
        self.Cooked = reader.readBool()
        self.Value = reader.readInt32()
    
    @classmethod
    def default(cls):
        inst = cls.__new__(cls)
        inst.Cooked = False
        inst.Value = 0
        return inst


class FPerPlatformFloat(FPerPlatform):
    Cooked: bool
    Value: float

    def __init__(self, reader: BinaryStream):
        super().__init__()
        self.Cooked = reader.readBool()
        self.Value = reader.readFloat()

    @classmethod
    def default(cls):
        inst = cls.__new__(cls)
        inst.Cooked = False
        inst.Value = 0.0
        return inst