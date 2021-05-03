from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Objects.Structs.Vector import FVector
from UE4Parse.Class.UClass import UClass


class FBoxSphereBounds(UClass):
    Origin: FVector
    BoxExtent: FVector
    SphereRadius: float

    def __init__(self, reader: BinaryStream):
        super().__init__()
        self.Origin = FVector(reader)
        self.BoxExtent = FVector(reader)
        self.SphereRadius = reader.readFloat()
