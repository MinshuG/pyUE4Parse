from io import BytesIO
from typing import Optional
from PIL import Image

from UE4Parse.Exceptions import UnknownPixelFormatException
from UE4Parse.Assets.Objects.EPixelFormat import EPixelFormat
from .DXT.DXTDecompress import DXTBuffer


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
        self.decoded_image = None

    def decode(self, isNormalMap):
        if self.pixel_format == EPixelFormat.PF_DXT1:
            image_bytes = DXTBuffer(self.sizeX, self.sizeY).DXT1Decompress(self.data)
            self.decoded_image = Image.frombytes("RGBA", (self.sizeX, self.sizeY), image_bytes)
        elif self.pixel_format == EPixelFormat.PF_DXT5:
            image_bytes = DXTBuffer(self.sizeX, self.sizeY).DXT5Decompress(self.data)
            self.decoded_image = Image.frombytes("RGBA", (self.sizeX, self.sizeY), image_bytes)
        elif self.pixel_format == EPixelFormat.PF_BC5:
            from quicktex.s3tc.bc5 import BC5Decoder, BC5Texture
            t = BC5Texture.from_bytes(self.data.read(), self.sizeX, self.sizeY)
            image_bytes = BC5Decoder(0, 1).decode(t).tobytes()
            self.decoded_image = Image.frombytes("RGBA", (self.sizeX, self.sizeY), image_bytes)
            # inverted_image = ImageOps.invert(self.decoded_image.convert("RGB")) # normal maps?
            # inverted_image.show()
        elif self.pixel_format == EPixelFormat.PF_BC4:
            from quicktex.s3tc.bc4 import BC4Decoder, BC4Texture
            t = BC4Texture.from_bytes(self.data.read(), self.sizeX, self.sizeY)
            image_bytes = BC4Decoder(0, 1).decode(t).tobytes()
            self.decoded_image = Image.frombytes("RGBA", (self.sizeX, self.sizeY), image_bytes)
        elif self.pixel_format.name.startswith("PF_ASTC_"):
            import astc_decomp  # PIL Decoder
            block_width, block_height = str(self.pixel_format.name).lstrip("PF_ASTC_").split("x")

            is_srgb: bool = isNormalMap  # Normal Maps are Linear
            self.decoded_image = Image.frombytes('RGBA', (self.sizeX, self.sizeY), self.data.read(), 'astc',
                                                 (block_width, block_height, is_srgb))
            # TODO https://github.com/FabianFG/CUE4Parse/blob/1974d845229d29ac6b161bc2606b246113cb5994/CUE4Parse-Conversion/Textures/TextureDecoder.cs#L62
            # use decompress_astc
        else:
            raise UnknownPixelFormatException(f"Unsupported pixel format {self.pixel_format.name}")
