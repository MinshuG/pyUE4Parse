from typing import Optional

from UE4Parse import Logger
from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Objects.FGuid import FGuid
from UE4Parse.Objects.FPropertyTag import FPropertyTag
from UE4Parse.PropertyTagData import BaseProperty
from UE4Parse.PropertyTagData.BaseProperty import ReadType

logger = Logger.get_logger(__name__)


class UObject:
    position: int
    Dict: dict = {}

    def __init__(self, reader: BinaryStream, validpos, structFallback: bool = False) -> None:
        self.Tags = []
        self.reader: BinaryStream = reader
        self.structFallback = structFallback
        self.position = self.reader.base_stream.tell()
        self.Dict = self.read(validpos)

    # @property
    def read(self, validpos):
        properties = {}
        num = 1
        tags = []
        while True:
            Tag = FPropertyTag(self.reader)
            if Tag.Name.isNone or Tag.Name.GetValue() == "None":
                break
            tags.append(Tag)
            self.reader.seek(Tag.Size, 1)

        for Tag in tags:
            self.reader.seek(Tag.end_pos, 0)
            pos = self.reader.base_stream.tell()
            try:
                obj = BaseProperty.ReadAsObject(
                    self.reader, Tag, Tag.Type, ReadType.NORMAL)
            except Exception as e:
                # raise e
                logger.debug(f"Failed to read values for {Tag.Name.string}, {e}")
                obj = None

            key = Tag.Name.string
            if key in properties:
                key = f"{key}_NK{num:00}"
                num += 1
            else:
                pass
            properties[key] = obj
            pos2 = self.reader.base_stream.tell()
            expectedPos: int = Tag.Size + pos
            if expectedPos != pos2:
                behind = expectedPos - pos2
                logger.debug(
                    f"Didn't read {key} correctly (at {pos2}, should be {Tag.Size + pos}, {behind} behind)")
                self.reader.seek(Tag.Size + pos, 0)
        if len(properties.keys()) > 0:
            self.Dict = properties

        pos = self.reader.tell()
        if pos + 4 <= validpos:
            wtf = self.reader.readBool()
            if pos + 20 <= validpos and wtf:  # 4+16
                FGuid(self.reader)

        return self.Dict

    def GetValue(self) -> dict:
        """Json"""
        dict_ = {}
        for key, value in self.Dict.items():
            if value is not None:
                if isinstance(value, list):
                    value = [x.GetValue() for x in value]
                else:
                    value = value.GetValue()
            dict_[key] = value
        return dict_

    def try_get(self, key: str) -> Optional[object]:
        for key_, value in self.Dict.items():
            if key_ == key:
                return value
        return None
