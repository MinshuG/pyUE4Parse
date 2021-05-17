import io
import json
import os
from collections import Counter
from typing import Dict, List, Optional, Union

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.IO import IoStoreReader
from UE4Parse.IO.IoObjects.FIoStoreEntry import FIoStoreEntry
from UE4Parse.IoObjects.FIoGlobalData import FIoGlobalData
from UE4Parse.Logger import get_logger
from UE4Parse.Objects.EUEVersion import EUEVersion
from UE4Parse.Objects.FPackageIndex import FPackageIndex
from UE4Parse.PackageReader import IoPackageReader, LegacyPackageReader
from UE4Parse.PakFile import PakReader
from UE4Parse.PakFile.PakObjects.FPakEntry import FPakEntry
from UE4Parse.provider.utils import *

logger = get_logger(__name__)


class FGame:
    UEVersion: EUEVersion = EUEVersion.LATEST
    GameName: Optional[str] = None
    # Version: EPakVersion = EPakVersion(11)
    # SubVersion = 0


class Package:
    _package: Union[FPakEntry, FIoStoreEntry]
    _name: str
    _uasset: BinaryStream
    _uexp: BinaryStream
    _ubulk: Optional[BinaryStream] = None
    _is_parsed: bool = False
    _parsed: Union[LegacyPackageReader, IoPackageReader]
    _provider = None

    def __init__(self, uasset: BinaryStream, uexp: BinaryStream, ubulk: BinaryStream,
                 package: Union[FPakEntry, FIoStoreEntry], provider):
        self._provider = provider
        self._package = package
        self._uasset = uasset
        self._uexp = uexp
        self._ubulk = ubulk
        self._name = self.get_mount_point() + package.Name

    def get_name(self):
        return self._name

    def parse_package(self):
        if not self._is_parsed:
            logger.info(f"Parsing {self._name}")
            if isinstance(self._package, FIoStoreEntry):
                self._parsed = IoPackageReader(self._uasset, self._ubulk, self._provider,
                                               onlyInfo=False)
            else:
                self._parsed = LegacyPackageReader(self._uasset, self._uexp, self._ubulk, self._provider)
            self._is_parsed = True
        return self._parsed

    def get_mount_point(self):
        path_ = self._package
        container = self._provider.Paks[path_.ContainerName] if path_.ContainerName in self._provider.Paks else \
            self._provider.IoStores[
                path_.ContainerName]

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
    files: Dict[str, Union[FPakEntry, FIoStoreEntry]]
    GameInfo: FGame
    files: Dict[str, Union[FPakEntry, FIoStoreEntry]]

    def __init__(self, pak_folder: Union[str, List[str]], caseinsensitive=False, GameInfo: FGame = FGame()):
        """
        pak_folder is pak folder path containing path files. \n
        :param pak_folder:
        """
        self._mounted_files = []
        self.Triggers = {}
        self.pak_folder = pak_folder
        self.caseinsensitive = caseinsensitive
        self.files = {}
        self.GameInfo = GameInfo

    @property
    def mounted_paks(self) -> list:
        """List of currently mounted paks"""
        return self._mounted_files

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

    def read_paks(self, AES_KEYs=None):
        """
        start reading paks
        AES_KEY should be a dict of PAKNAME:AES_KEY
        :param AES_KEYs:
        :return:
        """

        if AES_KEYs is None:
            AES_KEYs = {}
        self.AES_KEYs = AES_KEYs

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
            raise TypeError(f"unexpected 'pak_folder' type {type(self.pak_folder)}")

        paks: dict[str, PakReader.PakReader] = {}
        IoStores: dict[str, IoStoreReader.FFileIoStoreReader] = {}

        globalreader: Optional[IoStoreReader.FFileIoStoreReader] = None
        # just  register them
        for pak_name in pak_names:
            if not os.path.exists(pak_name):
                path = os.path.join(self.pak_folder, pak_name)
            else:
                path = pak_name
            if pak_name.endswith(".pak"):
                paks[os.path.basename(pak_name)] = PakReader.PakReader(path, self.caseinsensitive)
                logger.debug(f"Registering PakFile: {path}")
            if pak_name.endswith(".utoc"):
                ucas_path = path[:-5] + ".ucas"
                logger.debug(f"Registering IoStore: {path[:-5]}")
                reader = IoStoreReader.FFileIoStoreReader(ucas_path, BinaryStream(path),
                                                          BinaryStream(ucas_path), self.caseinsensitive)
                if pak_name.endswith("global.utoc") and globalreader is None:
                    globalreader = reader
                    continue
                IoStores[os.path.basename(ucas_path)] = reader

        pog = self.getGUID_PAKNAME_DICT(paks, IoStores)

        self.IoStores = IoStores
        self.Paks = paks

        def fixKey(aes: str):
            # isbase64 = re.findall(r'^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$', aes)
            # if (isbase64):
            #     return base64.b64decode(aes).hex()
            if aes.startswith("0x"):
                aes = aes.lstrip("0x")
            return aes

        def getaeskey(GUID, pak_name_) -> Optional[str]:
            pak_name = os.path.splitext(os.path.split(pak_name_)[1])[0]
            if GUID == '00000000000000000000000000000000':
                if '00000000000000000000000000000000' in self.AES_KEYs:
                    mainkey = fixKey(self.AES_KEYs['00000000000000000000000000000000'])
                    return mainkey
                else:
                    return None
            if pak_name in self.AES_KEYs:
                return fixKey(self.AES_KEYs[pak_name])
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
                if self.AES_KEYs is not None:
                    aeskey = getaeskey(key, pak_name)
                else:
                    aeskey = None

                try:  # IoStore
                    if pak_name.endswith(".ucas") or pak_name.endswith(".utoc"):
                        tocIndex, chunks = IoStores[pak_name].ReadDirectoryIndex(key=aeskey)
                        self.files.update(tocIndex)
                        if pak_name not in self._mounted_files:
                            self._mounted_files.append(pak_name)
                except Exception as e:
                    logger.warn(f"An error occurred while reading {pak_name}, {e}")

                try:  # pak
                    if pak_name.endswith(".pak"):
                        self.files.update(paks[pak_name].ReadIndex(key=aeskey))
                        if pak_name not in self._mounted_files:
                            self._mounted_files.append(pak_name)
                except Exception as e:
                    logger.warn(f"An error occurred while reading {pak_name}, {e}")

        if globalreader is not None:
            logger.info("Reading GlobalData...")
            self.GlobalData = FIoGlobalData(globalreader, list(IoStores.values()))

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

    def get_package(self, name: Union[str, FPackageIndex]) -> Optional[Package]:
        """Load Package into memory"""
        if isinstance(name, FPackageIndex):
            name = name.Resource.ObjectName.__str__()

        name = os.path.splitext(name)[0]  # remove extension
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

            uexp = None
            ubulk = None
            if isinstance(package, FIoStoreEntry):  # IoStorePackage
                uasset = package.GetData()
                if package.hasUbulk:
                    ubulk = BinaryStream(package.ubulk.GetData())
            else:  # PakPackage
                container = self.Paks[package.ContainerName]
                reader = container.reader

                uasset = package.get_data(reader, key=None, compression_method=container.Info.CompressionMethods)
                if package.hasUexp:
                    uexp = package.uexp.get_data(reader, key=None, compression_method=container.Info.CompressionMethods)
                if package.hasUbulk:
                    ubulk = package.ubulk.get_data(reader, key=None,
                                                   compression_method=container.Info.CompressionMethods)

            return Package(uasset, uexp, ubulk, package, self)

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
