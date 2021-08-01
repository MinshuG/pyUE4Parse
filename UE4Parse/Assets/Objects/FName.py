from typing import Union

from UE4Parse.Assets.Objects.FNameEntrySerialized import FNameEntrySerialized


class FName:
    Index: int
    Number: int
    _String: str
    string: str
    isNone: bool

    def __init__(self, name: Union[FNameEntrySerialized, str], index: int = 0, number: int = 0) -> None:
        self._String = name.Name if isinstance(name, FNameEntrySerialized) else name
        self.Index = index
        self.Number = number
        self.isNone = self.string is None or self.string == "None"

    @property
    def string(self):
        return self._String if self.Number == 0 else f"{self._String}_{self.Number - 1}"

    def GetValue(self):
        return self.string

    def __str__(self):
        return self.string


class DummyFName:
    Index: int
    Number: int
    string: str
    isNone: bool

    def __init__(self) -> None:
        self.string = None
        self.Index = 0
        self.Number = 69
        self.isNone = True

    def GetValue(self):
        return self.string
