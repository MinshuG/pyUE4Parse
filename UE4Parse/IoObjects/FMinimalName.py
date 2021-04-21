from typing import Optional

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.IoObjects.FNameEntryId import FNameEntryId


class FMinimalName:
    Index: FNameEntryId
    Number: int

    def __init__(self, reader: Optional[BinaryStream] = None):
        if reader is None:
            return
        self.Index = FNameEntryId(reader)
        self.Number = reader.readInt32()

    def make(self, index, number):
        self.Index = index
        self.Number = number
        return self
