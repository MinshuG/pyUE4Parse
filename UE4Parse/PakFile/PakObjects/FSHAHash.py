from UE4Parse.BinaryReader import BinaryStream


class FSHAHash:
    Hash: bytes = None

    def __init__(self, reader: BinaryStream) -> None:
        self.Hash = reader.readBytes(20)
