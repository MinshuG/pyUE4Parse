from UE4Parse import Globals as glob


def fixpath(path: str) -> str:
    GameName = glob.FGame.GameName
    if path.startswith("/Game/"):
        path = path.replace("/Game/", GameName + "/Content/")

    return path
