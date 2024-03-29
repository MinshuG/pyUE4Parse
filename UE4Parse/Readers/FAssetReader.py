from UE4Parse.Exceptions.Exceptions import ParserException
from UE4Parse.Assets.Objects.EPackageFlags import EPackageFlags
from typing import TYPE_CHECKING, BinaryIO, List, Union
from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Versions import EUEVersion

if TYPE_CHECKING:
    from UE4Parse.Assets.Objects.FNameEntrySerialized import FNameEntrySerialized
    from UE4Parse.Assets.PackageReader import Package
    from UE4Parse.Assets.Objects.FGuid import FGuid
    from UE4Parse.Provider.DefaultFileProvider import DefaultFileProvider


class FAssetReader(BinaryStream):
    provider: 'DefaultFileProvider'
    NameMap: List['FNameEntrySerialized']
    PackageReader: 'Package'
    absolute_offset: int

    def __init__(self, fp: Union[BinaryIO, str, bytes], owner: 'Package', size: int = -1, absolute_offset: int = 0):
        super().__init__(fp, size)
        self.PackageReader = owner
        self.absolute_offset = absolute_offset

    @property
    def absolute_position(self) -> int:
        return self.position + self.absolute_offset

    @property
    def NameMap(self):
        return self.PackageReader.NameMap

    @property
    def provider(self):
        return self.PackageReader.Provider

    def get_name_map(self):
        return self.NameMap

    @property
    def has_unversioned_properties(self):
        return bool(self.PackageReader.get_summary().PackageFlags & EPackageFlags.PKG_UnversionedProperties)

    @property
    def is_filter_editor_only(self):
        return bool(self.PackageReader.get_summary().PackageFlags & EPackageFlags.PKG_FilterEditorOnly)

    def seek_absolute(self, offset: int, whence: int = 0):
        return self.seek(offset - self.absolute_offset, whence)

    def set_ar_version(self, ueversion: EUEVersion):
        self.game = ueversion
        self.version = self.game.get_ar_ver()

    def CustomVer(self, key: 'FGuid') -> int:
        Summary = self.PackageReader.get_summary()
        if not hasattr(Summary, "GetCustomVersions"):
            return -1
        CustomVersion = Summary.GetCustomVersions().get_version(key)
        return CustomVersion if CustomVersion is not None else -1

    def getmappings(self):
        if getattr(self, "mappings", None):
            return self.mappings
        raise ParserException("mappings are not attached")
