from typing import Tuple

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.PakFile.PakObjects.FPathHashIndexEntry import FPathHashIndexEntry


class FPakDirectoryEntry:
    Directory: str
    Entries: Tuple[FPathHashIndexEntry]

    def __init__(self, reader: BinaryStream):
        self.Directory = reader.readFString()
        self.Entries = reader.readTArray(FPathHashIndexEntry, reader)
