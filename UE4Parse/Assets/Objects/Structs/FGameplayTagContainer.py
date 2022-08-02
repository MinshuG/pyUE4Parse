from typing import Tuple
from UE4Parse.Assets.Objects.Common import StructInterface

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Assets.Objects.FName import FName


class FGameplayTagContainer(StructInterface):
    position: int
    GameplayTags: Tuple[FName]

    def __init__(self, reader: BinaryStream) -> None:
        self.position = reader.base_stream.tell()
        self.GameplayTags = reader.readTArray(reader.readFName)

    @classmethod
    def default(cls):
        inst = cls.__new__(cls)
        inst.position = -1
        inst.GameplayTags = tuple()
        return inst

    def GetValue(self) -> list:
        List_ = []
        for GameplayTag in self.GameplayTags:
            List_.append(GameplayTag.string)
        return List_
