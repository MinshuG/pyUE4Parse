class FIoDirectoryIndexHandle:
    _handle: int
    InvalidHandle: int = 4294967295
    Root = 0

    def __init__(self, handle: int = None):
        if handle is not None:
            self._handle = handle
        else:
            self._handle = self.InvalidHandle

    def ToIndex(self):
        return self._handle

    def isValid(self):
        return self._handle != self.InvalidHandle

