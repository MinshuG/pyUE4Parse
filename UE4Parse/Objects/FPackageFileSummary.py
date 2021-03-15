from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Globals import FGame
from UE4Parse.Objects.EUnrealEngineObjectLicenseeUE4Version import EUnrealEngineObjectLicenseeUE4Version
from UE4Parse.Objects.EUnrealEngineObjectUE4Version import EUnrealEngineObjectUE4Version
from UE4Parse.Objects.FCompressedChunk import FCompressedChunk
from UE4Parse.Objects.FCustomVersionContainer import FCustomVersionContainer
from UE4Parse.Objects.FEngineVersion import FEngineVersion
from UE4Parse.Objects.FGenerationInfo import FGenerationInfo
from UE4Parse.Objects.FGuid import FGuid
from UE4Parse.PakFile import ECompressionFlags

PACKAGE_FILE_TAG = 0x9E2A83C1
PACKAGE_FILE_TAG_SWAPPED = 0xC1832A9E


class FPackageFileSummary:
    FileVersionUE4: EUnrealEngineObjectUE4Version = None
    FileVersionLicenseeUE4: EUnrealEngineObjectLicenseeUE4Version = None
    bUnversioned: bool = False
    CustomVersionContainer = FCustomVersionContainer

    def __init__(self, reader: BinaryStream) -> None:
        Tag = reader.readUInt32()
        if Tag != PACKAGE_FILE_TAG and Tag != PACKAGE_FILE_TAG_SWAPPED:
            raise FileExistsError("Not a UE package")

        if Tag == PACKAGE_FILE_TAG_SWAPPED:
            raise NotImplementedError("Byte swapping for packages is not implemented")

        LegacyFileVersion = reader.readInt32()
        if LegacyFileVersion < 0:
            if LegacyFileVersion < -7:
                raise Exception("Can not load UE3 packages.")
            if LegacyFileVersion != -4:
                reader.readInt32()  # VersionUE3

            self.FileVersionUE4 = EUnrealEngineObjectUE4Version(reader.readInt32())  # version
            self.FileVersionLicenseeUE4 = EUnrealEngineObjectLicenseeUE4Version(reader.readInt32())  # Licensee Version
            if LegacyFileVersion <= -2:
                self.CustomVersionContainer = FCustomVersionContainer(reader)

            if self.FileVersionUE4.value != 0 and self.FileVersionLicenseeUE4.value != 0:
                self.bUnversioned = True
            FileVersion = self.FileVersionUE4.value & 0xFFFF
        else:
            raise Exception("Can not load UE3 packages.")

        self.TotalHeaderSize = reader.readInt32()
        self.FolderName = reader.readFString()

        self.PackageFlags = reader.readUInt32()
        # self.PackageFlags = EPackageFlags(self.PackageFlags)

        self.NameCount = reader.readInt32()
        self.NameOffset = reader.readInt32()

        self.GatherableTextDataCount = reader.readInt32()
        self.GatherableTextDataOffset = reader.readInt32()

        self.ExportCount = reader.readInt32()
        self.ExportOffset = reader.readInt32()
        self.ImportCount = reader.readInt32()
        self.ImportOffset = reader.readInt32()
        self.DependsOffset = reader.readInt32()

        self.SoftPackageReferencesCount = reader.readInt32()
        self.SoftPackageReferencesOffset = reader.readInt32()

        # past VER_UE4_ADDED_SEARCHABLE_NAMES
        self.SearchableNamesOffset = reader.readInt32()

        self.ThumbnailTableOffset = reader.readInt32()
        self.Guid = FGuid(reader)
        if FGame.GameName == "ShooterGame": reader.readInt64()  # valorant

        self.GenerationCount = reader.readInt32()
        self.Generations = []
        if self.GenerationCount > 0:
            for _ in range(self.GenerationCount):
                self.Generations.append(FGenerationInfo(reader))

        self.SavedByEngineVersion = FEngineVersion(reader)
        self.CompatibleWithEngineVersion = FEngineVersion(reader)

        self.CompressionFlags = ECompressionFlags(reader.readUInt32())
        if self.CompressionFlags.name != "COMPRESS_None":
            raise Exception(f"Incompatible compression flags {self.CompressionFlags.name}")

        if len(reader.readTArray(FCompressedChunk)) != 0:  # "CompressedChunks"
            raise Exception("Package level compression is enabled")

        self.PackageSource = reader.readUInt32()
        reader.readTArray(reader.readFString)  # AdditionalPackagesToCook

        if LegacyFileVersion > -7:
            if reader.readInt32() != 0:  # "NumTextureAllocations"
                raise Exception("Can't load legacy UE3 file")

        self.AssetRegistryDataOffset = reader.readInt32()
        self.BulkDataStartOffset = reader.readInt64()
        self.WorldTileInfoDataOffset = reader.readInt32()
        self.ChunkIDs = reader.readTArray(reader.readInt32)
        self.PreloadDependencyCount = reader.readInt32()
        self.PreloadDependencyOffset = reader.readInt32()
