from UE4Parse.BinaryReader import BinaryStream


class Base:
    Namespace = ""
    Key = ""
    SourceString = ""
    def __init__(self,reader: BinaryStream) -> None:
        self.Namespace = reader.readFString() or ""
        self.Key = reader.readFString() or ""
        self.SourceString = reader.readFString()

    def GetValue(self):
        return {
            "Namespace": self.Namespace,
            "Key": self.Key,
            "SourceString": self.SourceString
        }