from UE4Parse.BinaryReader import BinaryStream


class FEngineVersion:
    Major: int
    Minor: int
    Patch: int
    Changelist: int
    Branch: str
    
    def __init__(self,reader: BinaryStream) -> None:
        self.Major = reader.readUInt16()
        self.Minor = reader.readUInt16()
        self.Patch = reader.readUInt16()
        self.Changelist = reader.readUInt32()
        self.Branch = reader.readFString()
