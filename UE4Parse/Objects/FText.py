from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Objects.ETextFlag import ETextFlag
from UE4Parse.Objects.ETextHistoryBase import ETextHistoryBase
from UE4Parse.Objects.FTextHistory.Base import Base
from UE4Parse.Objects.FTextHistory._None import _None
from UE4Parse.Objects.FTextHistory.StringTableEntry import StringTableEntry


class FText:
    Flags = None
    Text = None

    def __init__(self, reader: BinaryStream) -> None:
        FlagVal = reader.readUInt32()
        try:
            Flags = ETextFlag(FlagVal)
        except:
            Flags = FlagVal

        self.HistoryType = ETextHistoryBase(reader.readSByte())
        if self.HistoryType.name == "Base":
            self.Text = Base(reader)
        elif self.HistoryType.name == "StringTableEntry":
            self.Text = StringTableEntry(reader)
        elif self.HistoryType.name == "_None":
            self.Text = _None(reader)
        else:
            raise NotImplementedError(f"FText: Unsupported FText Type {self.HistoryType.name}")

    def GetValue(self):
        return self.Text.GetValue()
