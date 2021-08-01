from UE4Parse.Assets import PropertyTagData
from UE4Parse.BinaryReader import BinaryStream


class ByteProperty:
    position: int
    Value: str

    def __init__(self, reader: BinaryStream, readType, tag):
        self.position = reader.base_stream.tell()

        if readType == PropertyTagData.BaseProperty.ReadType.NORMAL:
            self.Value = reader.readByteToInt()
        elif readType == PropertyTagData.BaseProperty.ReadType.MAP:
            self.Value = reader.readUInt32()
        elif readType == PropertyTagData.BaseProperty.ReadType.ARRAY:
            self.Value = reader.readByteToInt()
        else:
            raise Exception(f"hmm {readType.name}")

    def GetValue(self):
        return self.Value
