from UE4Parse.BinaryReader import BinaryStream


class FEngineVersion:
    def __init__(self,reader: BinaryStream) -> None:
        self.reader = reader
        self.Major = reader.readUInt16()
        self.Minor = reader.readUInt16()
        self.Patch = reader.readUInt16()
        self.Changelist = reader.readUInt32()
        self.Branch = reader.readFString()