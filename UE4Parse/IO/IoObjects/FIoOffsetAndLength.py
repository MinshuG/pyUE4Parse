from UE4Parse.BinaryReader import BinaryStream


class FIoOffsetAndLength(object):
    OffsetAndLength: bytes

    # We use 5 bytes for offset and size, this is enough to represent
    # an offset and size of 1PB
    def __init__(self, reader: BinaryStream):
        self.OffsetAndLength = reader.readBytes(5 + 5)

    @property
    def GetOffset(self):
        return self.OffsetAndLength[4] | \
            (self.OffsetAndLength[3] << 8) | \
            (self.OffsetAndLength[2] << 16) | \
            (self.OffsetAndLength[1] << 24) | \
            (self.OffsetAndLength[0] << 32)

    @property
    def GetLength(self):
        return self.OffsetAndLength[9] | \
               (self.OffsetAndLength[8] << 8) | \
               (self.OffsetAndLength[7] << 16) | \
               (self.OffsetAndLength[6] << 24) | \
               (self.OffsetAndLength[5] << 32)
