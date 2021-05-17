from enum import IntEnum, auto

from UE4Parse import Logger
from UE4Parse.Objects import FName
from UE4Parse.Objects import FPropertyTag
from UE4Parse.Objects.FGuid import FGuid
from UE4Parse.PropertyTagData.ArrayProperty import ArrayProperty
from UE4Parse.PropertyTagData.BoolProperty import BoolProperty
from UE4Parse.PropertyTagData.ByteProperty import ByteProperty
from UE4Parse.PropertyTagData.DelegateProperty import DelegateProperty
from UE4Parse.PropertyTagData.DoubleProperty import DoubleProperty
from UE4Parse.PropertyTagData.EnumProperty import EnumProperty
from UE4Parse.PropertyTagData.FloatProperty import FloatProperty
from UE4Parse.PropertyTagData.IntProperty import *
from UE4Parse.PropertyTagData.LazyObjectProperty import LazyObjectProperty
from UE4Parse.PropertyTagData.MapProperty import MapProperty
from UE4Parse.PropertyTagData.NameProperty import NameProperty
from UE4Parse.PropertyTagData.ObjectProperty import ObjectProperty
from UE4Parse.PropertyTagData.SetProperty import SetProperty
from UE4Parse.PropertyTagData.SoftObjectProperty import SoftObjectProperty
from UE4Parse.PropertyTagData.StrProperty import StrProperty
from UE4Parse.PropertyTagData.StructProperty import StructProperty
from UE4Parse.PropertyTagData.TextProperty import TextProperty

logger = Logger.get_logger(__name__)


class ReadType(IntEnum):
    NORMAL = 0
    MAP = auto()
    ARRAY = auto()


def switch(toCompare, CompareTo):
    if toCompare == CompareTo:
        return True
    else:
        return False


def ReadAsObject(reader, tag: FPropertyTag = None, type_: FName = None, readType: ReadType = None):
    type_ = type_.string

    prop: object
    if switch("ByteProperty", type_):
        prop = ByteProperty(reader,  readType,tag)
    elif switch("BoolProperty", type_):
        prop = BoolProperty(reader, tag, readType)
    elif switch("IntProperty", type_):
        prop = IntProperty(reader)
    elif switch("FloatProperty", type_):
        prop = FloatProperty(reader)
    elif switch("ObjectProperty", type_):
        prop = ObjectProperty(reader)
    elif switch("NameProperty", type_):
        prop = NameProperty(reader)
    elif switch("DelegateProperty", type_):
        prop = DelegateProperty(reader)
    elif switch("DoubleProperty", type_):
        prop = DoubleProperty(reader)
    elif switch("ArrayProperty", type_):
        prop = ArrayProperty(reader, tag)
    elif switch("StructProperty", type_):
        prop = StructProperty(reader, tag)
    elif switch("StrProperty", type_):
        prop = StrProperty(reader)
    elif switch("TextProperty", type_):
        prop = TextProperty(reader)
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
        prop = UInt64Property(reader)
    elif switch("UInt32Property", type_):
        prop = UInt32Property(reader)
    elif switch("UInt16Property", type_):
        prop = UInt16Property(reader)
    elif switch("Int64Property", type_):
        prop = Int64Property(reader)
    elif switch("Int16Property", type_):
        prop = Int16Property(reader)
    elif switch("Int8Property", type_):
        prop = Int8Property(reader)
    elif switch("MapProperty", type_):
        prop = MapProperty(reader, tag)
    elif switch("SetProperty", type_):
        prop = SetProperty(reader, tag)
    elif switch("EnumProperty", type_):
        prop = EnumProperty(reader, tag, readType)
    elif switch("Guid", type_):
        prop = FGuid(reader).read()
    else:
        return None

    return prop


def ReadAsValue(reader, tag: FPropertyTag = None, type_: FName = None, readType: ReadType = None):
    return ReadAsObject(reader, tag, type_, readType).GetValue()
