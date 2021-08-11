import warnings

from UE4Parse.Encryption import FAESKey
from UE4Parse.Provider.MappingProvider import MappingProvider
from UE4Parse.IoObjects.FImportedPackage import FPackageId
from UE4Parse.Localization.FTextLocalizationResource import FTextLocalizationResource
import io
import json
import os
from collections import Counter
from typing import Dict, List, Optional, Union, Mapping

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.IO import IoStoreReader
from UE4Parse.IO.IoObjects.FIoStoreEntry import FIoStoreEntry
from UE4Parse.IoObjects.FIoGlobalData import FIoGlobalData
from UE4Parse.Logger import get_logger
from UE4Parse.Assets.PackageReader import IoPackageReader, LegacyPackageReader
from UE4Parse.PakFile import PakReader
from UE4Parse.PakFile.PakObjects.FPakEntry import FPakEntry
from UE4Parse.Provider.utils import *
from UE4Parse.Versions.Versions import VersionContainer

logger = get_logger(__name__)

FGame = VersionContainer


class PackageProvider:
    _package: Union[FPakEntry, FIoStoreEntry]
    _name: str
    _uasset: BinaryStream
    _uexp: BinaryStream
    _ubulk: Optional[BinaryStream] = None
    _uptnl: Optional[BinaryStream] = None
    _is_parsed: bool = False
    _parsed: Union[LegacyPackageReader, IoPackageReader]
    _provider: 'Provider' = None

    def __init__(self, uasset: BinaryStream, uexp: BinaryStream, ubulk: BinaryStream, uptnl: BinaryStream,
                 package: Union[FPakEntry, FIoStoreEntry], provider):
        self._provider = provider
        self._package = package
        self._uasset = uasset
        self._uexp = uexp
        self._ubulk = ubulk
        self._uptnl = uptnl
        self._name = self.get_mount_point() + package.Name

    def get_name(self):
        return self._name

    def parse_package(self, *args, **kwargs):
        """
        kwargs:
                `onlyInfo`: `bool` Used by `IoPackageReader'
        """

        if not self._is_parsed:
            logger.info(f"Parsing {self._name}")

            ext = os.path.splitext(os.path.basename(self._name))[1]
            if ext in [".uasset", ".umap", ".uptnl"]:
                if isinstance(self._package, FIoStoreEntry):
                    self._uasset.mappings = self._provider.mappingProvider
                    onlyInfo = kwargs.get("onlyInfo") or False
                    self._parsed = IoPackageReader(self._uasset, self._ubulk, self._uptnl, self._provider,
                                                   onlyInfo=onlyInfo)
                else:
                    self._parsed = LegacyPackageReader(self._uasset, self._uexp, self._ubulk, self._provider)
            elif ext in [".locres"]:
                self._parsed = FTextLocalizationResource(self._uasset)
            elif ext == ".locmeta":
                self._parsed = None
                print("TODO locmeta")
            elif ext in [".ufont", ".uproject", ".upluginmanifest", ".ini", ".pem"]:
                self._uasset.seek(0)
                self._parsed = self._uasset.read()
            else:
                print(f"Unknown Type: [{ext}] {self._name}")
                raise Exception("Unknown Type")
                self._parsed = None
            self._is_parsed = True
        return self._parsed

    def get_mount_point(self):
        path_ = self._package
        container = self._provider.Paks[path_.ContainerName] if path_.ContainerName in self._provider.Paks else \
            self._provider.IoStores[
                path_.ContainerName]  # .utoc

        mount_point = container.MountPoint if isinstance(container,
                                                         PakReader.PakReader) else container.ContainerFile.MountPoint
        if mount_point.startswith("/"):
            mount_point = mount_point[1:]

        return mount_point

    def save_package(self, path):
        def write(data, path_):
            mount_point = self.get_mount_point()

            mounted_path = os.path.join(mount_point, path_.Name[1:] if path_.Name.startswith("/") else path_.Name)
            x = os.path.join(path, mounted_path)
            dir_ = os.path.dirname(x)
            if not os.path.exists(dir_):
                os.makedirs(dir_)

            with open(x, "wb") as f:
                f.write(data.base_stream.read())
                data.seek(0, 0)

        package = self._package

        logger.info("Writing asset...")
        write(self._uasset, package)

        if package.hasUexp:
            write(self._uexp, package.uexp)
        if package.hasUbulk:
            write(self._ubulk, package.ubulk)
        return True

    def save_json(self, path, indent=4):
        def write(data, path_):
            mount_point = self.get_mount_point()

            mounted_path = os.path.join(mount_point, path_.Name)
            if mounted_path.startswith("/"):
                mounted_path = mounted_path[1:]

            x = os.path.splitext(os.path.join(path, mounted_path))[0] + ".json"
            dir_ = os.path.dirname(x)
            if not os.path.exists(dir_):
                os.makedirs(dir_)

            with open(x, "w") as f:
                json.dump(data, f, indent=indent)

        jsondata = self.parse_package().get_dict()
        write(jsondata, self._package)
        return True


class Provider:
    mainGuid = "00000000000000000000000000000000"

    pak_folder: str
    _mounted_files: list = []
    AES_KEYs: dict
    Paks: dict
    IoStores: dict
    caseinsensitive: bool
    GlobalData: FIoGlobalData
    GameInfo: FGame
    files: Dict[str, Union[FPakEntry, FIoStoreEntry]]
    mappingProvider: MappingProvider = None

    def __init__(self, pak_folder: Union[str, List[str]], caseinsensitive=False, GameInfo: FGame = FGame.default(),
                 mappings: MappingProvider = None):
        """
        pak_folder is pak folder path containing path files. \n
        :param pak_folder:
        """
        warnings.warn("Use DefaultFileProvider instead", category=DeprecationWarning, stacklevel=2)

        self._mounted_files = []
        self.Triggers = {}
        self.pak_folder = pak_folder
        self.caseinsensitive = caseinsensitive
        self.files = {}
        self.GameInfo = GameInfo
        self._AES_Keys = {}
        self.Paks: dict[str, PakReader.PakReader] = {}
        self.IoStores: dict[str, IoStoreReader.FFileIoStoreReader] = {}
        self.GlobalData = None
        self.mappingProvider = mappings
        self._intialize()

    def _intialize(self) -> None:
        if self.pak_folder is None:
            return
        if isinstance(self.pak_folder, list):
            pak_names = self.pak_folder
            self.pak_folder = os.path.dirname(pak_names[0])
        elif os.path.isdir(self.pak_folder):
            pak_names = os.listdir(self.pak_folder)
        elif isinstance(self.pak_folder, str):
            if os.path.isfile(self.pak_folder):
                pak_names = [self.pak_folder]
                self.pak_folder = os.path.dirname(pak_names[0])
        else:
            raise TypeError(f"unexpected 'pak_folder' type {type(self.pak_folder)}")  # path doesn't exit

        globalreader: Optional[IoStoreReader.FFileIoStoreReader] = None
        # just  register them
        for pak_name in pak_names:
            if not os.path.exists(pak_name):
                path = os.path.join(self.pak_folder, pak_name)
            else:
                path = pak_name
            reader, pak_name = self._register_file(pak_name, path)

            if reader is None:
                continue
            if pak_name.endswith("global.utoc") and globalreader is None:
                globalreader = reader
                continue

            if isinstance(reader, PakReader.PakReader):
                self.Paks[pak_name] = reader
            else:
                self.IoStores[pak_name] = reader

        if globalreader is not None:
            logger.info("Reading GlobalData...")
            self.GlobalData = FIoGlobalData(globalreader, list(self.IoStores.values()))

    @property
    def mounted_paks(self) -> list:
        """List of currently mounted paks"""
        return self._mounted_files

    def _register_file(self, con_file, path):
        pak_name = con_file

        if pak_name.endswith(".pak"):
            reader = PakReader.PakReader(path, self.caseinsensitive)
            logger.debug(f"Registering PakFile: {path}")
            return reader, os.path.basename(pak_name)
        if pak_name.endswith(".utoc"):
            ucas_path = path[:-5] + ".ucas"
            logger.debug(f"Registering IoStore: {path[:-5]}")
            reader = IoStoreReader.FFileIoStoreReader(ucas_path, BinaryStream(path),
                                                      BinaryStream(ucas_path), self.caseinsensitive)
            return reader, os.path.basename(pak_name)

        return None, None

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

    def read_paks(self, aes_keys: Optional[Mapping[str, FAESKey]] = None):
        """
        start reading paks
        AES_KEY should be a dict of PAKNAME:AES_KEY
        :param aes_keys:
        :return:
        """

        if aes_keys is None:
            aes_keys = {}
        self.AES_KEYs = aes_keys

        pog = self.getGUID_PAKNAME_DICT(self.Paks, self.IoStores)

        def getaeskey(guid, pak_name_) -> Optional[str]:
            pak_name = os.path.splitext(os.path.split(pak_name_)[1])[0]

            if guid in self.AES_KEYs:
                return self.AES_KEYs[guid]
            if pak_name in self.AES_KEYs:
                return self.AES_KEYs[pak_name]
            return None

        def most_frequent(List_):
            if self.GameInfo.GameName is None:  # don't override if set manually
                occurence_count = Counter(List_)
                commons = occurence_count.most_common(2)
                for x in commons:
                    if x[0] != "Engine":
                        return x[0]
            return self.GameInfo.GameName

        self.files = {}
        # read index
        for key, pak_names in pog.items():
            for pak_name in pak_names:
                try:  # IoStore
                    if pak_name.endswith(".ucas") or pak_name.endswith(".utoc"):
                        container = self.IoStores[pak_name]
                        aeskey = getaeskey(container.get_encryption_key_guid(), pak_name)
                        tocIndex, chunks = container.ReadDirectoryIndex(key=aeskey)
                        self.files.update(tocIndex)
                        if pak_name not in self._mounted_files:
                            self._mounted_files.append(pak_name)
                        self._AES_Keys[container.get_encryption_key_guid()] = aeskey
                except Exception as e:
                    logger.warn(f"An error occurred while reading {pak_name}, {e}")
                    # raise e

                try:  # pak
                    if pak_name.endswith(".pak"):
                        container = self.Paks[pak_name]
                        aeskey = getaeskey(container.get_encryption_key_guid(), pak_name)
                        self.files.update(container.ReadIndex(key=aeskey))
                        if pak_name not in self._mounted_files:
                            self._mounted_files.append(pak_name)
                        self._AES_Keys[container.get_encryption_key_guid()] = aeskey
                except Exception as e:
                    logger.warn(f"An error occurred while reading {pak_name}, {e}")

        if len(self.files) > 0:
            files = [file.split("/")[0] for file in self.files.keys()]
            self.GameInfo.GameName = most_frequent(files)

    @staticmethod
    def get_game_name():
        return FGame.GameName

    @staticmethod
    def getGUID_PAKNAME_DICT(paks, Ios):
        Dict = {}
        for pak_name in paks:
            pak = paks[pak_name]
            EncryptionID = pak.Info.EncryptionKeyGuid.GetValue()
            if EncryptionID not in Dict:
                Dict[EncryptionID] = []
            Dict[EncryptionID].append(pak_name)
        for utoc_name in Ios:
            IoStore = Ios[utoc_name]
            EncryptionID = IoStore.TocResource.Header.EncryptionKeyGuid.GetValue()
            if EncryptionID not in Dict:
                Dict[EncryptionID] = []
            Dict[EncryptionID].append(utoc_name)
        return Dict

    def findObject(self, object_name: str):  # not really
        for key, _ in self.files.items():
            if key.split("/")[-1].lower() == object_name.lower():
                return key
        return None

    def find_package_by_Id(self, Id: FPackageId) -> Optional[str]:
        # chunkId = Id.Id
        for name, package in self.files.items():
            if isinstance(package, FIoStoreEntry):
                if Id.Id == package.ChunkId.ChunkId:
                    return name
        return None

    def get_package(self, name: Union[str, FPackageId]) -> Optional[PackageProvider]:
        """Load Package into memory"""
        if isinstance(name, FPackageId):
            foundname = self.find_package_by_Id(name)
            if foundname is None:
                logger.error(f"Requested Package {name.Id!r} not found.")
                return None
            name = foundname

        name = os.path.splitext(name)[0]
        if name is not None:
            name = fixpath(name, self.GameInfo.GameName)
        name = name.lower() if self.caseinsensitive else name

        isObjectName = len(name.split("/")) == 1
        if isObjectName:
            object_name = self.findObject(name)
            if object_name is None:
                logger.error(f"Requested Package \"{name}\" not found.")
                return None
            name = object_name

        if name not in self.files:
            logger.error(f"Requested Package \"{name}\" not found.")
            return None
        else:
            logger.info(f"Loading {name}")
            package: Union[FPakEntry, FIoStoreEntry] = self.files[name]

            uexp = getattr(package, "uexp", None)
            ubulk = getattr(package, "ubulk", None)
            uptnl = getattr(package, "uptnl", None)
            if isinstance(package, FIoStoreEntry):  # IoStorePackage
                uasset = package.GetData()
                if ubulk:
                    ubulk = ubulk.GetData()
                if uptnl:
                    uptnl = uptnl.GetData()
            else:  # PakPackage
                container = self.Paks[package.ContainerName]
                reader = container.reader

                key = self._AES_Keys.get(container.get_encryption_key_guid(), None)

                uasset = package.get_data(reader, key=key, compression_method=container.Info.CompressionMethods)
                if uexp:
                    uexp = uexp.get_data(reader, key=key, compression_method=container.Info.CompressionMethods)
                if package.hasUbulk:
                    ubulk = ubulk.get_data(reader, key=key,
                                           compression_method=container.Info.CompressionMethods)

            return PackageProvider(uasset, uexp, ubulk, uptnl, package, self)

    def readpackage(self, uasset, uexp, ubulk=None) -> LegacyPackageReader:
        """
         Direct read packages from disk or buffer \n
         Provided args should be str, bytes or bytearray
        :param GameInfo:
        :param uasset:
        :param uexp:
        :param ubulk:
        :return LegacyPackageReader:
        """

        def yeet(anything):
            if isinstance(anything, str):
                if not os.path.exists(anything):
                    logger.error(f"{anything} not found")
                with open(anything, "rb") as f:
                    data = f.read()
                    return BinaryStream(io.BytesIO(data), size=len(data))

            elif isinstance(anything, (bytes, bytearray)):
                return BinaryStream(io.BytesIO(anything), size=len(anything))

        uasset = yeet(uasset)
        uexp = yeet(uexp)
        if ubulk is not None:
            ubulk = yeet(ubulk)

        return LegacyPackageReader(uasset, uexp, ubulk, self)
