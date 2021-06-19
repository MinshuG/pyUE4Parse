from typing import List

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Class.UObjects import UObject
from UE4Parse.Logger import get_logger
from UE4Parse.Objects.EPixelFormat import EPixelFormat
from UE4Parse.Objects.EUEVersion import GAME_UE4, Versions
from UE4Parse.Objects.FStripDataFlags import FStripDataFlags
from UE4Parse.PakFile.PakObjects.EPakVersion import EPakVersion
from UE4Parse.Textures.Objects.FTexturePlatformData import FTexturePlatformData

logger = get_logger(__name__)


class UTexture2D(UObject):
    data: List[FTexturePlatformData] = []

    def __init__(self, reader: BinaryStream) -> None:
        super().__init__(reader)

    def deserialize(self, validpos):
        reader = self.reader
        bulk = reader.ubulk_stream
        bulkOffset = reader.bulk_offset
        super().deserialize(validpos)

        FStripDataFlags(reader)
        FStripDataFlags(reader)

        bIsCooked = reader.version >= Versions.VER_UE4_ADD_COOKED_TO_TEXTURE2D and reader.readBool()  # 203
        if bIsCooked:
            PixelFormatName = reader.readFName()
            pos = reader.base_stream.tell()
            while not PixelFormatName.isNone:
                SkipOffset = reader.readInt32()
                if reader.game >= GAME_UE4(20):
                    SkipOffsetH = reader.readInt32()
                    assert SkipOffsetH == 0

                data = FTexturePlatformData(reader, ubulk=bulk, ubulkOffset=bulkOffset)
                self.data.append(data)
                PixelFormatName = reader.readFName()

                try:
                    EPixelFormat[PixelFormatName.GetValue()]
                except:
                    break

        # self.Dict["FTexturePlatformData"] = self.data

    # def GetValue(self, position_value_type: bool = False):
    #     return {"FTexturePlatformData": [x.GetValue() for x in self.data]}.update(super(UTexture2D, self).GetValue())

    # def getimage(self):
    #     if self.image == None:
    #         sizeX = 0
    #         sizeY = 0
    #         sizeZ = 0
    #         data: bytes = None
    #         PlatformDatas = self.data
    #         for PlatformData in PlatformDatas:
    #             if len(PlatformData.Mips) > 0:
    #                 i = PlatformData.FirstMipToSerialize
    #                 data = PlatformData.Mips[i].BulkData.Data
    #
    #                 sizeX = PlatformData.Mips[i].SizeX
    #                 sizeY = PlatformData.Mips[i].SizeY
    #                 sizeZ = PlatformData.Mips[i].SizeZ
    #
    #                 # image = TDecoder.DecodeImage(data, sizeX, sizeY, sizeZ, PlatformData.PixelFormat)
    #
    #                 # return image
