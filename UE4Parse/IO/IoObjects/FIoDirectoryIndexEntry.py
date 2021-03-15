from UE4Parse.BinaryReader import BinaryStream


class FIoDirectoryIndexEntry:
    Name: int
    FirstChildEntry: int
    NextSiblingEntry: int
    FirstFileEntry: int

    def __init__(self, reader: BinaryStream):
        self.Name = reader.readUInt32()
        self.FirstChildEntry = reader.readUInt32()
        self.NextSiblingEntry = reader.readUInt32()
        self.FirstFileEntry = reader.readUInt32()
