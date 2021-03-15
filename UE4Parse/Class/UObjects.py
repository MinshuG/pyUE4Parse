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

    def __init__(self, reader: BinaryStream, structFallback: bool = False) -> None:
        self.reader: BinaryStream = reader
        self.structFallback = structFallback
        self.Dict = self.read()

    # @property
    def read(self):
        properties = {}
        num = 1
        self.position = self.reader.base_stream.tell()
        while True:
            Tag = FPropertyTag(self.reader)
            if Tag.Name.isNone or Tag.Name.string == "None":
                break

            pos = self.reader.base_stream.tell()
            try:
                obj = BaseProperty.ReadAsObject(
                    self.reader, Tag, Tag.Type, ReadType.NORMAL)
            except Exception as e:
                logger.debug(f"Failed to read values for {Tag.Name.string}, {e}")
                obj = None

            key = Tag.Name.string
            if key in properties:
                key = f"{key}_NK{num:00}"
                num = + 1
            else:
                pass

            properties[key] = obj

            if obj is None:
                break
            pos2 = self.reader.base_stream.tell()
            if Tag.Size + pos != pos2:
                behind = Tag.Size + pos - pos2
                logger.debug(
                    f"Didn't read {key} correctly (at {pos2}, should be {Tag.Size + pos}, {behind} behind)")
                self.reader.seek(Tag.Size + pos, 0)
        if len(properties.keys()) > 0:
            self.Dict = properties

        if not self.structFallback:
            wtf = self.reader.readInt32() != 0
            if wtf:
                FGuid(self.reader)
        return self.Dict

    def GetValue(self, position_value_type: bool = False) -> dict:
        """Json"""
        dict_ = {}
        for key, value in self.Dict.items():
            if value is not None:
                if isinstance(value, bytes):
                    breakpoint()  # getting byte somewhere
                if position_value_type:
                    value = {
                        "position": value.position,
                        "Value": value.GetValue()
                    }
                else:
                    value = value.GetValue()
            dict_[key] = value
        return dict_

    def try_get(self, key: str) -> Optional[object]:
        for key_, value in self.Dict.items():
            if key_ == key:
                return value
        return None
