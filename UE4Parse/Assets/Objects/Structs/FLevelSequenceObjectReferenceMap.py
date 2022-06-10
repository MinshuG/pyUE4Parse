from UE4Parse.Assets.Objects.Common import StructInterface
from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Assets.Objects.FGuid import FGuid
from UE4Parse.Assets.Objects.FLevelSequenceLegacyObjectReference import FLevelSequenceLegacyObjectReference


class FLevelSequenceObjectReferenceMap(StructInterface):
    position: int
    Map: dict

    def __init__(self, reader: BinaryStream) -> None:
        self.position = reader.base_stream.tell()
        length = reader.readInt32()

        for _ in range(length):
            self.Map[FGuid(reader)] = FLevelSequenceLegacyObjectReference(reader)

    @classmethod
    def default(cls):
        inst = cls.__new__(cls)
        inst.Map = {}
        return inst

    def GetValue(self):
        return {x.GetValue() : y.GetValue() for x, y in self.Map.items()}
