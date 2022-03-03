from typing import List

from UE4Parse.BinaryReader import BinaryStream


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

    @classmethod
    def from_int(cls, x: int):
        inst = cls.__new__(cls); inst.Id = x
        return inst

    @classmethod
    def from_name(cls, name: str):
        raise NotImplementedError()
        # h = cityhash.CityHash64(bytes(name.lower(), "utf-16"))
        # return cls.from_int(h)

    def __eq__(self, other):
        return self.Id == other.Id

    def __hash__(self):
        return self.Id

    def __str__(self) -> str:
        return str(self.Id)


class FImportedPackage:
    index: FPackageId
    Arcs: List[FArc]

    def __init__(self, reader: BinaryStream):
        self.index = FPackageId(reader)
        self.Arcs = reader.readTArray(FArc, reader)
