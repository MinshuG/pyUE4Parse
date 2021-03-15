# actually None

from UE4Parse.BinaryReader import BinaryStream


class _None:
    CultureInvariantString: str = None

    def __init__(self, reader: BinaryStream) -> None:
        if reader.readInt32() != 0:
            self.CultureInvariantString = reader.readFString()

    def GetValue(self):
        return self.CultureInvariantString
