from typing import List, Optional

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Assets.Objects.FCustomVersion import FCustomVersion


class FCustomVersionContainer:
    Versions: List[FCustomVersion] = ()

    def __init__(self, reader: BinaryStream) -> None:
        self.Versions = reader.readTArray(FCustomVersion, reader)

    def get_version(self, key) -> Optional[int]:
        for ver in self.Versions:
            if ver.key == key:
                return ver.Version
        return None
