from typing import Optional

from UE4Parse.Versions.EUEVersion import EUEVersion


class VersionContainer:
    UEVersion: EUEVersion = EUEVersion.LATEST
    GameName: Optional[str] = None
