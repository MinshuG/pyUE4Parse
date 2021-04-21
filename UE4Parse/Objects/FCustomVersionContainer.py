from typing import List
from UE4Parse.Objects.FGuid import FGuid
from UE4Parse.Objects.FCustomVersion import FCustomVersion
from UE4Parse.BinaryReader import BinaryStream


class FCustomVersionContainer:
    Versions: List[FCustomVersion] = []

    def __init__(self, reader: BinaryStream) -> None:
        self.Versions = reader.readTArray_W_Arg(FCustomVersion, reader)

