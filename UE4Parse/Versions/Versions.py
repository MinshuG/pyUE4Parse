from typing import Optional

from UE4Parse.Versions.EUEVersion import EUEVersion


class VersionContainer:
    UEVersion: EUEVersion = EUEVersion.LATEST

    def __init__(self, ue_version) -> None:
        self.UEVersion = ue_version

    @classmethod
    def default(cls):
        return cls(EUEVersion.LATEST)
