from typing import List, Optional

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Objects.FCustomVersion import FCustomVersion


class FCustomVersionContainer:
    Versions: List[FCustomVersion] = []

    def __init__(self, reader: BinaryStream) -> None:
        self.Versions = reader.readTArray_W_Arg(FCustomVersion, reader)

    def GetVersion(self, key) -> Optional[int]:
        for ver in self.Versions:
            if ver.key == key:
                return ver.Version
        return None
