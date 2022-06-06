from typing import List, Dict

# from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.IO.IoObjects.FIoChunkId import FIoChunkId
from UE4Parse.IO.IoStoreReader import FFileIoStoreReader
from UE4Parse.IoObjects.EIoChunkType import EIoChunkType, EIoChunkType5
from UE4Parse.IoObjects.FMappedName import FMappedName
from UE4Parse.IoObjects.FPackageObjectIndex import FPackageObjectIndex
from UE4Parse.IoObjects.FScriptObjectDesc import FScriptObjectDesc
from UE4Parse.IoObjects.FScriptObjectEntry import FScriptObjectEntry
from UE4Parse.Assets.Objects.FNameEntrySerialized import FNameEntrySerialized
from UE4Parse.Logger import get_logger
from UE4Parse.Versions import EUEVersion

logger = get_logger(__name__)


class FIoGlobalData:
    GlobalNameMap: List[FNameEntrySerialized] = []
    # GlobalNameHashes: list = []
    ScriptObjectByGlobalId: Dict[FPackageObjectIndex, FScriptObjectDesc]

    def __init__(self, globalreader: FFileIoStoreReader, version: EUEVersion):
        logger.info("Reading Global Data...")
        if version >= EUEVersion.GAME_UE5_0 :
            initialLoadIoReader = globalreader.Read(FIoChunkId().construct(0, 0, EIoChunkType5.ScriptObjects))

            FNameEntrySerialized().LoadNameBatch2(self.GlobalNameMap, initialLoadIoReader)
        else:
            globalNamesReader = globalreader.Read(FIoChunkId().construct(0, 0, EIoChunkType.LoaderGlobalNames))
            globalNameHashReader = globalreader.Read(FIoChunkId().construct(0, 0, EIoChunkType.LoaderGlobalNameHashes))

            hashCount = int(globalNameHashReader.size / 8 - 1)
            globalNameHashReader.close()
            FNameEntrySerialized().LoadNameBatch(self.GlobalNameMap, globalNamesReader, hashCount)
            globalNamesReader.close()
            initialLoadIoReader = globalreader.Read(FIoChunkId().construct(0, 0, EIoChunkType.LoaderInitialLoadMeta))

        numScriptObjects = initialLoadIoReader.readInt32()
        # scriptObjectByGlobalIdKeys = []
        # scriptObjectByGlobalIdValues = []
        ScriptObjectByGlobalId = {}

        for i in range(numScriptObjects):
            scriptObjectEntry = FScriptObjectEntry(initialLoadIoReader, self.GlobalNameMap)
            # print(scriptObjectEntry.ObjectName.GetValue())
            # globalIndices[scriptObjectEntry.GlobalIndex.typeAndId] = i
            mappedName = FMappedName(scriptObjectEntry.ObjectName, self.GlobalNameMap, None)

            # scriptObjectByGlobalIdKeys.append(scriptObjectEntry.GlobalIndex)
            # scriptObjectByGlobalIdValues.append(
            #     FScriptObjectDesc(self.GlobalNameMap[mappedName.GetIndex()], mappedName, scriptObjectEntry))
            ScriptObjectByGlobalId[scriptObjectEntry.GlobalIndex.typeAndId] = FScriptObjectDesc(self.GlobalNameMap[mappedName.GetIndex()], mappedName, scriptObjectEntry)

        self.ScriptObjectByGlobalId = ScriptObjectByGlobalId
