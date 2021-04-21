from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Objects.Structs.Vector import FVector


class FBoxSphereBounds:
    Origin: FVector
    BoxExtent: FVector
    SphereRadius: float

    def __init__(self, reader: BinaryStream):
        self.Origin = FVector(reader)
        self.BoxExtent = FVector(reader)
        self.SphereRadius = reader.readFloat()
