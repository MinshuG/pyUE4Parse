from .Level import ULevel
from .MaterialInstanceConstant import UMaterialInstanceConstant
from .UObjects import UObject
from .UStaticMesh import UStaticMesh
from .UStringTable import UStringTable
from .UTexture2D import UTexture2D
from .World import UWorld


exports = {
    "Texture2D": UTexture2D,
    "StaticMesh": UStaticMesh,
    "StringTable": UStringTable,
    "World": UWorld,
    "Level": ULevel,
    "MaterialInstanceConstant": UMaterialInstanceConstant
}


def get_export_reader(export_type: str):
    return exports.get(export_type, UObject)
