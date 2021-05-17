
def fixpath(path: str, GameName: str) -> str:
    if path.startswith("/Game/"):
        path = path.replace("/Game/", GameName + "/Content/")

    return path
