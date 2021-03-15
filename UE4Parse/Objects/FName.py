from UE4Parse.Objects.FNameEntrySerialized import FNameEntrySerialized


class FName:
    Index: int
    Number: int
    string: str
    isNone: bool

    def __init__(self, name: FNameEntrySerialized, index: int = 0, number: int = 0) -> None:
        self.string = name.Name
        self.Index = index
        self.Number = number
        self.isNone = self.string is None or self.string == "None"

    # @property
    # def isNone(self):
    #     return self.string is None or self.string == "None"

    def GetValue(self):
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