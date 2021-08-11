from abc import ABC, abstractmethod


class GameFile(ABC):
    Name: str
    Encrypted: bool
    CompressionMethodIndex: int
    ContainerName: str

    def __init__(self):
        pass

    @abstractmethod
    def get_data(self):
        pass

    def __repr__(self):
        return f"<Name={self.Name}>"
