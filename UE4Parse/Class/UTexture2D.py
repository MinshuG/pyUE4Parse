from typing import List, Optional

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Class.UObjects import UObject
from UE4Parse.Globals import FGame
from UE4Parse.Logger import get_logger
from UE4Parse.Objects.EPixelFormat import EPixelFormat
from UE4Parse.Objects.EUEVersion import GAME_UE4, Versions
from UE4Parse.Objects.FGuid import FGuid
from UE4Parse.Objects.FStripDataFlags import FStripDataFlags
from UE4Parse.PakFile.PakObjects.EPakVersion import EPakVersion
from UE4Parse.Textures.Objects.FTexturePlatformData import FTexturePlatformData

logger = get_logger(__name__)


class UTexture2D(UObject):
    data: List[FTexturePlatformData] = []

    def __init__(self, reader: BinaryStream, bulk: Optional[BinaryStream], bulkOffset) -> None:
        super().__init__(reader)
        FStripDataFlags(reader)
        FStripDataFlags(reader)

        # if reader.version < Versions.VER_UE4_TEXTURE_SOURCE_ART_REFACTOR:
        #     FGuid(reader)
        if FGame.GameName.lower() == "shootergame":  # Custom game?
            reader.seek(4)

        bIsCooked = reader.readBool()
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

                if FGame.Version.value < EPakVersion.RELATIVE_CHUNK_OFFSETS.value:
                    break

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
