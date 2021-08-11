from typing import Tuple

from UE4Parse import DefaultFileProvider
from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Versions import VersionContainer


class StreamedFileProvider(DefaultFileProvider):

    def __init__(self, versions: VersionContainer = VersionContainer.default(),
                 isCaseInsensitive: bool = False):
        super().__init__(".", versions, isCaseInsensitive)

    def initialize(self, filename: str ,streams: Tuple[BinaryStream]):
        self.register_container(filename, streams)
