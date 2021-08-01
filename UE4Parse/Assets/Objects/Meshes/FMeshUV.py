from typing import Optional, Union

from UE4Parse.BinaryReader import BinaryStream


class FMeshUV:
    U: Union[int, float]
    V: Union[int, float]

    def __init__(self):
        pass

    def GetValue(self):
        return {
            "U": self.U,
            "V": self.V
        }


class FMeshUVFloat(FMeshUV):
    U: float
    V: float

    def __init__(self, reader: Optional[BinaryStream] = None):
        super().__init__()
        if reader is None:
            return
        self.U = reader.readFloat()
        self.V = reader.readFloat()

    def construct(self, U, V):
        self.U = U
        self.V = V
        return self


class FMeshUVHalf(FMeshUV):
    U: int
    V: int

    def __init__(self, reader: BinaryStream):
        super().__init__()
        self.U = reader.readUInt16()
        self.V = reader.readUInt16()

    def to_mesh_uv_float(self):
        return FMeshUVFloat().construct(self.U, self.V)
