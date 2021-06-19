from .Level import ULevel
from .MaterialInstanceConstant import UMaterialInstanceConstant
from .UObjects import UObject
from .UStaticMesh import UStaticMesh
from .UStringTable import UStringTable
from .UTexture2D import UTexture2D
from .World import UWorld



class Registry:
    exports = {
        "Texture2D": UTexture2D,
        "StaticMesh": UStaticMesh,
        "StringTable": UStringTable,
        "World": UWorld,
        "Level": ULevel,
        "MaterialInstanceConstant": UMaterialInstanceConstant
    }

    def __init__(self) -> None:
        pass

    def get_export_reader(self, export_type: str, export, reader):
        r = self.exports.get(export_type, UObject)(reader)
        r.type = export_type
        r.flag = export.ObjectFlags
        # r.name = export.ObjectName.string
        return r
