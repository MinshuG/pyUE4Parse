from UE4Parse.Readers.FAssetReader import FAssetReader


class Base:
    Namespace = ""
    Key = ""
    SourceString = ""
    def __init__(self, reader: FAssetReader) -> None:
        self.Namespace = reader.readFString() or ""
        self.Key = reader.readFString() or ""
        self.SourceString = reader.provider.get_localized_string(self.Namespace, self.Key, reader.readFString())

    def GetValue(self):
        return {
            "Namespace": self.Namespace,
            "Key": self.Key,
            "SourceString": self.SourceString
        }