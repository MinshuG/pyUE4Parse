from UE4Parse.BinaryReader import BinaryStream


class FGuid:
    position: int
    A: int
    B: int
    C: int
    D: int

    def __init__(self, reader: BinaryStream):
        self.A = reader.readUInt32()
        self.B = reader.readUInt32()
        self.C = reader.readUInt32()
        self.D = reader.readUInt32()

    def read(self):  # both works nvm. nope they don't stupid. now they do
        return self

    def GetValue(self):
        def formatter(a):
            return format(a, '08x')
        return f"{formatter(self.A)}{formatter(self.B)}{formatter(self.C)}{formatter(self.D)}".upper()
