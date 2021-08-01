from enum import IntEnum, auto
from typing import Dict, TYPE_CHECKING
from UE4Parse.BinaryReader import BinaryStream

if TYPE_CHECKING:
    from ..FText import FText

class NamedFormat:
    SourceFmt: 'FText'
    Arguments: Dict[str, 'FFormatArgumentValue']

    def __init__(self, reader: BinaryStream) -> None:
        from ..FText import FText
        self.SourceFmt = FText(reader)
        self.Arguments = {}
        lenargs = reader.readInt32()
        for _ in range(lenargs):
            self.Arguments[reader.readFString()] = FFormatArgumentValue(reader)

    def GetValue(self):
        Arguments = {}
        for k,v in self.Arguments.items():
            Arguments[k] = v.GetValue()
        return {
            "SourceFmt": self.SourceFmt.GetValue(),
            **Arguments
        }


class EFormatArgumentType(IntEnum):
    Int = 0
    UInt = auto()
    Float = auto()
    Double = auto()
    Text = auto()
    Gender =auto()
    # Add new enum types at the end only! They are serialized by index.



class FFormatArgumentValue:
    Type: EFormatArgumentType
    Value: object

    def __init__(self, reader: BinaryStream) -> None:
        Type = EFormatArgumentType(reader.readSByte())
        self.Type = Type
        if Type == EFormatArgumentType.Text:
            from ..FText import FText
            self.Value = FText(reader)
        elif Type == EFormatArgumentType.Int:
            self.Value = reader.readInt64()
        elif Type == EFormatArgumentType.UInt:
            self.Value = reader.readUInt64()
        elif Type == EFormatArgumentType.Double:
            self.Value = reader.readDouble()
        elif Type == EFormatArgumentType.Float:
            self.Value = reader.readFloat()

    def GetValue(self):
        attr = getattr(self.Value, "GetValue", False)
        if attr: return attr()
        else: return self.Value
