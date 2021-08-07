from enum import IntEnum, auto


class EReleaseObjectVersion(IntEnum):
    # Before any version changes were made
    BeforeCustomVersionWasAdded = 0

    # Static Mesh extended bounds radius fix
    StaticMeshExtendedBoundsFix = auto()

    # Physics asset bodies are either in the sync scene or the async scene, but not both
    NoSyncAsyncPhysAsset = auto()

    # ULevel was using TTransArray incorrectly (serializing the entire array in addition to individual mutations).
    # converted to a TArray = auto(
    LevelTransArrayConvertedToTArray = auto()

    # Add Component node templates now use their own unique naming scheme to ensure more reliable archetype lookups.
    AddComponentNodeTemplateUniqueNames = auto()

    # Fix a serialization issue with static mesh FMeshSectionInfoMap FProperty
    UPropertryForMeshSectionSerialize = auto()

    # Existing HLOD settings screen size to screen area conversion
    ConvertHLODScreenSize = auto()

    # Adding mesh section info data for existing billboard LOD models
    SpeedTreeBillboardSectionInfoFixup = auto()

    # Change FMovieSceneEventParameters::StructType to be a string asset reference from a TWeakObjectPtr<UScriptStruct>
    EventSectionParameterStringAssetRef = auto()

    # Remove serialized irradiance map data from skylight.
    SkyLightRemoveMobileIrradianceMap = auto()

    # rename bNoTwist to bAllowTwist
    RenameNoTwistToAllowTwistInTwoBoneIK = auto()

    # Material layers serialization refactor
    MaterialLayersParameterSerializationRefactor = auto()

    # Added disable flag to skeletal mesh data
    AddSkeletalMeshSectionDisable = auto()

    # Removed objects that were serialized as part of this material feature
    RemovedMaterialSharedInputCollection = auto()

    # HISMC Cluster Tree migration to add new data
    HISMCClusterTreeMigration = auto()

    # Default values on pins in blueprints could be saved incoherently
    PinDefaultValuesVerified = auto()

    # During copy and paste transition getters could end up with broken state machine references
    FixBrokenStateMachineReferencesInTransitionGetters = auto()

    # Change to MeshDescription serialization
    MeshDescriptionNewSerialization = auto()

    # Change to not clamp RGB values > 1 on linear color curves
    UnclampRGBColorCurves = auto()

    # Bugfix for FAnimObjectVersion::LinkTimeAnimBlueprintRootDiscovery.
    LinkTimeAnimBlueprintRootDiscoveryBugFix = auto()

    # Change trail anim node variable deprecation
    TrailNodeBlendVariableNameChange = auto()

    # Make sure the Blueprint Replicated Property Conditions are actually serialized properly.
    PropertiesSerializeRepCondition = auto()

    # DepthOfFieldFocalDistance at 0 now disables DOF instead of DepthOfFieldFstop at 0.
    FocalDistanceDisablesDOF = auto()

    # Removed versioning, but version entry must still exist to keep assets saved with this version loadable
    Unused_SoundClass2DReverbSend = auto()

    # Groom asset version
    GroomAssetVersion1 = auto()
    GroomAssetVersion2 = auto()

    # Store applied version of Animation Modifier to use when reverting
    SerializeAnimModifierState = auto()

    # Groom asset version
    GroomAssetVersion3 = auto()

    # Upgrade filmback
    DeprecateFilmbackSettings = auto()

    # custom collision type
    CustomImplicitCollisionType = auto()

    # FFieldPath will serialize the owner struct reference and only a short path to its property
    FFieldPathOwnerSerialization = auto()

    # Dummy version to allow us to fix up the fact that ReleaseObjectVersion was changed elsewhere
    ReleaseObjectVersionFixup = auto()

    # Pin types include a flag that propagates the 'CPF_UObjectWrapper' flag to generated properties
    PinTypeIncludesUObjectWrapperFlag = auto()

    # Added Weight member to FMeshToMeshVertData
    WeightFMeshToMeshVertData = auto()

    # Animation graph node bindings displayed as pins
    AnimationGraphNodeBindingsDisplayedAsPins = auto()

    # Serialized rigvm offset segment paths
    SerializeRigVMOffsetSegmentPaths = auto()

    # Upgrade AbcGeomCacheImportSettings for velocities
    AbcVelocitiesSupport = auto()

    # Add margin support to Chaos Convex
    MarginAddedToConvexAndBox = auto()

    # Add structure data to Chaos Convex
    StructureDataAddedToConvex = auto()

    # -----<new versions can be added above this line>-------------------------------------------------
    VersionPlusOne = auto()
    LatestVersion = VersionPlusOne - 1
