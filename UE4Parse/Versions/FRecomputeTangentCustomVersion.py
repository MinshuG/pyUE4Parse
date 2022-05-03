from enum import auto
from UE4Parse.Assets.Objects.FGuid import FGuid
from UE4Parse.Readers.FAssetReader import FAssetReader
from UE4Parse.Versions.EUEVersion import EUEVersion
from UE4Parse.Versions.EUeBase import EUeBase


class FRecomputeTangentCustomVersion(EUeBase):
    class Type(EUeBase.Type):
        # Before any version changes were made in the plugin
        BeforeCustomVersionWasAdded = 0,
        # UE4.12
        # We serialize the RecomputeTangent Option
        RuntimeRecomputeTangent = 1,
        # UE4.26
        # Choose which Vertex Color channel to use as mask to blend tangents
        RecomputeTangentVertexColorMask = 2,
        # -----<new versions can be added above this line>-------------------------------------------------
        VersionPlusOne = auto()
        LatestVersion = VersionPlusOne - 1

    GUID = FGuid(0x5579F886, 0x933A4C1F, 0x83BA087B, 0x6361B92F)

    def get(self, reader: FAssetReader) -> "FRecomputeTangentCustomVersion.Type":
        ver = reader.CustomVer(self.GUID)
        if ver > 0:
            return self.Type(ver)

        if reader.game < EUEVersion.GAME_UE4_12:
            return self.Type.BeforeCustomVersionWasAdded
        elif reader.game < EUEVersion.GAME_UE4_15:
            return self.Type.RuntimeRecomputeTangent
        else:
            return self.Type.LatestVersion
