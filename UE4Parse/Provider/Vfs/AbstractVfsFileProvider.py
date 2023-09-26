from UE4Parse.Assets.Exports.UObjects import UObject
from UE4Parse.Assets.PackageReader import Package
from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Localization.FTextLocalizationResource import FTextLocalizationResource
from UE4Parse.Provider.Vfs.DirectoryStorageProvider import DirectoryStorageProvider
from UE4Parse.Versions.Versions import VersionContainer
from UE4Parse.Exceptions.Exceptions import InvalidEncryptionKey
from abc import ABC, abstractmethod
from typing import Callable, Optional, Tuple, Union, Dict, List
from UE4Parse.IO import FFileIoStoreReader

from UE4Parse.Assets.Objects.FGuid import FGuid
from UE4Parse.Encryption import FAESKey
from UE4Parse.IoObjects.FIoGlobalData import FIoGlobalData
from UE4Parse.Logger import get_logger
from UE4Parse.PakFile.PakReader import PakReader

logger = get_logger(__name__)


class AbstractVfsFileProvider(ABC):
    IsCaseInsensitive: bool
    GlobalData: Optional[FIoGlobalData]
    UnloadedContainers: List[Union[FFileIoStoreReader, PakReader]]
    LoadedContainers: List[Union[FFileIoStoreReader, PakReader]]
    LocalizedResources: Dict[str, Dict[str, str]]
    _files: DirectoryStorageProvider
    GameName: str
    _file_streams: Dict[str, BinaryStream]

    def __init__(self, versions: VersionContainer, isCaseInsensitive: bool = False) -> None:
        self.GlobalData = None
        self.Versions = versions
        self.IsCaseInsensitive = isCaseInsensitive
        self.UnloadedContainers = []
        self.LoadedContainers = []
        self.LocalizedResources = {}
        self._files = DirectoryStorageProvider(self.IsCaseInsensitive)
        self.GameName = ""
        self._file_streams = {}
        self.virtual_paths = {}

    @property
    def files(self):
        return self._files

    @abstractmethod
    def open_stream(self, path: str) -> BinaryStream:
        pass

    def close(self):
        for container in self.LoadedContainers:
            container.close()
        for container in self.UnloadedContainers:
            container.close()

    def unload_container(self, container: Union[FFileIoStoreReader, PakReader]):
        if container in self.LoadedContainers:
            self.LoadedContainers.remove(container)
            for d in self.files.Storage:
                if container.FileName == d.get_container().FileName:
                    self.files.Storage.remove(d)
                    break
            self.UnloadedContainers.append(container)

    def register_container(self, name, streams: Tuple[BinaryStream, Callable[[str], BinaryStream]]):
        """
        Initializes container reader and adds it to `UnloadedContainers`
        """
        assert len(streams) > 0
        if name.endswith(".pak"):
            try:
                logger.debug(f"Registering PakFile: {name}")
                reader = PakReader(name, self.IsCaseInsensitive, streams[0])
                self.UnloadedContainers.append(reader)
            except Exception as e:
                logger.error(f"Error reading {name}: {e}")
        elif name.endswith(".utoc"):
            logger.debug(f"Registering IoStore: {name[:-5]}")
            try:
                reader = FFileIoStoreReader(name, streams[0],
                                            streams[1], self.Versions.UEVersion, self.IsCaseInsensitive)
                if name.endswith("global.utoc"):
                    self.GlobalData = FIoGlobalData(reader, self.Versions.UEVersion)
                self.UnloadedContainers.append(reader)
            except Exception as e:
                logger.error(f"Error reading {name}: {e}")
        else:
            pass

    def unloaded_files_by_guid(self, guid: Union[str, FGuid]) -> List[Union[FFileIoStoreReader, PakReader]]:
        files = []
        for x in self.UnloadedContainers:
            enc_guid = x.get_encryption_key_guid()
            if enc_guid == guid:
                files.append(x)
        return files

    def submit_key(self, guid: Union[str, FGuid]=FGuid(0,0,0,0), key: Optional[FAESKey]=None) -> int:
        """
        Tries to mount a file with the given guid
        returns: `int` the number of files successfully mounted

        Arguments: \n
        guid -- the guid of the file to mount \n
        key -- the key to use for the encryption
        """
        return self.submit_keys({guid: key})

    def submit_keys(self, keys: Dict[Union[str, FGuid], Optional[FAESKey]]) -> int:
        """
        Tries to mount a file with the given guid
        returns: `int` the number of files successfully mounted

        Arguments: \n
        `dict` of guid and key \n
        guid -- the guid of the file to mount \n
        key -- the key to use for the encryption
        """
        mounted_count = self._mount(keys)
        if self.GameName == "" and mounted_count > 0:
            self.set_game_name()
        return mounted_count

    def _mount(self, keys: Dict[Union[str, FGuid], Optional[FAESKey]]):
        mount_count = 0
        for guid, key in keys.items():
            for x in self.unloaded_files_by_guid(guid):
                if isinstance(x, FFileIoStoreReader):
                    if x.IsEncrypted and x.get_encryption_key_guid() not in keys:
                        continue
                    if not x.HasDirectoryIndex:
                        continue
                    try:
                        index, chunks = x.ReadDirectoryIndex(keys[x.get_encryption_key_guid()])
                        del chunks
                        self._files.add_index(index, x)
                        self.LoadedContainers.append(x)
                        self.UnloadedContainers.remove(x)
                        mount_count += 1
                    except Exception as e:
                        if isinstance(e, InvalidEncryptionKey):
                            continue
                        logger.error(f"Error reading index for {x.FileName}, {e}")
                elif isinstance(x, PakReader):
                    if x.Info.bEncryptedIndex and x.get_encryption_key_guid() not in keys:
                        continue
                    try:
                        index = x.ReadIndex(keys[x.get_encryption_key_guid()])
                        self._files.add_index(index, x)

                        self.LoadedContainers.append(x)
                        self.UnloadedContainers.remove(x)
                        mount_count += 1
                    except Exception as e:
                        if isinstance(e, InvalidEncryptionKey):
                            continue
                        logger.error(f"Error reading index for {x.FileName}, {e}")
                else:
                    continue
        return mount_count

    def set_game_name(self):
        for k, _ in self._files:
            root = k.split("/")[0]
            if root != "Engine":
                self.GameName = root

    def load_virtual_paths(self) -> int:
        import re
        import json
        pattern = re.compile(f"^{self.GameName}/Plugins/.+.upluginmanifest$", re.IGNORECASE)

        count = 0
        for _, v in self.files:
            if re.match(pattern, v.Name):
                try:
                    manifest = json.load(self.get_reader(v))
                except Exception as _:
                    continue
                if "Contents" in manifest:
                    for content in manifest["Contents"]:
                        if "File" in content:
                            s = content["File"].replace("../../../", "").split("/")
                            virtual_path = "/".join(s[:-1])
                            plugin_name = s[-1].split(".")[0]
                            if content.get("Descriptor", {}).get("CanContainContent", False):
                                if self.IsCaseInsensitive:
                                    self.virtual_paths[plugin_name.lower()] = virtual_path.lower()
                                else:
                                    self.virtual_paths[plugin_name] = virtual_path
                                count += 1
        logger.info(f"Loaded {count} virtual paths")
        return count

    def load_localization(self, language_code = "en") -> int:
        #  https://github.com/FabianFG/CUE4Parse/blob/22ad6c42a27071cd91fdad71f2a02e8597031de9/CUE4Parse/FileProvider/AbstractFileProvider.cs#L63
        import re
        pattern = re.compile( f"^{self.GameName}/.+/{language_code}/.+.locres$", re.IGNORECASE)
        self.LocalizedResources = {}
        count = 0
        for _, v in self.files:
            if re.match(pattern, v.Name):
                logger.debug(f"Loading {v.Name}")
                res = FTextLocalizationResource(self.get_reader(v))
                for key, value in res.Entries.items():
                    if key not in self.LocalizedResources:
                        self.LocalizedResources[key] = {}
                    self.LocalizedResources[key].update(value)
                    count += len(value)
        logger.info(f"Loaded {count} localized resources for {language_code}.")

        return count

    def get_localized_string(self, namespace, key, default=""):
        return self.LocalizedResources.get(namespace, {}).get(key, default)

    def fix_path(self, path: str) -> str:
        path = path.lower() if self.IsCaseInsensitive else path
        root = path[:path.index("/", path.index("/")+1)]

        if root.lower() == self.GameName.lower():
            return path
        if root.startswith("/"): root = root[1:]

        if root.lower() == "game":
            if self.IsCaseInsensitive:
                path = path.replace("/game", f"{self.GameName.lower()}/content", 1)
            else:
                path = path.replace("/Game", f"{self.GameName}/Content", 1)

        if plugin_path := self.virtual_paths.get(root):
            if self.IsCaseInsensitive:
                path = plugin_path + "/content" + path[path.index(root)+len(root):]
            else:
                path = plugin_path + "/Content" + path[path.index(root)+len(root):]
            return path

        return path

    @abstractmethod
    def get_reader(self, path: str):
        pass

    @abstractmethod
    def export_type_event(self, *args, **kwargs):
        pass

    @abstractmethod
    def try_load_package(self, *args, **kwargs) -> Optional[Package]:
        pass

    @abstractmethod
    def try_load_object(self, *args, **kwargs) -> Optional[UObject]:
        pass
