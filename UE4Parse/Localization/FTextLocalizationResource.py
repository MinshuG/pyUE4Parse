from typing import Dict, List, Optional

from UE4Parse import Logger
from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Exceptions import ParserException
from UE4Parse.Objects.FGuid import FGuid
from .FTextLocalizationResourceVersion import ELocResVersion

logger = Logger.get_logger(__name__)


class FTextLocalizationResourceString:
    String: str
    RefCount: int

    def __init__(self, reader: Optional[BinaryStream] = None) -> None:
        if reader is None:
            return
        self.String = reader.readFString()
        self.RefCount = reader.readInt32()

    def construct(self, string: str, refcount: int):
        self.String = string
        self.RefCount = refcount

# Locres
class FTextLocalizationResource:
    """LocRes Reader"""
    LocResMagic = FGuid().construct(0x7574140E, 0xFC034A67, 0x9D90154A, 0x1B7F37C3)

    Entries: Dict[str, Dict[str, str]]


    def __init__(self, reader: BinaryStream) -> None:
        self.Entries = {}
        magic = FGuid(reader)

        VersionNumber = ELocResVersion.Legacy
        if magic == self.LocResMagic:
            VersionNumber = ELocResVersion(reader.readByteToInt())
        else:
            reader.seek(0)
        
        if VersionNumber > ELocResVersion.Latest:
            raise ParserException(f"LocRes is too new to be loaded (File Version: {VersionNumber.value}, Loader Version: {ELocResVersion.Latest.value})")

        LocalizedStringArray: List[FTextLocalizationResourceString] = []
        if VersionNumber >= ELocResVersion.Compact:
            LocalizedStringArrayOffset = -1
            LocalizedStringArrayOffset = reader.readInt64()
            CurrentFileOffset = reader.tell()
            reader.seek(LocalizedStringArrayOffset, 0)

            if LocalizedStringArrayOffset != -1:
                if VersionNumber >= ELocResVersion.Optimized_CRC32:
                    LocalizedStringArray = reader.readTArray_W_Arg(FTextLocalizationResourceString, reader)
                    reader.seek(CurrentFileOffset, 0)
            else:
                TmpLocalizedStringArray: List[str]
                TmpLocalizedStringArray = reader.readTArray(reader.readFString)
                reader.seek(CurrentFileOffset, 0)
                for LocalizedString in TmpLocalizedStringArray:
                    LocalizedStringArray.append(FTextLocalizationResourceString().construct(LocalizedString, -1))

        if VersionNumber >= ELocResVersion.Optimized_CRC32:
            reader.seek(4) # EntriesCount uint

        NamespaceCount = reader.readUInt32()
        for _ in range(NamespaceCount):
            if VersionNumber >= ELocResVersion.Optimized_CRC32:
                reader.seek(4) # StrHash uint

            Namespace = reader.readFString()
            KeyCount = reader.readUInt32()
            Entries: Dict[str, str] = {}
            for i in range(KeyCount):
                if VersionNumber >= ELocResVersion.Optimized_CRC32:
                    reader.seek(4) # StrHash uint

                Key: str = reader.readFString();
                reader.seek(4) # SourceStringHash

                EntryLocalizedString: str
                if VersionNumber >= ELocResVersion.Compact:
                    LocalizedStringIndex = reader.readInt32()

                    if LocalizedStringIndex < len(LocalizedStringArray):
                        LocalizedString = LocalizedStringArray[LocalizedStringIndex]
                        EntryLocalizedString = LocalizedString.String
                        LocalizedString.RefCount -= 1
                    else:
                        raise ParserException(f"LocRes has an invalid localized string index for namespace '{Namespace}' and key '{Key}'. This entry will have no translation.")
                else:
                    EntryLocalizedString = reader.readFString()

                Entries[Key] = EntryLocalizedString
            self.Entries[Namespace] = Entries

    def GetValue(self):
        return self.Entries



if __name__ == '__main__':
    FTextLocalizationResource(BinaryStream(r"G:\umodel_win32\FModel\Output\Exports\ShooterGame\Content\Localization\Game\en-US\Game.locres"))
