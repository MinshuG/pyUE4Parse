from typing import List, Optional, TYPE_CHECKING

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Assets.Exports.UObjects import UObject
from UE4Parse.Logger import get_logger
from UE4Parse.Assets.Objects.EPixelFormat import EPixelFormat
from UE4Parse.Versions.EUEVersion import GAME_UE4, Versions
from UE4Parse.Assets.Objects.FStripDataFlags import FStripDataFlags
from UE4Parse.Assets.Exports.ExportRegistry import register_export
from UE4Parse.Assets.Exports.Textures.Objects.FTexturePlatformData import FTexturePlatformData
from .Decoder import TextureDecoder

if TYPE_CHECKING:
    from PIL.Image import Image

logger = get_logger(__name__)


@register_export
class UTexture2D(UObject):
    data: List[FTexturePlatformData]
    isNormalMap: bool

    def __init__(self, reader: BinaryStream) -> None:
        super().__init__(reader)
        self.data = []
        self.isNormalMap = False

    def deserialize(self, validpos):
        reader = self.reader
        bulk = reader.ubulk_stream
        bulkOffset = reader.bulk_offset
        super().deserialize(validpos)

        if compression_settings := self.try_get("CompressionSettings"):
            self.isNormalMap = str(compression_settings).lower().endswith("TC_Normalmap".lower())

        FStripDataFlags(reader)
        FStripDataFlags(reader)

        bIsCooked = reader.version >= Versions.VER_UE4_ADD_COOKED_TO_TEXTURE2D and reader.readBool()  # 203
        if bIsCooked:
            PixelFormatName = reader.readFName()
            while not PixelFormatName.isNone:
                if reader.game >= GAME_UE4(20):
                    SkipOffset = reader.readInt64()
                else:
                    SkipOffset = reader.readInt32()

                data = FTexturePlatformData(reader, ubulk=bulk, ubulkOffset=bulkOffset)
                self.data.append(data)
                PixelFormatName = reader.readFName()

    def GetValue(self):
        props = super().GetValue()
        props["FTexturePlatformData"] = [x.GetValue() for x in self.data]
        return props

    def decode(self, mip_index=-1) -> Optional['Image']:
        if len(self.data) == 0:
            return  # no data

        PlatformData = self.data[0]
        mip_index = PlatformData.FirstMipToSerialize if mip_index == -1 else mip_index

        Mip = PlatformData.Mips[mip_index]
        data = Mip.BulkData.Data
        if data is None:
            raise ValueError(f"mip {mip_index} doesn't have any data")

        sizeX = Mip.SizeX
        sizeY = Mip.SizeY
        sizeZ = Mip.SizeZ

        image = TextureDecoder(data, sizeX, sizeY, sizeZ, PlatformData.PixelFormat)
        image.decode(self.isNormalMap)
        return image.decoded_image
