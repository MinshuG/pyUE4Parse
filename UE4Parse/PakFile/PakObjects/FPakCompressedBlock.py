
class FPakCompressedBlock:
    CompressedStart = 0
    CompressedEnd = 0
    Size = 0

    def __init__(self, reader, start=0, end=0):
        if reader is not None:
            self.CompressedStart = reader.readInt64()
            self.CompressedEnd = reader.readInt64()
            self.Size = self.CompressedStart - self.CompressedEnd
        else:
            self.CompressedStart = start
            self.CompressedEnd = end
            self.Size = self.CompressedStart - self.CompressedEnd
