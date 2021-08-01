from enum import Enum, auto


class EUnrealEngineObjectLicenseeUE4Version(Enum):
    VER_LIC_NONE = 0

    VER_LIC_AUTOMATIC_VERSION_PLUS_ONE = auto()
    VER_LIC_AUTOMATIC_VERSION = VER_LIC_AUTOMATIC_VERSION_PLUS_ONE - 1
