from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Versions.EUEVersion import GAME_UE4


class FEditorObjectVersion:
    BeforeCustomVersionWasAdded = 0
    RefactorMeshEditorMaterials = 8
    UPropertryForMeshSection = 10
    AddedMorphTargetSectionIndices = 23
    StaticMeshDeprecatedRawMesh = 28
    LatestVersion = StaticMeshDeprecatedRawMesh

    def __init__(self):
        pass

    def get(self, reader: BinaryStream):
        if reader.game < GAME_UE4(12): return self.BeforeCustomVersionWasAdded
        if reader.game < GAME_UE4(13): return 2
        if reader.game < GAME_UE4(14): return 6
        if reader.game < GAME_UE4(15): return self.RefactorMeshEditorMaterials
        if reader.game < GAME_UE4(16): return 14
        if reader.game < GAME_UE4(17): return 17
        if reader.game < GAME_UE4(19): return 20
        if reader.game < GAME_UE4(20): return self.AddedMorphTargetSectionIndices
        if reader.game < GAME_UE4(21): return 24
        if reader.game < GAME_UE4(22): return 26
        if reader.game < GAME_UE4(23): return 30
        if reader.game < GAME_UE4(24): return 34
        if reader.game < GAME_UE4(25): return 37
        if reader.game < GAME_UE4(26): return 38
        return self.LatestVersion
