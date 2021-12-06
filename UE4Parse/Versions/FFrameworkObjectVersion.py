from enum import IntEnum, auto

from UE4Parse.Assets.Objects.FGuid import FGuid
from UE4Parse.Readers.FAssetReader import FAssetReader
from UE4Parse.Versions import EUEVersion
from UE4Parse.Versions.EUeBase import EUeBase


class FFrameworkObjectVersion(EUeBase):
    class Type(IntEnum):
            # Before any version changes were made
            BeforeCustomVersionWasAdded = 0

            # BodySetup's default instance collision profile is used by default when creating a new instance.
            UseBodySetupCollisionProfile = auto()

            # Regenerate subgraph arrays correctly in animation blueprints to remove duplicates and add
            # missing graphs that appear read only when edited
            AnimBlueprintSubgraphFix = auto()

            # Static and skeletal mesh sockets now use the specified scale
            MeshSocketScaleUtilization = auto()

            # Attachment rules are now explicit in how they affect location, rotation and scale
            ExplicitAttachmentRules = auto()

            # Moved compressed anim data from uasset to the DDC
            MoveCompressedAnimDataToTheDDC = auto()

            # Some graph pins created using legacy code seem to have lost the RF_Transactional flag,
            # which causes issues with undo. Restore the flag at this version
            FixNonTransactionalPins = auto()

            # Create new struct for SmartName, and use that for CurveName
            SmartNameRefactor = auto()

            # Add Reference Skeleton to Rig
            AddSourceReferenceSkeletonToRig = auto()

            # Refactor ConstraintInstance so that we have an easy way to swap behavior paramters
            ConstraintInstanceBehaviorParameters = auto()

            # Pose Asset support mask per bone
            PoseAssetSupportPerBoneMask = auto()

            # Physics Assets now use SkeletalBodySetup instead of BodySetup
            PhysAssetUseSkeletalBodySetup = auto()

            # Remove SoundWave CompressionName
            RemoveSoundWaveCompressionName = auto()

            # Switched render data for clothing over to unreal data, reskinned to the simulation mesh
            AddInternalClothingGraphicalSkinning = auto()

            # Wheel force offset is now applied at the wheel instead of vehicle COM
            WheelOffsetIsFromWheel = auto()

            # Move curve metadata to be saved in skeleton
            # Individual asset still saves some flag - i.e. disabled curve and editable or not, but
            # major flag - i.e. material types - moves to skeleton and handle in one place
            MoveCurveTypesToSkeleton = auto()

            # Cache destructible overlaps on save
            CacheDestructibleOverlaps = auto()

            # Added serialization of materials applied to geometry cache objects
            GeometryCacheMissingMaterials = auto()

            # Switch static & skeletal meshes to calculate LODs based on resolution-independent screen size
            LODsUseResolutionIndependentScreenSize = auto()

            # Blend space post load verification
            BlendSpacePostLoadSnapToGrid = auto()

            # Addition of rate scales to blend space samples
            SupportBlendSpaceRateScale = auto()

            # LOD hysteresis also needs conversion from the LODsUseResolutionIndependentScreenSize version
            LODHysteresisUseResolutionIndependentScreenSize = auto()

            # AudioComponent override subtitle priority default change
            ChangeAudioComponentOverrideSubtitlePriorityDefault = auto()

            # Serialize hard references to sound files when possible
            HardSoundReferences = auto()

            # Enforce const correctness in Animation Blueprint function graphs
            EnforceConstInAnimBlueprintFunctionGraphs = auto()

            # Upgrade the InputKeySelector to use a text style
            InputKeySelectorTextStyle = auto()

            # Represent a pins container type as an enum not 3 independent booleans
            EdGraphPinContainerType = auto()

            # Switch asset pins to store as string instead of hard object reference
            ChangeAssetPinsToString = auto()

            # Fix Local Variables so that the properties are correctly flagged as blueprint visible
            LocalVariablesBlueprintVisible = auto()

            # Stopped serializing UField_Next so that UFunctions could be serialized in dependently of a UClass
            # in order to allow us to do all UFunction loading in a single pass (after classes and CDOs are created):
            RemoveUField_Next = auto()

            # Fix User Defined structs so that all members are correct flagged blueprint visible
            UserDefinedStructsBlueprintVisible = auto()

            # FMaterialInput and FEdGraphPin store their name as FName instead of FString
            PinsStoreFName = auto()

            # User defined structs store their default instance, which is used for initializing instances
            UserDefinedStructsStoreDefaultInstance = auto()

            # Function terminator nodes serialize an FMemberReference rather than a name/class pair
            FunctionTerminatorNodesUseMemberReference = auto()

            # Custom event and non-native interface event implementations add 'const' to reference parameters
            EditableEventsUseConstRefParameters = auto()

            # No longer serialize the legacy flag that indicates this state, as it is now implied since we don't serialize the skeleton CDO
            BlueprintGeneratedClassIsAlwaysAuthoritative = auto()

            # Enforce visibility of blueprint functions - e.g. raise an error if calling a private function from another blueprint:
            EnforceBlueprintFunctionVisibility = auto()

            # ActorComponents now store their serialization index
            StoringUCSSerializationIndex = auto()

            # -----<new versions can be added above this line>-------------------------------------------------
            VersionPlusOne = auto()
            LatestVersion = VersionPlusOne - 1,

    GUID = FGuid(0xCFFC743F, 0x43B04480, 0x939114DF, 0x171D2073)

    def __init__(self):
        pass

    def get(self, reader: FAssetReader):
            ver = reader.CustomVer(self.GUID)
            if ver > 0:
                return self.Type(ver)

            if reader.game < EUEVersion.GAME_UE4_12:
                    return self.Type.BeforeCustomVersionWasAdded
            elif reader.game < EUEVersion.GAME_UE4_13:
                    return self.Type.FixNonTransactionalPins
            elif reader.game < EUEVersion.GAME_UE4_14:
                    return self.Type.RemoveSoundWaveCompressionName
            elif reader.game < EUEVersion.GAME_UE4_15:
                    return self.Type.GeometryCacheMissingMaterials
            elif reader.game < EUEVersion.GAME_UE4_16:
                    return self.Type.ChangeAudioComponentOverrideSubtitlePriorityDefault
            elif reader.game < EUEVersion.GAME_UE4_17:
                    return self.Type.HardSoundReferences
            elif reader.game < EUEVersion.GAME_UE4_18:
                    return self.Type.LocalVariablesBlueprintVisible
            elif reader.game < EUEVersion.GAME_UE4_19:
                    return self.Type.UserDefinedStructsBlueprintVisible
            elif reader.game < EUEVersion.GAME_UE4_20:
                    return self.Type.FunctionTerminatorNodesUseMemberReference
            elif reader.game < EUEVersion.GAME_UE4_22:
                    return self.Type.EditableEventsUseConstRefParameters
            elif reader.game < EUEVersion.GAME_UE4_24:
                    return self.Type.BlueprintGeneratedClassIsAlwaysAuthoritative
            elif reader.game < EUEVersion.GAME_UE4_25:
                    return self.Type.EnforceBlueprintFunctionVisibility
            elif reader.game < EUEVersion.GAME_UE4_26:
                    return self.Type.StoringUCSSerializationIndex
            else:
                    return self.Type.LatestVersion
