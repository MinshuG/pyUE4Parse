# actually None

from UE4Parse.BinaryReader import BinaryStream


class _None:
    CultureInvariantString: str = ""

    def __init__(self, reader: BinaryStream) -> None:
        if reader.readBool():
            self.CultureInvariantString = reader.readFString()

    def GetValue(self):
        return self.CultureInvariantString
