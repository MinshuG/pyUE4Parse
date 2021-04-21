from typing import List, Dict

from UE4Parse.IoObjects.FScriptObjectDesc import FScriptObjectDesc
from UE4Parse.Objects.FNameEntrySerialized import FNameEntrySerialized


class FIoGlobalData:
    GlobalNameMap: List[FNameEntrySerialized]
    GlobalNameHashes: list
    ScriptObjectByGlobalId: Dict[str, FScriptObjectDesc]

    def __init__(self):
        pass