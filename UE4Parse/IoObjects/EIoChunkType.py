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

class EIoChunkType5(IntEnum):
    Invalid = 0
    ExportBundleData = 1
    BulkData = 2
    OptionalBulkData = 3
    MemoryMappedBulkData = 4
    ScriptObjects = 5
    ContainerHeader = 6
    ExternalFile = 7
    ShaderCodeLibrary = 8
    ShaderCode = 9
    PackageStoreEntry = 10
