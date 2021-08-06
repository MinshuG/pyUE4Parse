import itertools
from typing import List, Tuple

from ..Exceptions.Exceptions import ParserException
from .FUnversionedHeader import FFragment, FUnversionedHeader, bitarray

def invertbool(booll: bool):
    return False if booll else True


class CIterator:
    Current = None

    def __init__(self, iterator) -> None:
        self.iterator = iterator

    def __iter__(self):
        return self

    def __next__(self):
        self.Current = next(self.iterator)
        return self.Current
        # raise StopIteration

class FIterator:
    _schemaIt: int
    _remainingFragmentValues: int
    _zeroMask: bitarray
    _zeroMaskIndex: int
    _fragmentIt: int  # CIterator

    def __init__(self, header: FUnversionedHeader) -> None:
        self._zeroMask = header.ZeroMask
        self._fragments = header.Fragments  # CIterator(itertools.cycle(header.Fragments))

        self.bDone = False
        self._fragmentIt = 0

        self._zeroMaskIndex = 0
        self._schemaIt = 0
        self._remainingFragmentValues = 0

        if not self.bDone:
            # next(self._fragmentIt)
            self.Skip()

    def Shouldread(self):
        return self.IsNonZero and not self.bDone

    @property
    def Current(self):
        return self._fragments[self._fragmentIt]

    @property
    def IsNonZero(self): 
        return invertbool(self.Current.HasAnyZeroes) or invertbool(self._zeroMask.checkifexists(self._zeroMaskIndex))

    def MoveNext(self):
        self._schemaIt += 1
        self._remainingFragmentValues -= 1

        if self.Current.HasAnyZeroes:
            self._zeroMaskIndex += 1

        if self._remainingFragmentValues == 0:
            if self.Current.IsLast:
                self.bDone = True
            else:
                self._fragmentIt += 1  # next(self._fragmentIt)
                self.Skip()
        return True

    def Skip(self):
        self._schemaIt += self.Current.SkipNum

        while self.Current.ValueNum == 0:
            assert invertbool(self.Current.IsLast)
            # next(self._fragmentIt)
            self._fragmentIt += 1
            self._schemaIt += self.Current.SkipNum

        self._remainingFragmentValues = self.Current.ValueNum
