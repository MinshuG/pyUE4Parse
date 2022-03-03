from UE4Parse.BinaryReader import BinaryStream


class FIoDirectoryIndexEntry:
    Name: int
    FirstChildEntry: int
    NextSiblingEntry: int
    FirstFileEntry: int

    def __init__(self, reader: BinaryStream):
        self.Name, self.FirstChildEntry, self.NextSiblingEntry, self.FirstFileEntry =  reader.unpack2('4I', 4*4)
        # self.Name = reader.readUInt32()
        # self.FirstChildEntry = reader.readUInt32()
        # self.NextSiblingEntry = reader.readUInt32()
        # self.FirstFileEntry = reader.readUInt32()
