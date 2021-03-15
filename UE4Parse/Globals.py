from UE4Parse.IoObjects import FIoGlobalData
from UE4Parse.Objects.EUEVersion import EUEVersion
from UE4Parse.PakFile.PakObjects.EPakVersion import EPakVersion


class Globals:
    PackageReader = None
    Index = {}
    Paks = {}
    IoStores = {}
    GlobalData: FIoGlobalData


class FGame:
    UEVersion: EUEVersion
    GameName = ""
    Version: EPakVersion = EPakVersion(11)
    SubVersion = 0

