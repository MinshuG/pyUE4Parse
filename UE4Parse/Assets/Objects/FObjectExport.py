from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Assets.Exports.UObjects import UObject
from UE4Parse.Assets.Objects.EObjectFlags import EObjectFlags
from UE4Parse.Versions.EUnrealEngineObjectUE4Version import EUnrealEngineObjectUE4Version
from UE4Parse.Assets.Objects.FGuid import FGuid
from UE4Parse.Assets.Objects.FName import FName
from UE4Parse.Assets.Objects.FPackageIndex import FPackageIndex


class FObjectExport:
    ClassIndex: FPackageIndex
    SuperIndex: FPackageIndex
    TemplateIndex: FPackageIndex
    OuterIndex: FPackageIndex
    ObjectName: FName
    ObjectFlags: EObjectFlags
    SerialSize: int
    SerialOffset: int
    bForcedExport: bool
    bNotForClient: bool
    bNotForServer: bool
    PackageGuid: FGuid
    PackageFlags: int
    bNotAlwaysLoadedForEditorGame: bool = True
    bIsAsset: bool = False
    exportObject: UObject
    name: FName = None
    type: FName = FName("Unknown")

    @property
    def name(self) -> FName:
        return self.ObjectName

    def __init__(self, reader: BinaryStream) -> None:
        self.ClassIndex = FPackageIndex(reader)
        self.SuperIndex = FPackageIndex(reader)

        # only serialize when file version is past VER_UE4_TemplateIndex_IN_COOKED_EXPORTS
        if reader.version >= EUnrealEngineObjectUE4Version.VER_UE4_TemplateIndex_IN_COOKED_EXPORTS.value:
            self.TemplateIndex = FPackageIndex(reader)

        self.OuterIndex = FPackageIndex(reader)
        self.ObjectName = reader.readFName()

        self.ObjectFlags = reader.readUInt32()
        try:
            self.ObjectFlags = EObjectFlags(self.ObjectFlags)# & EObjectFlags.RF_Load.value
        except:
            pass

        # only serialize when file version is past VER_UE4_64BIT_EXPORTMAP_SERIALSIZES
        if reader.version >= EUnrealEngineObjectUE4Version.VER_UE4_64BIT_EXPORTMAP_SERIALSIZES:
            self.SerialSize = reader.readInt64()
            self.SerialOffset = reader.readInt64()
        else:
            self.SerialSize = reader.readInt32()
            self.SerialOffset = reader.readInt32()

        self.bForcedExport = reader.readInt32() != 0
        self.bNotForClient = reader.readInt32() != 0
        self.bNotForServer = reader.readInt32() != 0

        self.PackageGuid = FGuid(reader)
        self.PackageFlags = reader.readUInt32()

        # only serialize when file version is past VER_UE4_LOAD_FOR_EDITOR_GAME
        if reader.version >= EUnrealEngineObjectUE4Version.VER_UE4_LOAD_FOR_EDITOR_GAME:
            self.bNotAlwaysLoadedForEditorGame = reader.readBool()

        # only serialize when file version is past VER_UE4_COOKED_ASSETS_IN_EDITOR_SUPPORT
        if reader.version >= EUnrealEngineObjectUE4Version.VER_UE4_COOKED_ASSETS_IN_EDITOR_SUPPORT:
            self.bIsAsset = reader.readBool()

        # only serialize when file version is past VER_UE4_PRELOAD_DEPENDENCIES_IN_COOKED_EXPORTS
        if reader.version >= EUnrealEngineObjectUE4Version.VER_UE4_PRELOAD_DEPENDENCIES_IN_COOKED_EXPORTS:
            self.FirstExportDependency = reader.readInt32()
            self.SerializationBeforeSerializationDependencies = reader.readInt32()
            self.CreateBeforeSerializationDependencies = reader.readInt32()
            self.SerializationBeforeCreateDependencies = reader.readInt32()
            self.CreateBeforeCreateDependencies = reader.readInt32()
        else:
            self.FirstExportDependency = -1
            self.SerializationBeforeSerializationDependencies = 0
            self.CreateBeforeSerializationDependencies = 0
            self.SerializationBeforeCreateDependencies = 0
            self.CreateBeforeCreateDependencies = 0

    def __str__(self):
        return f"FObjectExport(Name: {self.name.string} Type: {self.type.string})"

    def GetValue(self):
        return {
            "ClassIndex": self.ClassIndex.GetValue(),
            "SuperIndex": self.SuperIndex.GetValue(),
            "OuterIndex": self.OuterIndex.GetValue(),
            "ObjectName": self.ObjectName.GetValue()
        }
