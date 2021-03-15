#from UE4Parse.BinaryReader import BinaryStream # circular


class FNameEntrySerialized:
    Name: str

    def __init__(self, reader):
        self.Name = reader.readFString()
        reader.seek(4)
