from enum import IntEnum, auto

from UE4Parse.Assets.Objects.FGuid import FGuid
from UE4Parse.Readers.FAssetReader import FAssetReader
from UE4Parse.Versions import EUEVersion
from UE4Parse.Versions.EUeBase import EUeBase


class FCoreObjectVersion(EUeBase):
    """Custom serialization version for changes made in Dev-Core stream"""
    class Type(IntEnum):
        # Before any version changes were made
        BeforeCustomVersionWasAdded = 0,
        MaterialInputNativeSerialize = 1
        EnumProperties = 2
        SkeletalMaterialEditorDataStripping = 3
        FProperties = 4

        # -----<new versions can be added above this line>-------------------------------------------------
        VersionPlusOne = auto()
        LatestVersion = VersionPlusOne - 1

    GUID = FGuid(0x375EC13C, 0x06E448FB, 0xB50084F0, 0x262A717E)

    def __init__(self):
        super().__init__()

    def get(self, reader: FAssetReader):
        ver = reader.CustomVer(self.GUID)
        if ver > 0:
            return self.Type(ver)

        if reader.game < EUEVersion.GAME_UE4_12:
            return self.Type.BeforeCustomVersionWasAdded
        elif reader.game < EUEVersion.GAME_UE4_15:
            return self.Type.MaterialInputNativeSerialize
        elif reader.game < EUEVersion.GAME_UE4_22:
            return self.Type.EnumProperties
        elif reader.game < EUEVersion.GAME_UE4_25:
            return self.Type.SkeletalMaterialEditorDataStripping
        else:
            return self.Type.LatestVersion
