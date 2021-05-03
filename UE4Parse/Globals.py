from typing import Optional, Any

from UE4Parse.Objects.EUEVersion import EUEVersion
from UE4Parse.PakFile.PakObjects.EPakVersion import EPakVersion


class Globals: # TODO get rid of this
    PackageReader = None
    Index = {}
    ChunkIDs = {}
    Paks = {}
    IoStores = {}
    GlobalData: Any  # FIoGlobalData
    Triggers = {}


class FGame:
    UEVersion: EUEVersion = EUEVersion.LATEST
    GameName: Optional[str] = None
    Version: EPakVersion = EPakVersion(11)
    SubVersion = 0
