from typing import Optional

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.IoObjects.FNameEntryId import FNameEntryId
from UE4Parse.Assets.Objects.FName import FName


class FMinimalName:
    Index: FNameEntryId
    Number: int

    def __init__(self, reader: Optional[BinaryStream] = None, namemap=None):
        if reader is None:
            return
        self.NameMap = namemap
        self.Index = FNameEntryId(reader)
        self.Number = reader.readInt32()

    def make(self, index, number):
        self.Index = index
        self.Number = number
        return self

    def ToFName(self):
        IndexMask = (1 << 30) - 1
        return FName(self.NameMap[IndexMask & self.Index.Value], self.Index.Value, self.Number)

    def GetValue(self):
        return self.ToFName().GetValue()

    def __str__(self):
        return self.GetValue()
