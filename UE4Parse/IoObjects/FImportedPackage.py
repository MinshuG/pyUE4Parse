from typing import List

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.IO.IoObjects.FIoChunkId import FIoChunkId
from UE4Parse.IoObjects.EIoChunkType import EIoChunkType


class FArc:
    fromIndex: int
    toIndex: int

    def __init__(self, reader: BinaryStream):
        self.fromIndex = reader.readInt32()
        self.toIndex = reader.readInt32()


class FPackageId:
    Id: int

    def __init__(self, reader: BinaryStream):
        self.Id = reader.readUInt64()

    def __str__(self) -> str:
        return str(self.Id)


class FImportedPackage:
    index: FPackageId
    Arcs: List[FArc]

    def __init__(self, reader: BinaryStream):
        self.index = FPackageId(reader)
        self.Arcs = reader.readTArray(FArc, reader)
