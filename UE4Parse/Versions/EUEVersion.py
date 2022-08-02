from enum import IntEnum, auto

from UE4Parse.Versions.EUnrealEngineObjectUE4Version import UE4Versions


Versions = UE4Versions

def GAME_UE4(x: int):
    return 0x1000000 + (x << 4)

def GAME_UE5(x: int):  # can be better?
    return 0x2000000 + (x << 4)

class EUEVersion(IntEnum):
    GAME_UE4_0 = GAME_UE4(0)
    GAME_UE4_1 = GAME_UE4(1)
    GAME_UE4_2 = GAME_UE4(2)
    GAME_UE4_3 = GAME_UE4(3)
    GAME_UE4_4 = GAME_UE4(4)
    GAME_UE4_5 = GAME_UE4(5)
    GAME_UE4_6 = GAME_UE4(6)
    GAME_UE4_7 = GAME_UE4(7)
    GAME_UE4_8 = GAME_UE4(8)
    GAME_UE4_9 = GAME_UE4(9)
    GAME_UE4_10 = GAME_UE4(10)
    GAME_UE4_11 = GAME_UE4(11)
    GAME_UE4_12 = GAME_UE4(12)
    GAME_UE4_13 = GAME_UE4(13)
    GAME_UE4_14 = GAME_UE4(14)
    GAME_UE4_15 = GAME_UE4(15)
    GAME_UE4_16 = GAME_UE4(16)
    GAME_UE4_17 = GAME_UE4(17)
    GAME_UE4_18 = GAME_UE4(18)
    GAME_UE4_19 = GAME_UE4(19)
    GAME_UE4_20 = GAME_UE4(20)
    GAME_UE4_21 = GAME_UE4(21)
    GAME_UE4_22 = GAME_UE4(22)
    GAME_UE4_23 = GAME_UE4(23)
    GAME_UE4_24 = GAME_UE4(24)
    GAME_UE4_25 = GAME_UE4(25)
    GAME_UE4_26 = GAME_UE4(26)
    GAME_UE4_27 = GAME_UE4(27)

    GAME_UE5_0 = GAME_UE5(0)

    LATEST = GAME_UE5_0

    GAME_UE4_BASE = 0x1000000
    GAME_UE5_BASE = 0x2000000

    GAME_VALORANT = GAME_UE4_24 + 1

    def get_minor(self):
        minor = ((self.value - self.GAME_UE4_BASE.value) >> 4)
        return minor

    def get_ar_ver(self):  #TODO: deal with this
        if self.value >= self.GAME_UE5_0:
            return 1002
        versions = [Versions.VER_UE4_AUTOMATIC_VERSION, 342, 352, 363, 382, 385, 401, 413, 434, 451, 482, 482, 498, 504, 505, 508, 510, 513, 513, 514, 516, 516, 517, 517, 517, 518, 518, 522]

        return Versions(versions[self.get_minor()])
