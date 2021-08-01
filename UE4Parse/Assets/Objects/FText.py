from UE4Parse.Assets.Objects.FTextHistory.NamedFormat import NamedFormat
from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Assets.Objects.ETextFlag import ETextFlag
from UE4Parse.Assets.Objects.ETextHistoryBase import ETextHistoryBase
from UE4Parse.Assets.Objects.FTextHistory.Base import Base
from UE4Parse.Assets.Objects.FTextHistory.StringTableEntry import StringTableEntry
from UE4Parse.Assets.Objects.FTextHistory._None import _None


class FText:
    Flags: ETextFlag
    Text: object

    def __init__(self, reader: BinaryStream) -> None:
        FlagVal = reader.readUInt32()
        try:
            self.Flags = ETextFlag(FlagVal)
        except:
            self.Flags = FlagVal

        self.HistoryType = ETextHistoryBase(reader.readSByte())
        if self.HistoryType == ETextHistoryBase.Base:
            self.Text = Base(reader)
        elif self.HistoryType == ETextHistoryBase.NamedFormat:
            self.Text = NamedFormat(reader)
        elif self.HistoryType == ETextHistoryBase.StringTableEntry:
            self.Text = StringTableEntry(reader)
        elif self.HistoryType == ETextHistoryBase._None:
            self.Text = _None(reader)
        else:
            raise NotImplementedError(f"FText: Unsupported FText Type {self.HistoryType.name}")

    def GetValue(self):
        return self.Text.GetValue()
