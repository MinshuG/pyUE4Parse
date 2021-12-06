from UE4Parse.Assets.Objects.FName import FName
from UE4Parse.Assets.Objects.FPackageIndex import FPackageIndex
from UE4Parse.Assets.UObject.CoreNetTypes import ELifetimeCondition
from UE4Parse.Assets.UObject.FField import FField
from UE4Parse.Readers.FAssetReader import FAssetReader


class FProperty(FField):
    ArrayDim: int
    ElementSize: int
    PropertyFlags: int
    RepIndex: int
    RepNotifyFunc: FName
    BlueprintReplicationCondition: ELifetimeCondition

    def __init__(self):
        self.ArrayDim = 0
        self.ElementSize = 0
        self.PropertyFlags = 0
        self.RepIndex = 0
        self.RepNotifyFunc = FName("None", 0)
        self.BlueprintReplicationCondition = ELifetimeCondition.COND_None
        super().__init__()

    def deserialize(self, reader: FAssetReader):
        self.ArrayDim = reader.readInt32()
        self.ElementSize = reader.readInt32()
        self.PropertyFlags = reader.readUInt64()
        self.RepIndex = reader.readUInt16()
        self.RepNotifyFunc = reader.readFName()
        self.BlueprintReplicationCondition = ELifetimeCondition(reader.readUInt8())

    def GetValue(self):
        props = super().GetValue()
        props.update({
            "ArrayDim": self.ArrayDim,
            "ElementSize": self.ElementSize,
            "PropertyFlags": self.PropertyFlags,
            "RepIndex": self.RepIndex,
            "RepNotifyFunc": self.RepNotifyFunc,
            "BlueprintReplicationCondition": self.BlueprintReplicationCondition.value
        })
        return props


class FObjectProperty(FProperty):
    PropertyClass: FPackageIndex

    def deserialize(self, reader: FAssetReader):
        super().deserialize(reader)
        self.PropertyClass = FPackageIndex(self.reader)

    def GetValue(self):
        props = super().GetValue()
        props.update({
            "PropertyClass": self.PropertyClass.GetValue()
        })
        return props


class FArrayProperty(FProperty):
    Inner: FProperty

    def deserialize(self):
        super().deserialize()
        self.Inner = self.serialize_single_field(self.reader)

    def GetValue(self):
        props = super().GetValue()
        props.update({
            "Inner": self.Inner.GetValue()
        })
        return props

class FBoolProperty(FProperty):
    FieldSize: int
    ByteOffset: int
    ByteMask: int
    FieldMask: int
    BoolSize: int
    bIsNativeBool: bool

    def deserialize(self):
        super().deserialize()
        self.FieldSize = self.reader.readInt8()
        self.ByteOffset = self.reader.readInt8()
        self.ByteMask = self.reader.readInt8()
        self.FieldMask = self.reader.readInt8()
        self.BoolSize = self.reader.readInt8()
        self.bIsNativeBool = self.reader.readFlag()

    def GetValue(self):
        props = super().GetValue()
        props.update({
            "FieldSize": self.FieldSize,
            "ByteOffset": self.ByteOffset,
            "ByteMask": self.ByteMask,
            "FieldMask": self.FieldMask,
            "BoolSize": self.BoolSize,
            "bIsNativeBool": self.bIsNativeBool
        })
        return props

class FNumericProperty(FProperty): pass

class FByteProperty(FNumericProperty):
    Enum: FPackageIndex

    def deserialize(self):
        super().deserialize()
        self.Enum = FPackageIndex(self.reader)

    def GetValue(self):
        props = super().GetValue()
        props.update({
            "Enum": self.Enum.GetValue()
        })
        return props

class FClassProperty(FObjectProperty):
    MetaClass: FPackageIndex

    def deserialize(self):
        super().deserialize()
        self.MetaClass = FPackageIndex(self.reader)

    def GetValue(self):
        props = super().GetValue()
        props.update({
            "MetaClass": self.MetaClass.GetValue()
        })
        return props

class FDelegateProperty(FProperty):
    SignatureFunction: FPackageIndex

    def deserialize(self):
        super().deserialize()
        self.SignatureFunction = FPackageIndex(self.reader)

    def GetValue(self):
        props = super().GetValue()
        props.update({
            "SignatureFunction": self.SignatureFunction.GetValue()
        })
        return props

class FEnumProperty(FProperty):
    UnderlyingProp: FNumericProperty
    Enum: FPackageIndex

    def deserialize(self):
        super().deserialize()
        self.Enum = FPackageIndex(self.reader)
        self.UnderlyingProp = self.serialize_single_field(self.reader)

    def GetValue(self):
        props = super().GetValue()
        props.update({
            "UnderlyingProp": self.UnderlyingProp.GetValue(),
            "Enum": self.Enum.GetValue()
        })
        return props

class FFieldPathProperty(FProperty):
    PropertyClass: FName

    def deserialize(self):
        super().deserialize()
        self.PropertyClass = self.reader.readFName()

    def GetValue(self):
        props = super().GetValue()
        props.update({
            "PropertyClass": self.PropertyClass
        })
        return props

class FFloatProperty(FNumericProperty): pass
class FInt16Property(FNumericProperty): pass
class FInt64Property(FNumericProperty): pass
class FInt8Property(FNumericProperty): pass
class FIntProperty(FNumericProperty): pass

class FInterfaceProperty(FProperty):
    InterfaceClass: FPackageIndex

    def deserialize(self):
        super().deserialize()
        self.InterfaceClass = FPackageIndex(self.reader)

    def GetValue(self):
        props = super().GetValue()
        props.update({
            "InterfaceClass": self.InterfaceClass.GetValue()
        })
        return props

class FMapProperty(FProperty):
    KeyProp: FProperty
    ValueProp: FProperty

    def deserialize(self):
        super().deserialize()
        self.KeyProp = self.serialize_single_field(self.reader)
        self.ValueProp = self.serialize_single_field(self.reader)

    def GetValue(self):
        props = super().GetValue()
        props.update({
            "KeyProp": self.KeyProp.GetValue(),
            "ValueProp": self.ValueProp.GetValue()
        })
        return props

class FMulticastDelegateProperty(FProperty):
    SignatureFunction: FPackageIndex

    def deserialize(self):
        super().deserialize()
        self.SignatureFunction = FPackageIndex(self.reader)

    def GetValue(self):
        props = super().GetValue()
        props.update({
            "SignatureFunction": self.SignatureFunction.GetValue()
        })
        return props

class FMulticastInlineDelegateProperty(FProperty):
    SignatureFunction: FPackageIndex

    def deserialize(self):
        super().deserialize()
        self.SignatureFunction = FPackageIndex(self.reader)

    def GetValue(self):
        props = super().GetValue()
        props.update({
            "SignatureFunction": self.SignatureFunction.GetValue()
        })
        return props

class FNameProperty(FProperty): pass

class FSoftClassProperty(FObjectProperty):
    MetaClass: FPackageIndex

    def deserialize(self):
        super().deserialize()
        self.MetaClass = FPackageIndex(self.reader)

    def GetValue(self):
        props = super().GetValue()
        props.update({
            "MetaClass": self.MetaClass.GetValue()
        })
        return props

class FSoftObjectProperty(FObjectProperty): pass

class FSetProperty(FProperty):
    ElementProp: FProperty

    def deserialize(self):
        super().deserialize()
        self.ElementProp = self.serialize_single_field(self.reader)

    def GetValue(self):
        props = super().GetValue()
        props.update({
            "ElementProp": self.ElementProp.GetValue()
        })
        return props


class FStrProperty(FProperty): pass

class FStructProperty(FProperty):
    Struct: FPackageIndex

    def deserialize(self):
        super().deserialize()
        self.Struct = FPackageIndex(self.reader)

    def GetValue(self):
        props = super().GetValue()
        props.update({
            "Struct": self.Struct.GetValue()
        })
        return props

class FTextProperty(FProperty): pass
class FUInt16Property(FNumericProperty): pass
class FUInt32Property(FNumericProperty): pass
class FUInt64Property(FNumericProperty): pass

