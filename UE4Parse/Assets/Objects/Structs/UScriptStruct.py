from enum import IntEnum
from typing import Dict, Type
from UE4Parse import Logger
from UE4Parse.Assets.Exports import UObjects
from UE4Parse.Assets.Objects.FGuid import FGuid
from UE4Parse.Assets.Objects.Common import StructInterface
from UE4Parse.Assets.Objects.Structs.Box import FBox, FBox2D
from UE4Parse.Assets.Objects.Structs.Colors import FColor, FLinearColor
from UE4Parse.Assets.Objects.Structs.CurveKey import FSimpleCurveKey, FRichCurveKey
from UE4Parse.Assets.Objects.Structs.FFrameNumber import FFrameNumber
from UE4Parse.Assets.Objects.Structs.FGameplayTagContainer import FGameplayTagContainer
from UE4Parse.Assets.Objects.Structs.FIntPoint import FIntPoint
from UE4Parse.Assets.Objects.Structs.FLevelSequenceObjectReferenceMap import FLevelSequenceObjectReferenceMap
from UE4Parse.Assets.Objects.Structs.FNavAgentSelectorCustomization import FNavAgentSelectorCustomization
from UE4Parse.Assets.Objects.Structs.FPerPlatform import FPerPlatformInt, FPerPlatformFloat
from UE4Parse.Assets.Objects.Structs.FRotator import FRotator
from UE4Parse.Assets.Objects.Structs.FSmartName import FSmartName
from UE4Parse.Assets.Objects.Structs.FSoftObjectPath import FSoftObjectPath
from UE4Parse.Assets.Objects.Structs.Vector import FVector2D, FVector, FVector4
from UE4Parse.Assets.Objects.Meshes.FSkeletalMeshSamplingLODBuiltData import FSkeletalMeshSamplingLODBuiltData
from UE4Parse.BinaryReader import BinaryStream

logger = Logger.get_logger(__name__)


def switch(toCompare, CompareTo):  # wtf was this?
    return toCompare == CompareTo


def FallBackReader(reader: BinaryStream, structName=None):
    fallbackobj = UObjects.UObject(reader, True)
    fallbackobj.type = structName
    fallbackobj.deserialize(0)
    return fallbackobj

class ZeroStruct: # TODO
    def GetValue(self):
        return "None"

class UScriptStruct:
    Struct: StructInterface

    def __init__(self, reader: BinaryStream, StructName: str, readType: IntEnum) -> None:
        if readType.value == 3:
            # self.Struct = ZeroStruct()
            print("zero read!!!")
            # return

        self.read(reader, StructName, readType)

    def read(self, reader: BinaryStream, StructName: str, readType):
        Structs: Dict[str, Type[StructInterface]] = {
            "NavAgentSelector": FNavAgentSelectorCustomization,
            "GameplayTagContainer": FGameplayTagContainer,
            "Vector2D": FVector2D,
            "Vector": FVector,
            "Vector4": FVector4,
            "Quat": FVector4,
            "Rotator": FRotator,
            "SoftObjectPath": FSoftObjectPath,
            "SoftClassPath": FSoftObjectPath,
            "Guid": FGuid,
            "Color": FColor,
            "LinearColor": FLinearColor,
            "IntPoint": FIntPoint,
            "LevelSequenceObjectReferenceMap": FLevelSequenceObjectReferenceMap,
            "Box": FBox,
            "Box2D": FBox2D,
            "SimpleCurveKey": FSimpleCurveKey,
            "RichCurveKey": FRichCurveKey,
            "MovieSceneFloatValue": FRichCurveKey,
            "FrameNumber": FFrameNumber,
            "MovieSceneTrackIdentifier": FFrameNumber,
            "MovieSceneSegmentIdentifier": FFrameNumber,
            "MovieSceneSequenceID": FFrameNumber,
            "SmartName": FSmartName,
            "PerPlatformInt": FPerPlatformInt,
            "PerPlatformFloat": FPerPlatformFloat,
            "SkeletalMeshSamplingLODBuiltData": FSkeletalMeshSamplingLODBuiltData
        }  # type: ignore

        if StructName in Structs:
            if readType.value == 3: # zero
                self.Struct = Structs[StructName].default()
            else:
                self.Struct = Structs[StructName](reader)
        else:
            # logger.debug(f"Unsupported Struct {StructName}, using Fallback reader.")
            self.Struct = FallBackReader(reader, StructName)

    def GetValue(self):
        return self.Struct.GetValue()
