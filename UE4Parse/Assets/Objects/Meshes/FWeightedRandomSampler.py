from typing import List, Tuple
from UE4Parse.Assets.Objects.Common import StructInterface

from UE4Parse.BinaryReader import BinaryStream


class FWeightedRandomSampler(StructInterface):
    Prob: Tuple[float]
    Alias: Tuple[int]
    TotalWeight: float

    def __init__(self, reader: BinaryStream):
        self.Prob = reader.readTArray(reader.readFloat)
        self.Alias = reader.readTArray(reader.readInt32)
        self.TotalWeight = reader.readFloat()

    @classmethod
    def default(cls):
        inst = cls.__new__(cls)
        inst.Prob = tuple()
        inst.Alias = tuple()
        inst.TotalWeight = 0.0
        return inst

    def GetValue(self):
        return {
            "Prob": self.Prob,
            "Alias": self.Alias,
            "TotalWeight": self.TotalWeight
        }

class FSkeletalMeshAreaWeightedTriangleSampler(FWeightedRandomSampler):
    pass
