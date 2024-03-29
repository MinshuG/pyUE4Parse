from enum import Enum, auto
from UE4Parse.Assets.Objects.Common import StructInterface

from UE4Parse.BinaryReader import BinaryStream


class ERichCurveInterpMode(Enum):
    Linear = 0
    Constant = auto()
    Cubic = auto()
    none = auto()  # none is None


class ERichCurveTangentMode(Enum):
    Auto = 0
    User = auto()
    Break = auto()
    none = auto()


class ERichCurveTangentWeightMode(Enum):
    none = 0
    Arrive = auto()
    Leave = auto()
    Both = auto()


class FSimpleCurveKey(StructInterface):
    position: int
    KeyTime: float
    KeyValue: float

    def __init__(self, reader: BinaryStream):
        self.position = reader.base_stream.tell()
        self.KeyTime = reader.readFloat()
        self.KeyValue = reader.readFloat()

    @classmethod
    def default(cls):
        inst = cls.__new__(cls)
        inst.position = 0
        inst.KeyTime, inst.KeyValue = (0.0, 0.0,)

    def GetValue(self):
        return {
            "KeyTime": self.KeyTime,
            "KeyValue": self.KeyValue
        }


class FRichCurveKey(StructInterface):
    position: int
    InterpMode: ERichCurveInterpMode
    TangentMode: ERichCurveTangentMode
    TangentWeightMode: ERichCurveTangentWeightMode
    KeyTime: float
    KeyValue: float
    ArriveTangent: float
    ArriveTangentWeight: float
    LeaveTangent: float
    LeaveTangentWeight: float

    def __init__(self, reader: BinaryStream):  # probably crash
        self.position = reader.base_stream.tell()
        self.InterpMode = ERichCurveInterpMode(int.from_bytes(reader.readByte(), byteorder="little"))
        self.TangentMode = ERichCurveTangentMode(int.from_bytes(reader.readByte(), byteorder="little"))
        self.TangentWeightMode = ERichCurveTangentWeightMode(int.from_bytes(reader.readByte(), byteorder="little"))
        self.KeyTime = reader.readFloat()
        self.KeyValue = reader.readFloat()
        self.ArriveTangent = reader.readFloat()
        self.ArriveTangentWeight = reader.readFloat()
        self.LeaveTangent = reader.readFloat()
        self.LeaveTangentWeight = reader.readFloat()

    @classmethod
    def default(cls):
        inst = cls.__new__(cls)
        inst.position = -1
        inst.InterpMode, inst.TangentMode, inst.TangentWeightMode = (ERichCurveInterpMode.Linear, ERichCurveTangentMode.Auto, ERichCurveTangentWeightMode.none,)
        inst.KeyTime, inst.KeyValue = (0.0, 0.0,)
        inst.ArriveTangent, inst.ArriveTangentWeight = (0.0, 0.0,)
        inst.LeaveTangent, inst.LeaveTangentWeight = (0.0, 0.0,)
        return inst

    def GetValue(self):
        return {
            "InterpMode": self.InterpMode.name,
            "TangentMode": self.TangentMode.name,
            "TangentWeightMode": self.TangentWeightMode.name,
            "KeyTime": self.KeyTime,
            "KeyValue": self.KeyValue,
            "ArriveTangent": self.ArriveTangent,
            "ArriveTangentWeight": self.ArriveTangentWeight,
            "LeaveTangent": self.LeaveTangent,
            "LeaveTangentWeight": self.LeaveTangentWeight
        }
