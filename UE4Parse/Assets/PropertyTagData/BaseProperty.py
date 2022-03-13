from enum import IntEnum, auto

from UE4Parse import Logger
from UE4Parse.Assets.Objects.FName import FName
from UE4Parse.Assets.Objects.FPropertyTag import FPropertyTag
from UE4Parse.Assets.Objects.FGuid import FGuid
from UE4Parse.Assets.PropertyTagData.ArrayProperty import ArrayProperty
from UE4Parse.Assets.PropertyTagData.BoolProperty import BoolProperty
from UE4Parse.Assets.PropertyTagData.ByteProperty import ByteProperty
from UE4Parse.Assets.PropertyTagData.DelegateProperty import DelegateProperty
from UE4Parse.Assets.PropertyTagData.DoubleProperty import DoubleProperty
from UE4Parse.Assets.PropertyTagData.EnumProperty import EnumProperty
from UE4Parse.Assets.PropertyTagData.FloatProperty import FloatProperty
from UE4Parse.Assets.PropertyTagData.IntProperty import IntProperty, UInt64Property, UInt32Property, UInt16Property, \
    Int64Property, Int16Property, Int8Property
from UE4Parse.Assets.PropertyTagData.LazyObjectProperty import LazyObjectProperty
from UE4Parse.Assets.PropertyTagData.MapProperty import MapProperty
from UE4Parse.Assets.PropertyTagData.NameProperty import NameProperty
from UE4Parse.Assets.PropertyTagData.ObjectProperty import ObjectProperty
from UE4Parse.Assets.PropertyTagData.SetProperty import SetProperty
from UE4Parse.Assets.PropertyTagData.SoftObjectProperty import SoftObjectProperty
from UE4Parse.Assets.PropertyTagData.StrProperty import StrProperty
from UE4Parse.Assets.PropertyTagData.StructProperty import StructProperty
from UE4Parse.Assets.PropertyTagData.TextProperty import TextProperty

logger = Logger.get_logger(__name__)


class ReadType(IntEnum):
    """
    `NORMAL` = `0`\n
    `MAP` = `1`\n
    `ARRAY` = `2`\n
    `ZERO` = `3`\n
    """
    NORMAL = 0
    MAP = auto()
    ARRAY = auto()
    ZERO = auto()

def switch(toCompare, CompareTo):
    return toCompare == CompareTo


def ReadAsObject(reader, tag: FPropertyTag = None, type_: FName = None, readType: ReadType = None):
    type_ = type_.string if isinstance(type_, FName) else type_

    prop: object
    if switch("ByteProperty", type_):
        if enum := getattr(tag, "EnumName", None):
            if not enum.isNone:
                prop = EnumProperty(reader, tag, readType)
            else:
                prop = ByteProperty(reader,  readType, tag)
        else:
            prop = ByteProperty(reader,  readType, tag)
    elif switch("BoolProperty", type_):
        prop = BoolProperty(reader, tag, readType)
    elif switch("IntProperty", type_):
        prop = IntProperty(reader, readType)
    elif switch("FloatProperty", type_):
        prop = FloatProperty(reader, readType)
    elif switch("ObjectProperty", type_):
        prop = ObjectProperty(reader, readType)
    elif switch("NameProperty", type_):
        prop = NameProperty(reader, readType)
    elif switch("DelegateProperty", type_):
        prop = DelegateProperty(reader, readType)
    elif switch("DoubleProperty", type_):
        prop = DoubleProperty(reader, readType)
    elif switch("ArrayProperty", type_):
        prop = ArrayProperty(reader, tag, readType)
    elif switch("StructProperty", type_):
        prop = StructProperty(reader, tag, readType)
    elif switch("StrProperty", type_):
        prop = StrProperty(reader, readType)
    elif switch("TextProperty", type_):
        prop = TextProperty(reader, readType)
    # elif switch("InterfaceProperty", type_):
    #     prop = InterfaceProperty(reader)
    # # elif switch("MulticastDelegateProperty", type_):
    #     # prop = MulticastDelegateProperty(reader, tag)
    elif switch("LazyObjectProperty", type_):
        prop = LazyObjectProperty(reader, readType)  # (reader, tag)
    elif switch("SoftObjectProperty", type_):
        prop = SoftObjectProperty(reader, readType)
    elif switch("AssetObjectProperty", type_):
        prop = SoftObjectProperty(reader, readType)
    elif switch("UInt64Property", type_):
        prop = UInt64Property(reader, readType)
    elif switch("UInt32Property", type_):
        prop = UInt32Property(reader, readType)
    elif switch("UInt16Property", type_):
        prop = UInt16Property(reader, readType)
    elif switch("Int64Property", type_):
        prop = Int64Property(reader, readType)
    elif switch("Int16Property", type_):
        prop = Int16Property(reader, readType)
    elif switch("Int8Property", type_):
        prop = Int8Property(reader, readType)
    elif switch("MapProperty", type_):
        prop = MapProperty(reader, tag, readType)
    elif switch("SetProperty", type_):
        prop = SetProperty(reader, tag, readType)
    elif switch("EnumProperty", type_):
        prop = EnumProperty(reader, tag, readType)
    elif switch("Guid", type_):
        if readType == ReadType.ZERO:
            prop = FGuid(0, 0, 0, 0)
        else:
            prop = FGuid(reader)
    else:
        return None

    return prop


def ReadAsValue(reader, tag: FPropertyTag = None, type_: FName = None, readType: ReadType = None):
    return ReadAsObject(reader, tag, type_, readType).GetValue()
