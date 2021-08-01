from typing import List

from UE4Parse.BinaryReader import BinaryStream

TEXSTREAM_MAX_NUM_UVCHANNELS = 4


class FMeshUVChannelInfo:
    bInitialized: bool
    bOverrideDensities: bool
    LocalUVDensities: List[float]

    def __init__(self, reader: BinaryStream):
        self.bInitialized = reader.readBool()
        self.bOverrideDensities = reader.readBool()
        self.LocalUVDensities = [reader.readFloat() for _ in range(TEXSTREAM_MAX_NUM_UVCHANNELS)]
