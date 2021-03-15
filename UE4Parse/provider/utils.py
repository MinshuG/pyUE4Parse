from UE4Parse.Globals import FGame


def fixpath(path: str) -> str:
    GameName = FGame.GameName
    if path.startswith("/Game/"):
        path = path.replace("/Game/", GameName + "/Content/")

    return path
