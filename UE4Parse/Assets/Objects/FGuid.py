from functools import singledispatchmethod
from typing import Union

from UE4Parse.BinaryReader import BinaryStream


# TODO Implement EGuidFormats
class FGuid:
    position: int
    A: int
    B: int
    C: int
    D: int

    @singledispatchmethod
    def __init__(self, reader: BinaryStream):
        self.A = reader.readUInt32()
        self.B = reader.readUInt32()
        self.C = reader.readUInt32()
        self.D = reader.readUInt32()

    @__init__.register
    def _from_str(self, string: str):
        self.A = int(string[0:8], 16)
        self.B = int(string[8:16], 16)
        self.C = int(string[16:24], 16)
        self.D = int(string[24:32], 16)

    @__init__.register
    def from_int_(self, A: int, B: int, C: int, D: int):
        self.A = A
        self.B = B
        self.C = C
        self.D = D

    def __eq__(self, o: Union['FGuid', str]) -> bool:
        if isinstance(o, str):
            return str(self).lower() == o.lower()
        return ((self.A ^ o.A) | (self.B ^ o.B) | (self.C ^ o.C) | (self.D ^ o.D)) == 0

    def GetValue(self):
        def formatter(a):
            return format(a, '08x')
        return f"{formatter(self.A)}{formatter(self.B)}{formatter(self.C)}{formatter(self.D)}".upper()

    def __str__(self):
        return self.GetValue()

    def __hash__(self) -> int:
        return hash(self.GetValue())
