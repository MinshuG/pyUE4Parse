from UE4Parse.BinaryReader import BinaryStream

class FSHAHash:
    __slots__ = ('Hash',)
    Hash: bytes

    def __init__(self, reader: BinaryStream) -> None:
        self.Hash = reader.readBytes(20)
