from .UObjects import UObject

exports = {}


def register_export(cls=None, Type=None):
    def wrapper(cls, _type=None):
        if Type is not None:
            _type = Type
        if _type is None:
            _type: str = cls.__name__
            if _type.startswith(("U", "A")):
                _type = _type[1:]
        exports[_type] = cls
        return cls

    if cls is None:
        return wrapper
    return wrapper(cls, Type)


class Registry:
    def __init__(self) -> None:
        pass

    def get_export_reader(self, export_type: str, export, reader):
        r = exports.get(export_type, UObject)(reader)
        r.type = export_type
        r.flag = export.ObjectFlags
        return r
