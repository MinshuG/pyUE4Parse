from typing import List

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Versions.EUEVersion import Versions, GAME_UE4


class FRawStaticIndexBuffer:
    indices16: List[int]
    indices32: List[int]

    def __init__(self, reader: BinaryStream):
        if reader.version < Versions.VER_UE4_SUPPORT_32BIT_STATIC_MESH_INDICES:
            self.indices16 = reader.readBulkTArray(reader.readUInt16)
            self.indices32 = []
        else:
            is32bit = reader.readBool()
            data = bytearray(reader.readBulkTArray(reader.readInt8))

            tr = BinaryStream(data)
            tr.game = reader.game
            tr.version = reader.version

            if reader.game >= GAME_UE4(25):
                reader.readBool()

            if len(data) == 0:
                self.indices16 = []
                self.indices32 = []
                return

            if is32bit:
                count = int(len(data) / 4)
                self.indices32 = [tr.readUInt32() for _ in range(count)]
                self.indices16 = []
            else:
                count = int(len(data) / 2)
                self.indices16 = [tr.readUInt16() for _ in range(count)]
                self.indices32 = []

    def GetValue(self):
        return {
            "indices16": self.indices16,
            "indices32": self.indices32
        }
