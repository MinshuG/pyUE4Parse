from UE4Parse.Assets.Objects.EPackageFlags import EPackageFlags
import os
from io import BufferedReader, BytesIO
from struct import *
from typing import BinaryIO, Tuple, TypeVar, Union, TYPE_CHECKING, AnyStr, Optional, Iterable

from UE4Parse import Logger
from UE4Parse.Exceptions.Exceptions import ParserException
from UE4Parse.Versions.EUEVersion import EUEVersion
from UE4Parse.Assets.Objects.FName import FName
from UE4Parse.Assets.Objects.FPackageIndex import FPackageIndex

if TYPE_CHECKING:
    from UE4Parse.Assets.Exports.UObjects import UObject
    from UE4Parse.Assets.Objects.FGuid import FGuid
    from UE4Parse.Assets.PackageReader import Package
    from UE4Parse.Provider.MappingProvider import MappingProvider

logging = Logger.get_logger(__name__)

T = TypeVar("T")


class BinaryStream(BinaryIO):
    NameMap: list
    PackageReader: Union['Package']
    version: int
    game: EUEVersion = None
    fake_size: int
    ubulk_stream: 'BinaryStream'
    bulk_offset: int = -1
    size = 0
    mappings: 'MappingProvider'

    def __init__(self, fp: Union[BinaryIO, str, bytes], size: int = -1):
        if isinstance(fp, str):
            self.base_stream = open(fp, "rb")
            self.size = os.path.getsize(fp)
        elif isinstance(fp, (bytes, bytearray)):
            self.base_stream = BytesIO(fp)
            self.size = len(fp)
        else:
            self.base_stream = fp
            self.size = size

        self.close = self.base_stream.close
        self.tell = self.base_stream.tell
        self.readBytes = self.base_stream.read

    def change_stream(self, fp: Union[BufferedReader, str, bytes, bytearray]):
        if isinstance(fp, str):
            self.base_stream = open(fp, "rb")
            self.size = os.path.getsize(fp)
        elif isinstance(fp, bytes) or isinstance(fp, bytearray):
            self.base_stream = BytesIO(fp)
            self.size = len(fp)
        else:  # self
            self.base_stream = fp.base_stream
            self.fake_size = self.size + fp.size
            self.size = fp.size

    def set_ar_version(self, ueversion):
        self.game = ueversion
        self.version = self.game.get_ar_ver()

    def CustomVer(self, key: 'FGuid') -> int:
        Summary = self.PackageReader.get_summary()
        if not hasattr(Summary, "GetCustomVersions"):
            return -1
        CustomVersion = Summary.GetCustomVersions().get_version(key)
        return CustomVersion if CustomVersion is not None else -1

    @property
    def has_unversioned_properties(self):
        return bool(self.PackageReader.get_summary().PackageFlags & EPackageFlags.PKG_UnversionedProperties)

    def seek(self, offset, SEEK_SET=1):
        self.base_stream.seek(offset, SEEK_SET)

    def seekable(self) -> bool:
        return self.base_stream.seekable()

    def getmappings(self):
        if getattr(self, "mappings", None):
            return self.mappings
        raise ParserException("mappings are not attached")

    def get_name_map(self):
        return self.PackageReader.NameMap

    @property
    def position(self):
        return self.base_stream.tell()

    def tellfake(self) -> int:
        return (self.fake_size - self.size) + self.base_stream.tell()

    def __enter__(self):
        raise NotImplementedError()

    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError()

    def read(self, length=-1) -> bytes:
        if length > 0:
            return self.readBytes(length)
        return self.base_stream.read()

    def readByte(self) -> bytes:
        return self.base_stream.read(1)

    def readByteToInt(self, length=1) -> int:
        return int.from_bytes(self.base_stream.read(length), "little")

    # def readBytes(self, length): # more performance issues
    #     # if self.size == self.position:  # performance issues
    #     #     raise ParserException("Cannot read beyond end of stream")
    #     return self.base_stream.read(length)

    def readChar(self) -> int:
        return self.unpack('b')

    def readUChar(self):
        return self.unpack('B')

    def readBool(self):
        """Booleans in UE are serialized as int32"""
        val = self.readInt32()
        if val not in [0, 1]:
            raise ParserException("Invalid boolean value")
        return val != 0
        # return self.unpack('?')

    def readSByte(self) -> int:
        return self.unpack("b", 1)

    def readInt8(self) -> int:
        return self.readByteToInt(1)

    def readUInt8(self) -> int:
        return self.readByteToInt(1)  # ?

    def readInt16(self) -> int:
        return self.unpack('h', 2)

    def readUInt16(self) -> int:
        return self.unpack('H', 2)

    def readInt32(self) -> int:
        return self.unpack('i', 4)

    def readUInt32(self) -> int:
        return self.unpack('I', 4)

    def readInt64(self) -> int:
        return self.unpack('q', 8)

    def readUInt64(self) -> int:
        return self.unpack('Q', 8)

    def readFloat(self) -> float:
        return self.unpack('f', 4)

    def readDouble(self) -> float:
        return self.unpack('d', 8)

    def readString(self) -> str:
        length = self.readByteToInt()
        return self.unpack(str(length) + 's', length).decode("utf-8")

    def readFString(self) -> str:
        length = self.readInt32()
        LoadUCS2Char: bool = length < 0

        if LoadUCS2Char:
            if length == -2147483648:
                raise Exception("Archive is corrupted.")

            length = -length

        if length == 0:
            return ""

        if LoadUCS2Char:
            data = []
            for i in range(length):
                if i == length - 1:
                    self.readUInt16()
                else:
                    data.append(self.readUInt16())
            string = ''.join([chr(v) for v in data])
            return string
        else:
            byte = self.base_stream.read(length)[:-1]
            return byte.decode("utf-8")

    def readTArray(self, func: T, *args) -> Tuple[T]:
        SerializeNum = self.readInt32()
        A = tuple(func(*args) for _ in range(SerializeNum))
        return A

    def readTArray_W_Arg(self, func: T, *args) -> Tuple[T]:  # argument
        """use readTArray"""
        return self.readTArray(func, *args)

    def readBulkTArray(self, func, *args) -> tuple:
        elementSize = self.readInt32()
        savePos = self.tell()
        array = self.readTArray(func, *args)
        if self.tell() != savePos + 4 + len(array) * elementSize:
            raise ParserException(
                f"RawArray item size mismatch: expected {elementSize}, serialized {(self.tell() - savePos) / len(array)}")
        return array

    def readFName(self) -> FName:
        NameMap = self.get_name_map()
        NameIndex = self.readInt32()
        Number = self.readInt32()

        if not 0 <= NameIndex < len(NameMap):
            logging.debug(f"Bad Name Index: {NameIndex}/{len(NameMap)} - Reader Position: {self.base_stream.tell()}")
            return FName("None")

        return FName(NameMap[NameIndex], NameIndex, Number)

    def readObject(self) -> 'UObject':
        index = FPackageIndex(self)
        if index.IsNull:
            return None
        object = self.PackageReader.findObject(index)
        if index is None or object is None:
            logging.warn(f"{index.Index} is not found.")
        return object

    def writable(self):
        return self.base_stream.writable()

    def truncate(self, size: Optional[int] = ...) -> int:
        return self.base_stream.truncate(size)

    def writelines(self, lines: Iterable[AnyStr]) -> None:
        return self.base_stream.writelines(lines)

    def write(self, s: AnyStr) -> int:
        return self.base_stream.write(s)

    def writeBytes(self, value):
        self.size += len(value)
        self.base_stream.write(value)

    def writeChar(self, value):
        self.pack('c', value)

    def writeUChar(self, value):
        self.pack('C', value)

    def writeBool(self, value):
        self.pack('?', value)

    def writeInt16(self, value):
        self.pack('h', value)

    def writeUInt16(self, value):
        self.pack('H', value)

    def writeInt32(self, value):
        self.pack('i', value)

    def writeUInt32(self, value):
        self.pack('I', value)

    def writeInt64(self, value):
        self.pack('q', value)

    def writeUInt64(self, value):
        self.pack('Q', value)

    def writeFloat(self, value):
        self.pack('f', value)

    def writeDouble(self, value):
        self.pack('d', value)

    def writeString(self, value):
        length = len(value)
        self.writeUInt16(length)
        self.pack(str(length) + 's', value)

    def pack(self, fmt, data):
        return self.writeBytes(pack(fmt, data))

    def unpack(self, fmt, length=1):
        return unpack(fmt, self.base_stream.read(length))[0]


def Align(val: int, alignment: int):
    return val + alignment - 1 & ~(alignment - 1)
