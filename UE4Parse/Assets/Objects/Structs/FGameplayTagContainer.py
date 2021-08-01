from typing import List

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Assets.Objects.FName import FName


class FGameplayTagContainer:
    position: int
    GameplayTags: List[FName]

    def __init__(self, reader: BinaryStream) -> None:
        self.position = reader.base_stream.tell()
        self.GameplayTags = reader.readTArray(reader.readFName)

    def GetValue(self) -> list:
        List_ = []
        for GameplayTag in self.GameplayTags:
            List_.append(GameplayTag.string)
        return List_
