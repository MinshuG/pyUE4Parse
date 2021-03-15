from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Objects.FPackageIndex import FPackageIndex
from UE4Parse.Objects.FGuid import FGuid
from UE4Parse.Objects.EObjectFlags import EObjectFlags


class FObjectExport:
    def __init__(self,reader: BinaryStream) -> None:
        self.reader = reader

    def read(self):
        reader = self.reader
        self.ClassIndex =  FPackageIndex(reader)
        self.SuperIndex =  FPackageIndex(reader)

        # only serialize when file version is past VER_UE4_TemplateIndex_IN_COOKED_EXPORTS
        self.TemplateIndex =  FPackageIndex(reader)

        self.OuterIndex =  FPackageIndex(reader)
        self.ObjectName = reader.readFName()

        try: self.ObjectFlags = EObjectFlags(reader.readUInt32()) & EObjectFlags.RF_Load
        except: pass

        # only serialize when file version is past VER_UE4_64BIT_EXPORTMAP_SERIALSIZES
        self.SerialSize = reader.readInt64()
        self.SerialOffset = reader.readInt64()

        self.bForcedExport = reader.readInt32() != 0
        self.bNotForClient = reader.readInt32() != 0
        self.bNotForServer = reader.readInt32() != 0

        self.PackageGuid =  FGuid(reader).read()
        self.PackageFlags = reader.readUInt32()

        # only serialize when file version is past VER_UE4_LOAD_FOR_EDITOR_GAME
        self.bNotAlwaysLoadedForEditorGame = reader.readInt32() != 0

        # only serialize when file version is past VER_UE4_COOKED_ASSETS_IN_EDITOR_SUPPORT
        self.bIsAsset = reader.readInt32() != 0

        # only serialize when file version is past VER_UE4_PRELOAD_DEPENDENCIES_IN_COOKED_EXPORTS
        self.FirstExportDependency = reader.readInt32()
        self.SerializationBeforeSerializationDependencies = reader.readInt32()
        self.CreateBeforeSerializationDependencies = reader.readInt32()
        self.SerializationBeforeCreateDependencies = reader.readInt32() 
        self.CreateBeforeCreateDependencies = reader.readInt32()
        
        return self