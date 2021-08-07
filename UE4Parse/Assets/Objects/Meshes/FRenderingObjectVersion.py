from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Versions.EUEVersion import EUEVersion, GAME_UE4


class FRenderingObjectVersion:
    BeforeCustomVersionWasAdded = 0
    TextureStreamingMeshUVChannelData = 10
    IncreaseNormalPrecision = 26
    StaticMeshSectionForceOpaqueField = 37
    LatestVersion = StaticMeshSectionForceOpaqueField

    def __init__(self):
        pass
 
    def get(self, reader: BinaryStream):
        version = reader.game
        if version < GAME_UE4(12):
            return self.BeforeCustomVersionWasAdded
        elif version < GAME_UE4(13):
            return 2
        elif version < GAME_UE4(14):
            return 4
        elif version < GAME_UE4(16):
            return 12  # 4.14 and 4.15
        elif version < GAME_UE4(17):
            return 15
        elif version < GAME_UE4(18):
            return 19
        elif version < GAME_UE4(19):
            return 20
        elif version < GAME_UE4(20):
            return 25
        elif version < GAME_UE4(21):
            return self.IncreaseNormalPrecision
        elif version < GAME_UE4(22):
            return 27
        elif version < GAME_UE4(23):
            return 28
        elif version < GAME_UE4(24):
            return 31
        elif version < GAME_UE4(25):
            return 36
        elif version < GAME_UE4(26):
            return 43
        else:
            return EUEVersion.LATEST
