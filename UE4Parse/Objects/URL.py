from typing import List

from UE4Parse.BinaryReader import BinaryStream


class FURL:
    Protocol: str  # Protocol, i.e. "unreal" or "http".
    Host: str  # Optional hostname, i.e. "204.157.115.40" or "unreal.epicgames.com", blank if local.
    Port: int  # Optional host port.
    Valid: int
    Map: str  # Map name, i.e. "SkyCity", default is "Entry".
    RedirectURL: str  # Optional place to download Map if client does not possess it
    Op: List[str]  # Options.
    Portal: str  # Portal to enter through, default is "".

    def __init__(self, reader: BinaryStream):
        self.Protocol = reader.readFString()
        self.Host = reader.readFString()
        self.Map = reader.readFString()
        self.Portal = reader.readFString()
        self.Op = reader.readTArray(reader.readFString)
        self.Port = reader.readInt32()
        self.Valid = reader.readInt32()

