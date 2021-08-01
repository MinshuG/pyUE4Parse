from UE4Parse.BinaryReader import BinaryStream


class FRotator:
    SIZE = 4+4+4
    position: int
    Pitch = 0.0
    Yaw = 0.0
    Roll = 0.0

    def __init__(self, reader: BinaryStream):
        self.position = reader.base_stream.tell()
        self.Pitch = reader.readFloat()
        self.Yaw = reader.readFloat()
        self.Roll = reader.readFloat()

    def GetValue(self):
        return {
            "Pitch": self.Pitch,
            "Yaw": self.Yaw,
            "Roll": self.Roll
        }
