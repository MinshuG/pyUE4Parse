from io import BytesIO
from typing import Tuple
from UE4Parse.Assets.Exports.UObjects import UObject
from UE4Parse.Assets.Exports.ExportRegistry import register_export
from UE4Parse.Readers.FAssetReader import FAssetReader
from UE4Parse.Assets.Objects.FByteBulkData import FByteBulkData



class FAkMediaDataChunk:
    IsPrefetch: bool
    Data: FByteBulkData

    def __init__(self, reader: FAssetReader) -> None:
        self.IsPrefetch = reader.readBool()
        self.Data = FByteBulkData(reader, reader.ubulk_stream, -1)


@register_export
class UAkMediaAssetData(UObject):
    IsStreamed: bool
    UseDeviceMemory: bool
    DataChunks: Tuple[FAkMediaDataChunk]

    def __init__(self, reader: FAssetReader):
        super().__init__(reader)

    def deserialize(self, validpos):
        super().deserialize(validpos)
        reader = self.reader

        self.IsStreamed = self.try_get("IsStreamed", False)
        self.UseDeviceMemory = self.try_get("UseDeviceMemory", False)
        self.DataChunks = reader.readTArray(FAkMediaDataChunk, reader)

    def decode(self) -> BytesIO:
        out = BytesIO()
        for chunk in self.DataChunks:
            out.write(chunk.Data.Data)

        return out
