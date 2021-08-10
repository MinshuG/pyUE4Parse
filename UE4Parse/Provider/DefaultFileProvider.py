from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Versions import VersionContainer
from .Vfs import AbstractVfsFileProvider

import os
from glob import glob


class DefaultFileProvider(AbstractVfsFileProvider):
    __path: str

    def __init__(self, path: str, versions: VersionContainer = VersionContainer.default(),
                 isCaseInsensitive: bool = False) -> None:
        assert os.path.exists(path)
        self.__path = path
        super().__init__(versions, isCaseInsensitive=isCaseInsensitive)

    def initialize(self):
        for f in glob(self.__path + "/*"):
            if os.path.isfile(f):
                name = os.path.basename(f)
                if f.endswith(".utoc"):
                    utoc_stream = BinaryStream(f)
                    ucas_stream = BinaryStream(f.replace(".utoc", ".ucas"))
                    self.register_container(name, (utoc_stream, ucas_stream))
                elif f.endswith(".pak"):
                    self.register_container(name, [BinaryStream(f)])
                else:
                    continue
