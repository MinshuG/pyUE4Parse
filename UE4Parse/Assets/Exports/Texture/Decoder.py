from UE4Parse.Exceptions.Exceptions import UnknownPixelFormatException
from typing import Optional
from UE4Parse.Assets.Objects.EPixelFormat import EPixelFormat
from PIL import Image
from .DXT.DXTDecompress import DXTBuffer
from io import BytesIO

class TextureDecoder:
    pixel_format: EPixelFormat
    sizeX: int
    sizeY: int
    sizeZ: int
    decoded_image: Optional[Image.Image] = None

    def __init__(self, data, sizeX, sizeY, sizeZ, pixel_format) -> None:
        self.data = BytesIO(data)
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.sizeZ = sizeZ
        self.pixel_format = pixel_format
        self.decoded_data = None
    
    def decode(self):
        if self.pixel_format == EPixelFormat.PF_DXT1:
            image_bytes = DXTBuffer(self.sizeX, self.sizeY).DXT1Decompress(self.data)
            self.decoded_image = Image.frombytes("RGBA", (self.sizeX, self.sizeY), image_bytes)
            return True
        elif self.pixel_format == EPixelFormat.PF_DXT5:
            image_bytes = DXTBuffer(self.sizeX, self.sizeY).DXT5Decompress(self.data)
            self.decoded_image = Image.frombytes("RGBA", (self.sizeX, self.sizeY), image_bytes)
            return True
        else:
            raise UnknownPixelFormatException("Unsupported pixel format")
