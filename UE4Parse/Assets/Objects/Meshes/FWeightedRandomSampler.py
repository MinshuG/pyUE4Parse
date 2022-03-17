from typing import List

from UE4Parse.BinaryReader import BinaryStream


class FWeightedRandomSampler:
    Prob: List[float]
    Alias: List[int]
    TotalWeight: float

    def __init__(self, reader: BinaryStream):
        self.Prob = reader.readTArray(reader.readFloat)
        self.Alias = reader.readTArray(reader.readInt32)
        self.TotalWeight = reader.readFloat()

    def GetValue(self):
        return {
            "Prob": self.Prob,
            "Alias": self.Alias,
            "TotalWeight": self.TotalWeight
        }

class FSkeletalMeshAreaWeightedTriangleSampler(FWeightedRandomSampler):
    pass
