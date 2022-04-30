from contextlib import suppress
from UE4Parse.Assets.Objects.EPackageFlags import EPackageFlags
from typing import List

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Exceptions.Exceptions import InvalidMagic, ParserException
from UE4Parse.Versions.EUEVersion import EUEVersion
from UE4Parse.Versions.EUnrealEngineObjectLicenseeUE4Version import EUnrealEngineObjectLicenseeUE4Version
from UE4Parse.Versions.EUnrealEngineObjectUE4Version import EUnrealEngineObjectUE4Version
from UE4Parse.Assets.Objects.FCompressedChunk import FCompressedChunk
from UE4Parse.Versions.FCustomVersionContainer import FCustomVersionContainer
from UE4Parse.Assets.Objects.FEngineVersion import FEngineVersion
from UE4Parse.Assets.Objects.FGenerationInfo import FGenerationInfo
from UE4Parse.Assets.Objects.FGuid import FGuid
from UE4Parse.PakFile import ECompressionFlags

PACKAGE_FILE_TAG = 0x9E2A83C1
PACKAGE_FILE_TAG_SWAPPED = 0xC1832A9E


class FPackageFileSummary:
    FileVersionUE4: EUnrealEngineObjectUE4Version
    FileVersionLicenseeUE4: EUnrealEngineObjectLicenseeUE4Version
    bUnversioned: bool = False
    CustomVersionContainer: FCustomVersionContainer

    def __init__(self, reader: BinaryStream) -> None:
        Tag = reader.readUInt32()
        if Tag != PACKAGE_FILE_TAG and Tag != PACKAGE_FILE_TAG_SWAPPED:
            raise InvalidMagic("Not a UE package")

        if Tag == PACKAGE_FILE_TAG_SWAPPED:
            raise NotImplementedError("Byte swapping for packages is not implemented")

        LegacyFileVersion = reader.readInt32()
        if LegacyFileVersion < 0:
            if LegacyFileVersion < -7:
                raise ParserException("Can not load UE3 packages.")
            if LegacyFileVersion != -4:
                reader.readInt32()  # VersionUE3

            version = reader.readInt32()
            self.FileVersionUE4 = EUnrealEngineObjectUE4Version(version)  # version

            self.FileVersionLicenseeUE4 = EUnrealEngineObjectLicenseeUE4Version(reader.readInt32())  # Licensee Version
            if LegacyFileVersion <= -2:
                self.CustomVersionContainer = FCustomVersionContainer(reader)

            if self.FileVersionUE4.value != 0 and self.FileVersionLicenseeUE4.value != 0:
                self.bUnversioned = True
        else:
            raise ParserException("Can not load UE3 packages.")

        self.TotalHeaderSize = reader.readInt32()
        self.FolderName = reader.readFString()

        self.PackageFlags = reader.readUInt32()
        with suppress(ValueError):
            self.PackageFlags = EPackageFlags(self.PackageFlags)

        self.NameCount = reader.readInt32()
        self.NameOffset = reader.readInt32()

        if self.FileVersionUE4.value >= EUnrealEngineObjectUE4Version.VER_UE4_ADDED_PACKAGE_SUMMARY_LOCALIZATION_ID.value:
            self.LocalizationId = reader.readFString()

        if self.FileVersionUE4.value >= EUnrealEngineObjectUE4Version.VER_UE4_SERIALIZE_TEXT_IN_PACKAGES.value or self.FileVersionUE4.value == 0:
            self.GatherableTextDataCount = reader.readInt32()
            self.GatherableTextDataOffset = reader.readInt32()

        self.ExportCount = reader.readInt32()
        self.ExportOffset = reader.readInt32()
        self.ImportCount = reader.readInt32()
        self.ImportOffset = reader.readInt32()
        self.DependsOffset = reader.readInt32()
        if self.FileVersionUE4.value >= EUnrealEngineObjectUE4Version.VER_UE4_ADD_STRING_ASSET_REFERENCES_MAP.value or self.FileVersionUE4.value == 0:
            self.SoftPackageReferencesCount = reader.readInt32()
            self.SoftPackageReferencesOffset = reader.readInt32()

        if self.FileVersionUE4.value >= EUnrealEngineObjectUE4Version.VER_UE4_ADDED_SEARCHABLE_NAMES.value or self.FileVersionUE4.value == 0:
            self.SearchableNamesOffset = reader.readInt32()

        self.ThumbnailTableOffset = reader.readInt32()
        self.Guid = FGuid(reader)

        if reader.game == EUEVersion.GAME_VALORANT:
            reader.readInt64()  # valorant

        self.GenerationCount = reader.readInt32()
        self.Generations = []
        if self.GenerationCount > 0:
            for _ in range(self.GenerationCount):
                self.Generations.append(FGenerationInfo(reader))

        if self.FileVersionUE4.value >= EUnrealEngineObjectUE4Version.VER_UE4_ENGINE_VERSION_OBJECT.value or self.FileVersionUE4.value == 0:
            self.SavedByEngineVersion = FEngineVersion(reader)

        if self.GetFileVersionUE4().value >= EUnrealEngineObjectUE4Version.VER_UE4_PACKAGE_SUMMARY_HAS_COMPATIBLE_ENGINE_VERSION.value or self.FileVersionUE4.value == 0:
            self.CompatibleWithEngineVersion = FEngineVersion(reader)

        self.CompressionFlags = ECompressionFlags(reader.readUInt32())
        if self.CompressionFlags.name != "COMPRESS_None":
            raise ParserException(f"Incompatible compression flags {self.CompressionFlags.name}")

        self.CompressedChunks: List[FCompressedChunk] = reader.readTArray(FCompressedChunk)
        if len(self.CompressedChunks) != 0:  # "CompressedChunks"
            raise ParserException("Package level compression is enabled")

        self.PackageSource = reader.readUInt32()
        self.AdditionalPackagesToCook = reader.readTArray(reader.readFString)  # AdditionalPackagesToCook

        if LegacyFileVersion > -7:
            if reader.readInt32() != 0:  # "NumTextureAllocations"
                raise ParserException("Can't load legacy UE3 file")

        # if reader.Ver >= VER_UE4_ASSET_REGISTRY_TAGS
        self.AssetRegistryDataOffset = reader.readInt32()

        self.BulkDataStartOffset = reader.readInt64()
        self.WorldTileInfoDataOffset = reader.readInt32()
        self.ChunkIDs = reader.readTArray(reader.readInt32)
        self.PreloadDependencyCount = reader.readInt32()
        self.PreloadDependencyOffset = reader.readInt32()

    def GetFileVersionUE4(self):
        return self.FileVersionUE4

    def GetCustomVersions(self):
        return self.CustomVersionContainer
