from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Assets.Objects.Structs.Vector import FVector


class FBoxSphereBounds:
    Origin: FVector
    BoxExtent: FVector
    SphereRadius: float

    def __init__(self, reader: BinaryStream):
        super().__init__()
        self.Origin = FVector(reader)
        self.BoxExtent = FVector(reader)
        self.SphereRadius = reader.readFloat()

    def GetValue(self):
        return {
            "Origin": self.Origin.GetValue(),
            "BoxExtent": self.BoxExtent.GetValue(),
            "SphereRadius": self.SphereRadius
        }
