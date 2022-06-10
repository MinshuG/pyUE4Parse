from typing import TYPE_CHECKING
from UE4Parse.Assets.Objects.Common import StructInterface

from UE4Parse.Assets.Objects.Meshes.FWeightedRandomSampler import FSkeletalMeshAreaWeightedTriangleSampler
from UE4Parse.BinaryReader import BinaryStream


class FSkeletalMeshSamplingLODBuiltData(StructInterface):
    AreaWeightedTriangleSampler: FSkeletalMeshAreaWeightedTriangleSampler

    def __init__(self, reader: BinaryStream):
        self.AreaWeightedTriangleSampler = FSkeletalMeshAreaWeightedTriangleSampler(reader)

    @classmethod
    def default(cls):
        inst = cls.__new__(cls)
        inst.AreaWeightedTriangleSampler = FSkeletalMeshAreaWeightedTriangleSampler.default()
        return inst

    def GetValue(self):
        return {
            "AreaWeightedTriangleSampler": self.AreaWeightedTriangleSampler.GetValue()
        }
