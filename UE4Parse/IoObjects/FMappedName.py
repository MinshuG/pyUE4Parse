from typing import List

# from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Objects.FNameEntrySerialized import FNameEntrySerialized


class FMappedName:
    Index: int
    Number: int
    _reader: object
    _globalNameMap: List[FNameEntrySerialized]
