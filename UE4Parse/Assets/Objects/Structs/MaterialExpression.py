from UE4Parse.Assets.Objects.Common import StructInterface
from UE4Parse.Assets.Objects.FName import FName
from UE4Parse.Readers.FAssetReader import FAssetReader
from UE4Parse.Versions.FFrameworkObjectVersion import FFrameworkObjectVersion

class Float(StructInterface):
    def __init__(self, reader: FAssetReader):
        self.value = reader.readFloat()

    @classmethod
    def default(cls) -> 'Float':
        inst = cls.__new__(cls)
        inst.value = 0.0
        return inst

    def GetValue(self) -> float:
        return self.value

class FExpressionInput(StructInterface):
    OutputIndex: int
    InputName: FName
    Mask: int
    MaskR: int
    MaskG: int
    MaskB: int
    MaskA: int
    ExpressionName: FName


    def __init__(self, reader: FAssetReader) -> None:
        self.OutputIndex = reader.readInt32()
        self.InputName = reader.readFName() if FFrameworkObjectVersion().get(reader) >= FFrameworkObjectVersion.Type.PinsStoreFName else FName(reader.readFString())
        self.Mask = reader.readInt32()
        self.MaskR = reader.readInt32()
        self.MaskG = reader.readInt32()
        self.MaskB = reader.readInt32()
        self.MaskA = reader.readInt32()
        self.ExpressionName = reader.readFName() if reader.is_filter_editor_only else FName("None")

    @classmethod
    def default(cls: 'StructInterface') -> 'StructInterface':
        inst = cls.__new__(cls)
        inst.OutputIndex = 0
        inst.InputName = FName("None")
        inst.Mask = 0
        inst.MaskR = 0
        inst.MaskG = 0
        inst.MaskB = 0
        inst.MaskA = 0
        inst.ExpressionName = FName("None")
        return inst

    def GetValue(self) -> str:
        return {
            "OutputIndex": self.OutputIndex,
            "InputName": self.InputName.GetValue(),
            "Mask": self.Mask,
            "MaskR": self.MaskR,
            "MaskG": self.MaskG,
            "MaskB": self.MaskB,
            "MaskA": self.MaskA,
            "ExpressionName": self.ExpressionName.GetValue()
        }

class FMaterialInput(FExpressionInput):
    UseConstant: bool
    Constant: StructInterface
    TypeConstant: StructInterface

    def __call__(self, reader: FAssetReader):
        super().__init__(reader)
        self.UseConstant = reader.readBool()
        self.Constant = self.TypeConstant(reader)
        return self

    def __init__(self, t) -> None:
        self.TypeConstant = t

    # @classmethod
    def default(self: 'StructInterface') -> 'StructInterface':
        inst = super().default()
        inst.UseConstant = False
        inst.Constant = self.TypeConstant.default()
        return inst

    def GetValue(self):
        val = super().GetValue()
        val.update({
            "UseConstant": self.UseConstant,
            "Constant": self.Constant.GetValue()
        })
        return val
