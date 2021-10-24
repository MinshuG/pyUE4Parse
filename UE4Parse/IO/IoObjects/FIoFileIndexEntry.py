from UE4Parse.BinaryReader import BinaryStream


class FIoFileIndexEntry:
    __slots__ = ("Name", "NextFileEntry", "UserData")
    Name: int
    NextFileEntry: int
    UserData: int

    def __init__(self, reader: BinaryStream):
        self.Name = reader.readUInt32()
        self.NextFileEntry = reader.readUInt32()
        self.UserData = reader.readUInt32()
