from typing import Dict

from UE4Parse.BinaryReader import BinaryStream


class FStringTable:
    TableNamespace: str
    KeysToMetadata: Dict[str, Dict[str, str]]

    def __init__(self, reader: BinaryStream):
        self.TableNamespace = reader.readFString()

        self.KeysToMetadata = {}

        NumEntries = reader.readInt32()
        for i in range(NumEntries):
            key = reader.readFString()
            text = reader.readFString()
            self.KeysToMetadata[key] = text

    def GetValue(self):
        return {
            "Namespace": self.TableNamespace,
            "Table": self.KeysToMetadata
        }
