from typing import List, TypeVar, Type, TYPE_CHECKING

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.PakFile.PakObjects.FSHAHash import FSHAHash
from UE4Parse.Readers.FAssetReader import FAssetReader
from UE4Parse.Versions import EUEVersion

if TYPE_CHECKING:
    from UE4Parse.IoObjects.FImportedPackage import FPackageId

T = TypeVar("T")

class FFilePackageStoreEntry:
    ExportCount: int
    ExportBundleCount: int
    ImportedPackages: List['FPackageId']
    ShaderMapHashes: List[FSHAHash]

    def __init__(self, reader: BinaryStream, version):
        if version >= EUEVersion.GAME_UE5_0:
            self.ExportCount, self.ExportBundleCount = reader.unpack2("2i", 8)
            from UE4Parse.IoObjects.FImportedPackage import FPackageId
            self.ImportedPackages = self.ReadCArrayView(reader, FPackageId)
            self.ShaderMapHashes = self.ReadCArrayView(reader, FSHAHash)
        else:
            raise NotImplementedError()

    @staticmethod
    def ReadCArrayView(reader: BinaryStream, func: T) -> List[Type[T]]:
        start_pos = reader.tell()

        size = reader.readInt32()
        offset = reader.readInt32() # offset to data from this
        if size == 0: return  []

        reader.seek(start_pos + offset, 0)
        res = reader.readTArray2(func, size, reader)
        reader.seek(start_pos + 8, 0) # move where we left
        return list(res)
