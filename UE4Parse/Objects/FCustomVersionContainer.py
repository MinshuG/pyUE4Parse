from UE4Parse.Objects.FGuid import FGuid
from UE4Parse.Objects import FCustomVersion
from UE4Parse.BinaryReader import BinaryStream


class FCustomVersionContainer:
    Versions: FCustomVersion = []

    def __init__(self, reader: BinaryStream) -> None:
        self.Versions = reader.readTArray(FGuid)  # hmm

