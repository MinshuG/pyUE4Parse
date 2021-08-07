from UE4Parse.Assets.Objects.EObjectFlags import EObjectFlags
from UE4Parse.Exceptions.Exceptions import ParserException
from UE4Parse.IoObjects.FIterator import FIterator
from UE4Parse.IoObjects.FUnversionedHeader import FUnversionedHeader
from typing import Optional

from UE4Parse import Logger
from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Assets.Objects.FGuid import FGuid
from UE4Parse.Assets.Objects.FPropertyTag import FPropertyTag
from UE4Parse.Assets.PropertyTagData import BaseProperty
from UE4Parse.Assets.PropertyTagData.BaseProperty import ReadType, ZERORead

logger = Logger.get_logger(__name__)


class UObject:
    position: int
    Dict: dict
    type: str
    flag: int

    def __init__(self, reader: BinaryStream, structFallback: bool = False) -> None:
        # self.Tags = []
        self.Dict: dict = {}
        self.reader: BinaryStream = reader
        self.structFallback = structFallback
        self.position = self.reader.base_stream.tell()
        self.ObjectGuid = None

    def deserialize(self, validpos):
        if self.reader.has_unversioned_properties:
            self.deserializeUnVersioned()
        else:
            self.deserializeVersioned()

        pos = self.reader.tell()
        if pos + 4 <= validpos:
            val = self.reader.readInt32()
            if val not in [0, 1]:
                self.reader.seek(-4)
                return
            boolval = val != 0
            if not self.flag & EObjectFlags.RF_ClassDefaultObject and boolval:
                self.ObjectGuid = FGuid(self.reader)

    def deserializeVersioned(self):
        properties = {}
        num = 1
        while True:
            Tag = FPropertyTag(self.reader)
            if Tag.Name.isNone:
                break
            pos = self.reader.base_stream.tell()
            try:
                obj = BaseProperty.ReadAsObject(
                    self.reader, Tag, Tag.Type, ReadType.NORMAL)
            except Exception as e:
                # raise e
                logger.debug(f"Failed to read values for {Tag.Name}, {e}")
                obj = None

            key = Tag.Name.string
            if key in properties:
                key = f"{key}_NK{num:00}"
                num += 1
            else:
                pass
            self.addProp(Tag, obj, num)
            properties[key] = obj
            pos2 = self.reader.base_stream.tell()
            expectedPos: int = Tag.Size + pos
            if expectedPos != pos2:
                behind = expectedPos - pos2
                logger.debug(
                    f"Didn't read {Tag!r} correctly (at {pos2}, should be {Tag.Size + pos}, {behind} behind)")
                self.reader.seek(Tag.Size + pos, 0)

        return properties

    def deserializeUnVersioned(self, type=None):
        reader = self.reader
        properties = {}
        pos = reader.tell()
        Header = FUnversionedHeader(reader)
        if not Header.hasValues():
            return properties

        Schema = self.reader.getmappings().get_schema(type or self.type)
        if Schema is None:
            raise ParserException(f"Missing prop mappings for type {type or self.type}")
        tags = []
        num = 1
        if Header.HasNonZeroValues:
            iterator = FIterator(Header)
            while not iterator.bDone:
                current = iterator.Current
                propmappings = Schema.TryGetProp(iterator._schemaIt)
                if propmappings is None:
                    raise ParserException("Missing Mappings for index {} (type={}) cannot proceed with serilization".format(iterator._schemaIt, self.type))
                Tag = FPropertyTag(None, propmappings)
                tags.append(Tag)

                if iterator.IsNonZero:
                    try:
                        pos = reader.tell()
                        obj = BaseProperty.ReadAsObject(
                        self.reader, Tag, Tag.Type, ReadType.NORMAL)
                        logger.debug(f"{pos} -> {reader.tell()} : {Tag.Name}")
                    except Exception as e:
                        raise ParserException(f"Failed to read values for {Tag.Name.string}") from e

                    self.addProp(Tag, obj, num)
                    if obj is None:
                        break
                else:  # Zero prop
                    try:
                        pos = reader.tell()
                        obj = BaseProperty.ReadAsObject(
                        self.reader, Tag, Tag.Type, ReadType.ZERO)
                        logger.debug(f"{pos} -> {reader.tell()} : {Tag.Name}")
                    except Exception as e:
                        logger.debug(f"Failed to read values for {Tag.Name.string}, but's it's zero")
                        obj = None
                    self.addProp(Tag, obj, num)

                iterator.MoveNext()

    def addProp(self, Tag, value, num):
        key = Tag.Name.string
        if key in self.Dict:
            key = f"{key}_NK{num:00}"
            num += 1
        self.Dict[key] = value

    def GetValue(self) -> dict:
        """:returns JSON Serializable dict"""
        if len(self.Dict) == 0:
            return {}
        properties = {}
        for key, value in self.Dict.items():
            if value is not None:
                if isinstance(value, list):
                    value = [x.GetValue() for x in value]
                else:
                    value = value.GetValue()
            properties[key] = value
        if self.structFallback:
            return properties
        return {"Properties": properties}

    def try_get(self, key: str) -> Optional[object]:
        if found := self.Dict.get(key, None):
            return found.Value
        return None
