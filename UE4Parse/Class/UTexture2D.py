from typing import List

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Globals import FGame
from UE4Parse.Logger import get_logger
from UE4Parse.Objects.FStripDataFlags import FStripDataFlags
from UE4Parse.PakFile.PakObjects.EPakVersion import EPakVersion
from UE4Parse.Textures.Objects.FTexturePlatformData import FTexturePlatformData

logger = get_logger(__name__)


class UTexture2D:
    data: List[FTexturePlatformData]

    def __init__(self, reader: BinaryStream, bulk: BinaryStream, bulkOffset) -> None:
        FStripDataFlags(reader)
        FStripDataFlags(reader)

        bIsCooked = reader.readInt32() != 0
        if bIsCooked:
            data = []
            PixelFormatName = reader.readFName()
            pos = reader.base_stream.tell()
            while not PixelFormatName.isNone:
                try:
                    SkipOffset = reader.readInt64()

                    data.append(FTexturePlatformData(reader, ubulk=bulk, ubulkOffset=bulkOffset))

                    PixelFormatName = reader.readFName()

                    if FGame.Version.value < EPakVersion.RELATIVE_CHUNK_OFFSETS.value:
                        break
                    self.data = data
                except Exception as e:
                    logger.debug("Error occurred while reading Texture2D")
                    break

            # self.image = self.getimage()

    def GetValue(self, position_value_type: bool = False):
        return {"FTexturePlatformData": [x.GetValue() for x in self.data]}

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
