from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Objects.FGuid import FGuid

class FCustomVersion:
    key: FGuid = ""
    Version: int = None

    def read(self,reader: BinaryStream):
        self.key = FGuid(reader).read(),
        self.Version = reader.readInt32()