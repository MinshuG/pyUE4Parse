**UE4/5 Asset Parser**

<!-- ~[![pypi](https://img.shields.io/pypi/v/ue4parse.svg)](https://pypi.python.org/pypi/ue4parse) -->

## Installation
`python -m pip install git+https://github.com/MinshuG/pyUE4Parse.git`

## Features
* Parse UE4/5 asset files(.uasset, .umap, .uexp, .ubulk)
* Convert Textures to PIL Image object
* Convert assets to json
* Supports reading .pak/.utoc containers


## Usages

<details>
<summary>Basic Usages</summary>

```python
from UE4Parse.Assets.Objects.FGuid import FGuid
from UE4Parse.Provider import DefaultFileProvider, MappingProvider
from UE4Parse.Versions import EUEVersion, VersionContainer
from UE4Parse.Encryption import FAESKey

import logging

logging.getLogger("UE4Parse").setLevel(logging.INFO)  # set logging level

path = r"C:\Program Files\Epic Games\Fortnite\FortniteGame\Content\Paks"

aeskeys = {
    FGuid(0,0,0,0): FAESKey("0xFE478B39DF1B1D4E8D8DFD38272F216DBE933E7F80ADCC45DC4108D70428F37D"),
}

import gc; gc.disable() # temporarily disabling garbage collector gives a huge performance boost

provider = DefaultFileProvider(path, VersionContainer(EUEVersion.LATEST))
provider.initialize()
provider.submit_keys(aeskeys)  # mount files

gc.enable() # enable garbage collector again

provider.mappings = MappingProvider("path/to/mappings.usmap")

package_path = 'FortniteGame/Content/Animation/Game/MainPlayer/Skydive/ParaGlide/MechanicalEngineer/BS_MechanicalEngineer_Into_NoPack_GLIDER'

package = provider.try_load_package(package_path)
if package is not None:
    package_dict = package.get_dict() # get json serializable dict

    # write package_dict to json
    import json
    with open('something.json', 'w') as f:
        json.dump(package_dict, f, indent=4)
```
</details>

<details>
<summary>Converting Textures</summary>

```python
if texture := package.find_export_of_type("Texture2D"):
    image = texture.decode()  # returns PIL Image object
    image.save("cool_image.png", "PNG")  # save image
    # for more information refer to https://pillow.readthedocs.io/en/stable/reference/Image.html?highlight=Image#PIL.Image.Image
```
</details>


## Links

- [Trello](https://trello.com/b/yp0hx22L/pyue4parse)
- [CUE4Parse](https://github.com/FabianFG/CUE4Parse)
## Notes for Developers

- Developers can use pyximport for development purposes (loading cython extensions)

    ```python 
    import pyximport
    pyximport.install()
    ```
