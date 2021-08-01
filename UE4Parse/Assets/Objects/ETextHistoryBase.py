from enum import Enum, auto


class ETextHistoryBase(Enum):
    _None = -1
    Base = 0
    NamedFormat = auto()
    OrderedFormat = auto()
    ArgumentFormat = auto()
    AsNumber = auto()
    AsPercent = auto()
    AsCurrency = auto()
    AsDate = auto()
    AsTime = auto()
    AsDateTime = auto()
    Transform = auto()
    StringTableEntry = auto()
    TextGenerator = auto()
