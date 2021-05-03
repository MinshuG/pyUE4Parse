from typing import Union

from UE4Parse.BinaryReader import BinaryStream


class FNameEntryId:
    Value: int

    def __init__(self, reader: Union[BinaryStream, int]):
        if isinstance(reader, BinaryStream):
            self.Value = reader.readUInt32()
        else:
            self.Value = reader
