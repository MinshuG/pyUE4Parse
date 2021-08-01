**unfinished pak and ue4 asset parser**


### Usages

```python
from UE4Parse.Provider import FGame, Provider, MappingProvider
from UE4Parse.Assets.Objects.EUEVersion import EUEVersion
from UE4Parse.Encryption import FAESKey

import logging

logging.getLogger("UE4Parse").setLevel(logging.INFO)  # set logging level

path = r"C:\Program Files\Epic Games\Fortnite\FortniteGame\Content\Paks"

aeskeys = {
    "00000000000000000000000000000000": FAESKey("0xFE478B39DF1B1D4E8D8DFD38272F216DBE933E7F80ADCC45DC4108D70428F37D"),
    # main key
    "pakchunk1007-WindowsClient": FAESKey("397ba3ba988d44d4faf9bd60d5d8362173ed750c9fa0d3d4bafb60a9f5e79446"),
}

mappings = MappingProvider()

game = FGame()
game.UEVersion = EUEVersion.LATEST

provider = Provider(path, mappings=mappings, GameInfo=game)
provider = Provider(path)
provider.read_paks(aeskeys)

package_path = 'FortniteGame/Content/Animation/Game/MainPlayer/Skydive/ParaGlide/MechanicalEngineer/BS_MechanicalEngineer_Into_NoPack_GLIDER'

package = provider.get_package(package_path)
if package is not None:
    package.save_package("Assets")  # saves .uasset, .uexp etc.
    package.save_json("Assets")  # saves serialized json

```
