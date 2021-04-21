# from UE4Parse.IoObjects import FIoGlobalData
from typing import Optional

from UE4Parse.Objects.EUEVersion import EUEVersion
from UE4Parse.PakFile.PakObjects.EPakVersion import EPakVersion


class Globals:
    PackageReader = None
    Index = {}
    Paks = {}
    IoStores = {}
    GlobalData: object
    Triggers = {}


class FGame:
    UEVersion: EUEVersion = EUEVersion.LATEST
    GameName: Optional[str] = None
    Version: EPakVersion = EPakVersion(11)
    SubVersion = 0
