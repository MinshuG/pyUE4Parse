from typing import List

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.IO.IoObjects.FIoDirectoryIndexEntry import FIoDirectoryIndexEntry
from UE4Parse.IO.IoObjects.FIoFileIndexEntry import FIoFileIndexEntry


class FIoDirectoryIndexResource:
    MountPoint: str
    DirectoryEntries: List[FIoDirectoryIndexEntry]
    FileEntries: List[FIoFileIndexEntry]
    StringTable: List[str]

    def __init__(self, reader: BinaryStream, Case_insensitive: bool):
        self.MountPoint = reader.readFString()

        if self.MountPoint.startswith("../../.."):
            self.MountPoint = self.MountPoint[8::]

        if Case_insensitive:
            self.MountPoint = self.MountPoint.lower()

        self.DirectoryEntries = reader.readTArray_W_Arg(FIoDirectoryIndexEntry, reader)
        self.FileEntries = reader.readTArray_W_Arg(FIoFileIndexEntry, reader)
        self.StringTable = reader.readTArray(reader.readFString)

