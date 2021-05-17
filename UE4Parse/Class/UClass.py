#  test
import inspect


class UClass:  # ik this should be base class for other all but who cares
    def __init__(self):
        pass

    def GetValue(self):
        Dict = {}
        for i in inspect.getmembers(self):
            if not i[0].startswith('_'):
                if i[0] not in ["reader", "position"]:  # and str(type(i[1])) not in dir(builtins):
                    if hasattr(i[1], "GetValue"):
                        Dict[i[0]] = i[1].GetValue()
                    else:
                        Dict[i[0]] = i[1]
        return Dict
