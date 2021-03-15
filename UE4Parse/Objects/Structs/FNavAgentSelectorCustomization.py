from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Objects.FText import FText


class FNavAgentSelectorCustomization:
    SupportedDesc: FText

    def __init__(self, reader: BinaryStream):
        self.SupportedDesc = FText(reader)
