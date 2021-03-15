from UE4Parse.Globals import FGame
from UE4Parse.Objects.EUEVersion import EUEVersion


def val(val):
    return EUEVersion(val).value


class FRenderingObjectVersion:
    BeforeCustomVersionWasAdded = 0
    TextureStreamingMeshUVChannelData = 10
    IncreaseNormalPrecision = 26
    StaticMeshSectionForceOpaqueField = 37
    LatestVersion = StaticMeshSectionForceOpaqueField

    def get(self):
        version = FGame.UEVersion.value

        if version < val(12):
            return self.BeforeCustomVersionWasAdded
        elif version < val(13):
            return 2
        elif version < val(14):
            return 4
        elif version < val(16):
            return 12  # 4.14 and 4.15
        elif version < val(17):
            return 15
        elif version < val(18):
            return 19
        elif version < val(19):
            return 20
        elif version < val(20):
            return 25
        elif version < val(21):
            return self.IncreaseNormalPrecision
        elif version < val(22):
            return 27
        elif version < val(23):
            return 28
        elif version < val(24):
            return 31
        elif version < val(25):
            return 36
        elif version < val(26):
            return 43
        else:
            return EUEVersion.LATEST
