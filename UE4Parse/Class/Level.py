from typing import List, Union, Optional

from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Class.UObjects import UObject
from UE4Parse.Objects.FObjectExport import FObjectExport
from UE4Parse.Objects.FObjectImport import FObjectImport
from UE4Parse.Objects.URL import FURL


class ULevel(UObject):
    URL: FURL
    Actors: List[Optional[Union[FObjectExport, FObjectImport]]]
    Model: List[Optional[Union[FObjectExport, FObjectImport]]]
    ModelComponents: List[Optional[Union[FObjectExport, FObjectImport]]]
    LevelScriptActor: Optional[Union[FObjectExport, FObjectImport]]
    NavListStart: Optional[Union[FObjectExport, FObjectImport]]
    NavListEnd: Optional[Union[FObjectExport, FObjectImport]]

    def __init__(self, reader: BinaryStream, validpos):
        super().__init__(reader, validpos)
        self.Actors = reader.readTArray(reader.readObject)
        self.URL = FURL(reader)
        self.Model = reader.readObject()
        self.ModelComponents = reader.readTArray(reader.readObject)
        self.LevelScriptActor = reader.readObject()
        self.NavListStart = reader.readObject()
        self.NavListEnd = reader.readObject()
        # rest later
