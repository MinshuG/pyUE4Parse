from UE4Parse.BinaryReader import BinaryStream


class FPerPlatform:
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


class FPerPlatformFloat(FPerPlatform):
    Cooked: bool
    Value: float

    def __init__(self, reader: BinaryStream):
        super().__init__()
        self.Cooked = reader.readBool()
        self.Value = reader.readFloat()
