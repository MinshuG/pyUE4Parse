**pak and ue4 asset parser**


## Usages

<details>
<summary>Basic Usages</summary>

```python
from UE4Parse.Provider import FGame, Provider, MappingProvider
from UE4Parse.Versions.EUEVersion import EUEVersion
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

# import gc; gc.disable() # temporarily disabling garbage collector gives a huge performance boost
provider = Provider(path, mappings=mappings, GameInfo=game)
provider.read_paks(aeskeys)
# gc.enable() # enable garbage collector again

package_path = 'FortniteGame/Content/Animation/Game/MainPlayer/Skydive/ParaGlide/MechanicalEngineer/BS_MechanicalEngineer_Into_NoPack_GLIDER'

package = provider.get_package(package_path)
if package is not None:
    package.save_package("Assets")  # saves .uasset, .uexp etc.
    package.save_json("Assets")  # saves serialized json
```
</details>
<details>
<summary>Converting Textures</summary>

```python
package = provider.get_package(somepackagepath)
parsed_package = package.parse_package()
if texture := parsed_package.find_export_of_type("Texture2D"):
    image = texture.decode()  # returns PIL Image object
    image.save(f"{os.path.basename(os.path.splitext(package.get_name())[0])}.png", "PNG")  # save image
    # for more information refer to https://pillow.readthedocs.io/en/stable/reference/Image.html?highlight=Image#PIL.Image.Image
```
</details>


## Links

- [Trello](https://trello.com/b/yp0hx22L/pyue4parse)

## Notes for Developers

- Developers can use pyximport for development purposes 

    ```python 
    import pyximport
    pyximport.install()
    ```
