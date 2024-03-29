from typing import Any, Tuple
from ..BinaryReader import BinaryStream


class bitarray:
    """list of bools"""

    def __init__(self, size) -> None:
        if isinstance(size, list):
            self.__bools = size
        elif isinstance(size, str):
            self.__bools = []
            for x in size:
                self.__bools.append(bool(int(x)))
        else:
            self.__bools = [False] * size

    def addTrueAt(self, index: int):
        if len(self.__bools) - 1 <= index:
            extra = [False] * (index - len(self.__bools) + 1)
            self.__bools = extra + self.__bools
            self.__bools[index] = True
        else:
            self.__bools[index] = True

    def trim(self, where: int, to: int):
        return bitarray(self.__bools[where:to])

    def contains(self, what: bool):
        for x in self.__bools:
            if x == what:
                return True
        return False
        # return any(i == what for i in self.__bools)

    def __str__(self) -> str:
        return str(self.__bools)

    def __repr__(self) -> str:
        return str(self)

    def __len__(self):
        return len(self.__bools)

    def checkifexists(self, index):
        try:
            self.__bools[index]
            return True
        except IndexError:
            return False

    def get(self, index, default=None):
        try:
            return self.__bools[index]
        except IndexError:
            return default

class FFragment:
    _SkipMax = 127
    _ValueMax = 127
    _SkipNumMask = 0x007f
    _HasZeroMask = 0x0080
    _ValueNumShift = 9
    _IsLastMask = 0x0100

    SkipNum: int
    HasAnyZeroes: bool
    ValueNum: int
    IsLast: bool

    def __init__(self, value: int) -> None:
        self.SkipNum = (value & self._SkipNumMask)
        self.HasAnyZeroes = (value & self._HasZeroMask) != 0
        self.ValueNum = (value >> self._ValueNumShift)
        self.IsLast = (value & self._IsLastMask) != 0


class FUnversionedHeader:
    Fragments: Tuple[FFragment]
    ZeroMask: bitarray
    HasNonZeroValues: bool

    def hasValues(self):
        return self.HasNonZeroValues | len(self.ZeroMask) > 0

    def __init__(self, reader: BinaryStream) -> None:
        fragments = []

        zeroMaskNum = 0
        unmaskedNum = 0
        while True:
            fragment = FFragment(reader.readUInt16())
            fragments.append(fragment)

            if fragment.HasAnyZeroes:
                zeroMaskNum += fragment.ValueNum
            else:
                unmaskedNum += fragment.ValueNum

            if fragment.IsLast:
                break

        if zeroMaskNum > 0:
            self.ZeroMask = self.LoadZeroMaskData(reader, zeroMaskNum)
            self.HasNonZeroValues = unmaskedNum > 0 or self.ZeroMask.contains(True)  # this work no idea how
        else:
            self.ZeroMask = bitarray(0)
            self.HasNonZeroValues = unmaskedNum > 0

        self.Fragments = tuple(fragments)

    def LoadZeroMaskData(self, reader: BinaryStream, numBits: int) -> bitarray:
        if numBits <= 8:
            bits = '{:08b}'.format(ord(reader.readByte()))[::-1]
            data = bitarray(bits)            
        elif numBits <= 16:
            rawdata = reader.read(2) # *sizeof(uint16)
            bits = "".join("{:08b}".format(x)[::-1] for x in rawdata)
            data = bitarray(bits)
        else:
            num = divide_round_up(numBits, 32)
            rawdata = reader.read(num*4) # *sizeof(int32)
            bits = "".join("{:08b}".format(x)[::-1] for x in rawdata)

            data = bitarray(bits)
        trimed = data.trim(0, numBits)
        return trimed


def divide_round_up(dividend, divisor):
    return int((dividend + divisor - 1) / divisor)
