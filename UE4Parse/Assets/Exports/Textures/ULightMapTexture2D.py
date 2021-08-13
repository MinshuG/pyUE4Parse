from enum import IntEnum
from typing import Union
from contextlib import suppress

from UE4Parse.Assets.Exports.Textures import UTexture2D
from UE4Parse.Assets.Exports.ExportRegistry import register_export


class ELightMapFlags(IntEnum):
    """
    Bit-field flags that affects storage (e.g. packing, streaming) and other info about a lightmap.
    """
    LMF_None = 0  # No flags
    LMF_Streamed = 0x00000001  # Lightmap should be placed in a streaming
    LMF_LQLightmap = 0x00000002  # Whether this is a low quality lightmap or not # removed not there anymore


@register_export
class ULightMapTexture2D(UTexture2D):
    """A 2D texture containing lightmap coefficients."""
    LightmapFlags: Union[int, ELightMapFlags]

    def __init__(self, reader):
        super().__init__(reader)

    def deserialize(self, validpos):
        super().deserialize(validpos)
        reader = self.reader
        self.LightmapFlags = reader.readUInt32()

        with suppress(ValueError):
            self.LightmapFlags = ELightMapFlags(self.LightmapFlags)

    def GetValue(self):
        props = super().GetValue()
        props["LightmapFlags"] = self.LightmapFlags.value if isinstance(self.LightmapFlags,
                                                                     IntEnum) else self.LightmapFlags
        return props
