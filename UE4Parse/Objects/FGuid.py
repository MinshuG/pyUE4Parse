from typing import Optional

from UE4Parse.BinaryReader import BinaryStream


# TODO Implement EGuidFormats
class FGuid:
    position: int
    A: int
    B: int
    C: int
    D: int

    def __init__(self, reader: Optional[BinaryStream] = None):
        if reader is None:
            return
        self.A = reader.readUInt32()
        self.B = reader.readUInt32()
        self.C = reader.readUInt32()
        self.D = reader.readUInt32()

    def read(self):  # both works nvm. nope they don't stupid. now they do
        return self

    def construct(self, A: int, B: int, C: int, D: int):
        self.A = A
        self.B = B
        self.C = C
        self.D = D
        return self

    def __eq__(self, o: 'FGuid') -> bool:
        return ((self.A ^ o.A) | (self.B ^ o.B) | (self.C ^ o.C) | (self.D ^ o.D)) == 0
        # return self.GetValue() == o.GetValue()

    def GetValue(self):
        def formatter(a):
            return format(a, '08x')

        return f"{formatter(self.A)}{formatter(self.B)}{formatter(self.C)}{formatter(self.D)}".upper()

    def __hash__(self) -> int:
        return hash(self.GetValue())
