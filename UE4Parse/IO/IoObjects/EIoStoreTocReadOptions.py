from enum import Enum


class EIoStoreTocReadOptions(Enum):
    Default = 0
    ReadDirectoryIndex = 1 << 0
    ReadTocMeta = 1 << 1
    ReadAll = ReadDirectoryIndex | ReadTocMeta

