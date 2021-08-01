from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Assets.Objects.FGuid import FGuid


class FCustomVersion:
    key: FGuid
    Version: int

    def __init__(self, reader: BinaryStream):
        self.key = FGuid(reader)
        self.Version = reader.readInt32()
