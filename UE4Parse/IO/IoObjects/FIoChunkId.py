from UE4Parse.BinaryReader import BinaryStream, convert_each_byte_to_int
from UE4Parse.IoObjects.EIoChunkType import EIoChunkType


class FIoChunkId:
    Id: int
    raw: bytes

    def __init__(self, reader: BinaryStream = None):
        if reader is not None:
            self.raw = reader.readBytes(12)
            self.Id = convert_each_byte_to_int(self.raw)

    @property
    def ChunkId(self) -> int:
        return int.from_bytes(bytearray(self.raw)[:8], "little", signed=False)

    def construct(self, chunkId: int, chunkIndex: int, ioChunkType: EIoChunkType):  # ??
        buffer = bytearray()
        for x in chunkId.to_bytes(8, "little", signed=False):
            buffer.append(x)
        for x in chunkIndex.to_bytes(4, "little", signed=False):
            buffer.append(x)

        buffer[11] = ioChunkType.value
        self.raw = buffer
        self.Id = convert_each_byte_to_int(buffer)
        return self


if __name__ == "__main__":
    yeet = FIoChunkId().construct(8610797960815396523, 0, EIoChunkType.ContainerHeader)
