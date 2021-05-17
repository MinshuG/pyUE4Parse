from typing import List

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Objects.FCustomVersion import FCustomVersion


class FCustomVersionContainer:
    Versions: List[FCustomVersion] = []

    def __init__(self, reader: BinaryStream) -> None:
        self.Versions = reader.readTArray_W_Arg(FCustomVersion, reader)

