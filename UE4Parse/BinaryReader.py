import os
from io import BufferedReader, BytesIO
from struct import *
from typing import Union

from UE4Parse import Logger
from UE4Parse.Exceptions.Exceptions import ParserException
from UE4Parse.Objects.EUEVersion import EUEVersion
from UE4Parse.Objects.FName import FName, DummyFName
from UE4Parse.Objects.FPackageIndex import FPackageIndex

logging = Logger.get_logger(__name__)


class BinaryStream:
    NameMap: list
    PackageReader: object
    version: int
    game: EUEVersion = None
    fake_size: int
    ubulk_stream: object
    bulk_offset: int = -1
    size = 0

    def __init__(self, fp: Union[BufferedReader, BytesIO, str, bytes], size: int = -1):
        if isinstance(fp, str):
            self.base_stream = open(fp, "rb")
            self.size = os.path.getsize(fp)
        elif isinstance(fp, bytes) or isinstance(fp, bytearray):
            self.base_stream = BytesIO(fp)
            self.size = len(fp)
        else:
            self.base_stream = fp
            self.size = size

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

    def seek(self, offset, SEEK_SET=1):
        self.base_stream.seek(offset, SEEK_SET)

    @property
    def position(self):
        return self.base_stream.tell()

    def close(self):
        return self.base_stream.close()

    def tell(self):
        return self.base_stream.tell()

    def tellfake(self):
        return (self.fake_size - self.size) + self.base_stream.tell()

    def read(self):
        """read till end"""
        return self.base_stream.read()

    def readByte(self):
        return self.base_stream.read(1)

    def readByteToInt(self, length=1):
        return int.from_bytes(self.readBytes(length), "little")

    def readBytes(self, length):
        if self.size == self.position:
            raise ParserException("Cannot read beyond end of stream")
        return self.base_stream.read(length)

    def readChar(self):
        return self.unpack('b')

    def readUChar(self):
        return self.unpack('B')

    def readBool(self):
        """Booleans in UE are serialized as int32"""
        return self.readInt32() != 0
        # return self.unpack('?')

    def readSByte(self):
        return self.unpack("b", 1)

    def readInt8(self):
        return self.readByteToInt(1)

    def readUInt8(self):
        return self.readByteToInt(1)  # ?

    def readInt16(self):
        return self.unpack('h', 2)

    def readUInt16(self):
        return self.unpack('H', 2)

    def readInt32(self) -> int:
        return self.unpack('i', 4)

    def readUInt32(self):
        return self.unpack('I', 4)

    def readInt64(self):
        return self.unpack('q', 8)

    def readUInt64(self):
        return self.unpack('Q', 8)

    def readFloat(self):
        return self.unpack('f', 4)

    def readDouble(self):
        return self.unpack('d', 8)

    def readString(self):
        length = self.readByteToInt()
        return self.unpack(str(length) + 's', length).decode("utf-8")

    def readFString(self):
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
            byte = self.readBytes(length)[:-1]
            return byte.decode("utf-8")

    def readTArray(self, func, *args):
        SerializeNum = self.readInt32()
        A = []
        for _ in range(SerializeNum):
            A.append(func(*args))
        return A

    def readTArray_W_Arg(self, func, *args):  # argument
        """use readTArray"""
        SerializeNum = self.readInt32()
        A = []
        for _ in range(SerializeNum):
            A.append(func(*args))
        return A

    # https://github.com/FabianFG/JFortniteParse/blob/aa1c3a224c948939ec91270dea655dc677e05a1e/src/main/kotlin/me/fungames/jfortniteparse/ue4/reader/FArchive.kt#L174
    def readBulkTArray(self, func, *args) -> list:
        elementSize = self.readInt32()
        savePos = self.tell()
        array = self.readTArray_W_Arg(func, *args)
        if self.tell() != savePos + 4 + len(array) * elementSize:
            raise ParserException(
                f"RawArray item size mismatch: expected {elementSize}, serialized {(self.tell() - savePos) / len(array)}")
        return array

    def readFName(self):
        NameMap = self.NameMap
        NameIndex = self.readInt32()
        Number = self.readInt32()

        if not 0 <= NameIndex < len(NameMap):
            logging.debug(f"Bad Name Index: {NameIndex}/{len(NameMap)} - Loader Position: {self.base_stream.tell()}")
            return DummyFName()

        return FName(NameMap[NameIndex], NameIndex, Number)

    def readObject(self):
        index = FPackageIndex(self)
        if index.IsNull:
            return None
        object = self.PackageReader.findObject(index)
        if index is None or object is None:
            logging.warn(f"{index.Index} is not found.")
        return object

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
        return unpack(fmt, self.readBytes(length))[0]


def Align(val: int, alignment: int):
    return val + alignment - 1 & ~(alignment - 1)


def convert_each_byte_to_int(bytes_):
    ints = ""
    for x in bytes_:
        ints += str(x)
    return int(ints)
