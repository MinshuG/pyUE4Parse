# actually None

from functools import singledispatchmethod
from UE4Parse.BinaryReader import BinaryStream


class _None:
    CultureInvariantString: str = ""

    @singledispatchmethod
    def __init__(self, reader: BinaryStream) -> None:
        if reader.readBool():
            self.CultureInvariantString = reader.readFString()

    @__init__.register
    def _(self, string: str="" ):
        self.CultureInvariantString = string

    def GetValue(self):
        return self.CultureInvariantString
