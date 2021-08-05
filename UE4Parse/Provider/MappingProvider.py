from Usmap.main import Struct
from UE4Parse.Exceptions.Exceptions import ParserException
import os
from urllib.request import urlopen, Request
import json

from Usmap import Usmap


class PropMappings:

    def __init__(self, struct: Struct, provider: 'MappingProvider') -> None:
        self.struct = struct
        self.provider = provider

    def TryGetProp(self, index: int):
        if index <= self.struct.PropertyCount-1:  # len(props)
            return self.struct.props[index]
        elif self.struct.SuperIndex is not None:
            super_ = self.provider.get_schema_by_index(self.struct.SuperIndex)
            if super_ is None:
                return None
            return super_.TryGetProp(index - self.struct.PropertyCount)


class MappingProvider:
    __mappings: Usmap

    def __init__(self, fp=None) -> None:
        if fp == None:
            if self._check_mappings():
                filepath = self._find_latest_Mappings()
                with open(filepath, "rb") as f:
                    self.__mappings = Usmap(f).read()
            else:
                raise FileNotFoundError("mappings not found")
        else:
            self.__mappings = Usmap(fp).read()

    def get_schema(self, Type: str):
        schema = self.__mappings.Mappings.get(Type)
        if schema is None:
            return None
        return PropMappings(schema, self)

    def get_schema_by_index(self, Index: int):
        """Index: `int` NameMap Entry Index"""
        if Index > len(self.__mappings.NameMap):
            return None
        Type = self.__mappings.NameMap[Index]
        return self.get_schema(Type)

    def get_enum(self, Type: str):
        return self.__mappings.Enums.get(Type)

    def _find_latest_Mappings(self):
        import glob
        list_of_files = glob.glob(os.getcwd() + "/mappings/*.usmap")
        latest_file = max(list_of_files, key=os.path.getctime)
        return latest_file

    def _check_mappings(self):
        path = os.getcwd()
        mappings_path = os.path.join(path, "mappings")
        if not os.path.exists(mappings_path):
            os.makedirs(mappings_path)
            self._dl_mappings(mappings_path)
            return True
        try:
            self._dl_mappings(mappings_path)
            return True
        except Exception as e:
            pass
        return os.path.exists(mappings_path)

    def _dl_mappings(self, path):
        ENDPOINT = "https://benbot.app/api/v1/mappings"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
            "accept": "application/json"
        }

        req = Request(url=ENDPOINT, headers=headers)
        r = urlopen(req)
        data = json.loads(r.read().decode(r.info().get_param("charset") or "utf-8"))

        if not os.path.exists(os.path.join(path,data[0]["fileName"])):
            with open(os.path.join(path,data[0]["fileName"]),"wb") as f:
                downfile = urlopen(Request(url=data[0]["url"], headers=headers))
                print("Downloading",data[0]["fileName"])
                f.write(downfile.read(downfile.length))
        return True
