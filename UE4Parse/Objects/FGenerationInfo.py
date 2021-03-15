from UE4Parse.BinaryReader import BinaryStream


class FGenerationInfo:
    def __init__(self,reader: BinaryStream) -> None:
        self.reader = reader
        
        self.ExportCount = reader.readInt32()
        self.NameCount = reader.readInt32()

    # def read():
    #     self.ExportCount = reader.readInt32()
    #     self.NameCount = reader.readInt32()