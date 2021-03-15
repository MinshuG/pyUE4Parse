from UE4Parse.BinaryReader import BinaryStream


class FPathHashIndexEntry:
    FileName: str
    Location: int

    def __init__(self, reader: BinaryStream):
        self.FileName = reader.readFString()
        self.Location = reader.readInt32()
