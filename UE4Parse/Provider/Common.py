
class GameFile:
    Name: str
    Encrypted: bool
    CompressionMethodIndex: int
    ContainerName: str

    def __init__(self):
        pass

    def __repr__(self):
        return f"<Name={self.Name}>"
