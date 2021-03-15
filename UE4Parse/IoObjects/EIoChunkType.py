from enum import auto, IntEnum


class EIoChunkType(IntEnum):
    Invalid = 0
    InstallManifest = auto()
    ExportBundleData = auto()
    BulkData = auto()
    OptionalBulkData = auto()
    MemoryMappedBulkData = auto()
    LoaderGlobalMeta = auto()
    LoaderInitialLoadMeta = auto()
    LoaderGlobalNames = auto()
    LoaderGlobalNameHashes = auto()
    ContainerHeader = auto()
