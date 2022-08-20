from io import BytesIO
from typing import Dict, Optional, Tuple
from UE4Parse.Assets.Exports.UObjects import UObject
from UE4Parse.Assets.Exports.ExportRegistry import register_export
from UE4Parse.Assets.Objects.FGuid import FGuid
from UE4Parse.Assets.Objects.FName import FName
from UE4Parse.Exceptions.Exceptions import ParserException
from UE4Parse.Readers.FAssetReader import FAssetReader
from UE4Parse.Versions import EUEVersion
from UE4Parse.Versions.EUnrealEngineObjectUE4Version import EUnrealEngineObjectUE4Version
from UE4Parse.Versions.FFrameworkObjectVersion import FFrameworkObjectVersion
from UE4Parse.Assets.Objects.FByteBulkData import FByteBulkData


class FFormatContainer:
    Formats: Dict[str, FByteBulkData]

    def __init__(self, reader: FAssetReader):
        self.Formats = {}
        for i in range(reader.readInt32()):
            self.Formats[reader.readFName()] = FByteBulkData(reader, reader.ubulk_stream, -1)

class FStreamedAudioChunk:
    DataSize: int
    AudioDataSize: int
    BulkData: FByteBulkData

    def __init__(self, reader: FAssetReader):
        if (reader.readBool()):
            self.BulkData = FByteBulkData(reader, reader.ubulk_stream, -1)
            self.DataSize = reader.readInt32()
            self.AudioDataSize = reader.readInt32()
        else:
            reader.seek(-4, 1)
            raise ParserException("Streamed audio chunk must be cooked")

class FStreamedAudioPlatformData:
    NumChunks: int
    AudioFormat: FName
    Chunks: Tuple[FStreamedAudioChunk]

    def __init__(self, reader: FAssetReader):
        self.NumChunks = reader.readInt32()
        self.AudioFormat = reader.readFName()
        self.Chunks = reader.readTArray2(FStreamedAudioChunk, self.NumChunks, reader)


class USoundBase(UObject): pass

@register_export
class USoundWave(USoundBase):
    bStreaming: bool
    bCooked: bool
    CompressedFormatData: Optional[FFormatContainer]
    RawData: Optional[FByteBulkData]
    CompressedDataGuid: FGuid

    def __init__(self, reader: FAssetReader):
        super().__init__(reader)

    def deserialize(self, validpos):
        super().deserialize(validpos)
        reader = self.reader

        self.bStreaming = reader.game >= EUEVersion.GAME_UE4_25
        if (bstreaming := self.try_get("bStreaming", False)):
            self.bStreaming = bstreaming

        self.bCooked = reader.readBool()

        if reader.version >= EUnrealEngineObjectUE4Version.VER_UE4_SOUND_COMPRESSION_TYPE_ADDED and FFrameworkObjectVersion().get(reader) < FFrameworkObjectVersion.Type.RemoveSoundWaveCompressionName:
            reader.readFName() # DummyCompressionName

        if not self.bStreaming:
            if self.bCooked:
                self.RawData = None
                self.CompressedFormatData = FFormatContainer(reader)
            else:
                self.CompressedFormatData = None
                self.RawData = FByteBulkData(reader, reader.ubulk_stream, -1)

            self.CompressedDataGuid = FGuid(reader)
        else:
            self.CompressedDataGuid = FGuid(reader)
            self.RunningPlatformData  = FStreamedAudioPlatformData(reader)

    def decode(self) -> Tuple[BytesIO, str]:
        out = BytesIO()
        if not self.bStreaming:
            if self.bCooked:
                out = BytesIO(self.CompressedFormatData.Formats.values()[0].Data)
                format = self.CompressedFormatData.Formats.keys()[0].string
                return out, format
            else:
                raise NotImplementedError("Raw data not implemented")
        else:
            for chunk in self.RunningPlatformData.Chunks:
                out.write(chunk.BulkData.Data)
            return out, self.RunningPlatformData.AudioFormat.string

