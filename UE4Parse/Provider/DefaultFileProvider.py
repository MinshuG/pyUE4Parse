from functools import singledispatchmethod
from typing import Union, Optional, List

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Versions import VersionContainer
from . import MappingProvider
from .Common import GameFile
from .Vfs import AbstractVfsFileProvider

import os
from glob import glob

from .utils import fixpath
from ..Assets.PackageReader import IoPackageReader, LegacyPackageReader, Package, EPackageLoadMode
from ..IO.IoObjects import FIoStoreEntry
from ..IoObjects.FImportedPackage import FPackageId
from ..Logger import get_logger

logger = get_logger(__name__)


class DefaultFileProvider(AbstractVfsFileProvider):
    __path: str
    mappings: MappingProvider

    @singledispatchmethod
    def __init__(self, path: List[str], versions: VersionContainer = VersionContainer.default(),
                 isCaseInsensitive: bool = False) -> None:
        self.__path = path
        super().__init__(versions, isCaseInsensitive=isCaseInsensitive)
        self.GameInfo = versions  # old provider
        self.Triggers = {}
        self.mappings = None

    @__init__.register
    def _(self, path: str, versions: VersionContainer = VersionContainer.default(),
                 isCaseInsensitive: bool = False) -> None:
        assert os.path.exists(path), "provided path must exists"
        self.__path = path
        super().__init__(versions, isCaseInsensitive=isCaseInsensitive)
        self.GameInfo = versions  # old provider
        self.Triggers = {}
        self.mappings = None

    def initialize(self, *args, **kwargs):
        if isinstance(self.__path, list):
            files = self.__path
        else:
            files = glob(self.__path + "/*")

        for f in files:
            if os.path.isfile(f):
                name = os.path.basename(f)
                if f.endswith(".utoc"):
                    utoc_stream = BinaryStream(f)
                    ucas_stream = BinaryStream(f.replace(".utoc", ".ucas"))
                    self.register_container(name, (utoc_stream, ucas_stream))
                elif f.endswith(".pak"):
                    self.register_container(name, (BinaryStream(f),))
                else:
                    continue
            else:
                logger.warn(f"{f} is not a file")

    def get_reader(self, path: str):  # TODO Game file overload
        name = os.path.splitext(path)[0]
        name = fixpath(name, self.GameName)
        name = name.lower() if self.IsCaseInsensitive else name
        package = self.files.get(name)
        if package is None:
            logger.error(f"Requested Package \"{path}\" not found.")
            return None
        return package.get_data()

    @singledispatchmethod
    def try_load_package(self, name: Union[str, FPackageId], load_mode: EPackageLoadMode = EPackageLoadMode.Full) -> Optional[Package]:
        """Load a Package"""
        package: GameFile
        if isinstance(name, FPackageId):
            package = self.files.get(name)
        else:
            name = os.path.splitext(name)[0]
            name = fixpath(name, self.GameName)
            name = name.lower() if self.IsCaseInsensitive else name
            package = self.files.get(name)

        if package is not None:
            return self.try_load_package(package, load_mode)
        else:
            logger.error(f"Requested Package \"{name}\" not found.")
            return None

    @try_load_package.register
    def _(self, package: GameFile, load_mode: EPackageLoadMode = EPackageLoadMode.Full):
        if not package.Name.endswith((".umap", ".uasset")):
            return None

        real_path = package.Container.get_mount_point() + package.Name

        logger.info(f"Loading {real_path}")

        uexp = getattr(package, "uexp", None)
        ubulk = getattr(package, "ubulk", None)
        uptnl = getattr(package, "uptnl", None)
        if isinstance(package, FIoStoreEntry):  # IoStorePackage
            uasset = package.get_data()
            uasset.mappings = self.mappings
            if ubulk:
                ubulk = ubulk.get_data()
            if uptnl:
                uptnl = uptnl.get_data()
            return IoPackageReader(uasset, ubulk, uptnl, self, load_mode)
        else:  # PakPackage
            uasset = package.get_data()
            uasset.mappings = self.mappings
            if uexp:
                uexp = uexp.get_data()
            if ubulk:
                ubulk = ubulk.get_data()
            return LegacyPackageReader(uasset, uexp, ubulk, self, load_mode)

    def export_type_event(self, *args, **kwargs):
        if len(args) > 0:
            func = args[0]
            if func:
                self.Triggers[func.__name__] = func
                return func
        name = kwargs.get("name")

        if name is None:
            name = func.__name__

        def wrapper(func):
            self.Triggers[name] = func

        return wrapper
