from enum import IntEnum



class ELocMetaVersion(IntEnum):
    Initial = 0
    LatestPlusOne = 1
    Latest = LatestPlusOne - 1

class ELocResVersion(IntEnum):
    # Legacy format file - will be missing the magic number.
    Legacy = 0
    # Compact format file - strings are stored in a LUT to avoid duplication.
    Compact = 1
    # Optimized format file - namespaces/keys are pre-hashed (CRC32), we know the number of elements up-front, and the number of references for each string in the LUT (to allow stealing).
    Optimized_CRC32 = 2
    # Optimized format file - namespaces/keys are pre-hashed (CityHash64, UTF-16), we know the number of elements up-front, and the number of references for each string in the LUT (to allow stealing).
    Optimized_CityHash64_UTF16 = 3

    LatestPlusOne = 4
    Latest = LatestPlusOne - 1
