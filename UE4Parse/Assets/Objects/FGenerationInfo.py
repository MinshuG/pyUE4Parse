from UE4Parse.BinaryReader import BinaryStream


class FGenerationInfo:
    ExportCount: int
    NameCount: int

    def __init__(self,reader: BinaryStream) -> None:
        self.ExportCount = reader.readInt32()
        self.NameCount = reader.readInt32()

    @property
    def SIZE(self):
        return 8