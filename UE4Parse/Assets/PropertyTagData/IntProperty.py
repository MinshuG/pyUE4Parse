from UE4Parse.BinaryReader import BinaryStream


class Int8Property:
    position: int
    Value: int

    def __init__(self, reader: BinaryStream):
        self.position = reader.base_stream.tell()
        self.Value = int.from_bytes(reader.readByte(), "little")

    def GetValue(self):
        return self.Value


class Int16Property:
    position: int
    Value: int

    def __init__(self, reader: BinaryStream):
        self.position = reader.base_stream.tell()
        self.Value = reader.readInt16()

    def GetValue(self):
        return self.Value


class IntProperty:
    position: int
    Value: int

    def __init__(self, reader: BinaryStream):
        self.position = reader.base_stream.tell()
        self.Value = reader.readInt32()

    def GetValue(self):
        return self.Value


class Int64Property:
    position: int
    Value: int

    def __init__(self, reader: BinaryStream):
        self.position = reader.base_stream.tell()
        self.Value = reader.readInt64()

    def GetValue(self):
        return self.Value


class UInt16Property:
    position: int
    Value: int

    def __init__(self, reader: BinaryStream):
        self.position = reader.base_stream.tell()
        self.Value = reader.readUInt16()

    def GetValue(self):
        return self.Value


class UInt32Property:
    position: int
    Value: int

    def __init__(self, reader: BinaryStream):
        self.position = reader.base_stream.tell()
        self.Value = reader.readUInt32()

    def GetValue(self):
        return self.Value


class UInt64Property:
    position: int
    Value: int

    def __init__(self, reader: BinaryStream):
        self.position = reader.base_stream.tell()
        self.Value = reader.readUInt64()

    def GetValue(self):
        return self.Value
