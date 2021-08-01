from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Assets.Objects.FText import FText


class FNavAgentSelectorCustomization:
    SupportedDesc: FText

    def __init__(self, reader: BinaryStream):
        self.SupportedDesc = FText(reader)
