from io import BytesIO
from typing import Optional

from PIL import Image

from UE4Parse.Exceptions import UnknownPixelFormatException
from UE4Parse.Assets.Objects.EPixelFormat import EPixelFormat
from UE4Parse.Logger import get_logger


logger = get_logger(__name__)

try:
    from .utils import build_blue_channel
    from .utils import swap_b_and_r
except ImportError:
    logger.warning("Cython based texture decoder is not available. Slower Python implementation will be used.")
    from math import floor
    def build_blue_channel(data: bytearray, size_x: int, size_y: int):
        offset = 0
        i = 0
        # float uf, vf, t
        while i < size_x*size_y:
            i += 1
            u = data[offset]
            v = data[offset + 1]
            uf = u / 255.0 * 2 - 1
            vf = v / 255.0 * 2 - 1
            t = t  = 1.0 - uf * uf - vf * vf
            if t >= 0:
                data[offset+2] = floor((t + 1.0) * 127.5)
            else:
                data[offset+2] = 255
            offset += 4

    def swap_b_and_r(data: bytearray, size_x: int, size_y: int):
        offset = 0
        i = 0
        while i < size_x * size_y:
            i += 1
            b_ = data[offset]
            data[offset] = data[offset+2]  # replace b with r
            data[offset+2] = b_
            offset += 4


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

    def decode(self, is_normal_map):
        if self.pixel_format == EPixelFormat.PF_DXT1:  # https://en.wikipedia.org/wiki/S3_Texture_Compression
            from quicktex.s3tc.bc1 import BC1Decoder, BC1Texture
            t = BC1Texture.from_bytes(self.data.read(), self.sizeX, self.sizeY)
            image_bytes = BC1Decoder().decode(t).tobytes()
            self.decoded_image = Image.frombytes("RGBA", (self.sizeX, self.sizeY), image_bytes)  # doesn't have alpha
        elif self.pixel_format == EPixelFormat.PF_DXT5:
            from quicktex.s3tc.bc3 import BC3Decoder, BC3Texture
            t = BC3Texture.from_bytes(self.data.read(), self.sizeX, self.sizeY)
            image_bytes = BC3Decoder().decode(t).tobytes()
            if is_normal_map:
                image_bytes = bytearray(image_bytes)
                build_blue_channel(image_bytes, self.sizeX, self.sizeY)
            self.decoded_image = Image.frombytes("RGBA", (self.sizeX, self.sizeY), bytes(image_bytes))
        elif self.pixel_format == EPixelFormat.PF_BC5:  # missing some channel probably same as astc?
            from quicktex.s3tc.bc5 import BC5Decoder, BC5Texture
            t = BC5Texture.from_bytes(self.data.read(), self.sizeX, self.sizeY)
            image_bytes = BC5Decoder(0, 1).decode(t).tobytes()
            if is_normal_map:
                image_bytes = bytearray(image_bytes)
                build_blue_channel(image_bytes, self.sizeX, self.sizeY)
            self.decoded_image = Image.frombytes("RGBA", (self.sizeX, self.sizeY), bytes(image_bytes))
        elif self.pixel_format == EPixelFormat.PF_BC4:
            from quicktex.s3tc.bc4 import BC4Decoder, BC4Texture
            t = BC4Texture.from_bytes(self.data.read(), self.sizeX, self.sizeY)
            image_bytes = BC4Decoder(0, 1).decode(t).tobytes()
            self.decoded_image = Image.frombytes("RGBA", (self.sizeX, self.sizeY), image_bytes)
        elif self.pixel_format.name.startswith("PF_ASTC_"):
            from astc_decomp import decompress_astc
            block_width, block_height = str(self.pixel_format.name).lstrip("PF_ASTC_").split("x")

            is_srgb: bool = not is_normal_map  # Normal Maps are Linear
            image_bytes = decompress_astc(self.data.read(), self.sizeX, self.sizeY, block_width, block_height, is_srgb)
            if is_normal_map:
                image_bytes = bytearray(image_bytes)
                build_blue_channel(image_bytes, self.sizeX, self.sizeY)
            self.decoded_image = Image.frombytes("RGBA", (self.sizeX, self.sizeY), bytes(image_bytes))
        elif self.pixel_format == EPixelFormat.PF_B8G8R8A8:
            image_bytes = bytearray(self.data.read())
            swap_b_and_r(image_bytes, self.sizeX, self.sizeY)
            self.decoded_image = Image.frombytes('RGBA', (self.sizeX, self.sizeY), bytes(image_bytes))
        elif self.pixel_format == EPixelFormat.PF_G8:
            self.decoded_image = Image.frombytes('L', (self.sizeX, self.sizeY), self.data.read())  # L??
        elif self.pixel_format == EPixelFormat.PF_FloatRGBA:
            self.decoded_image = Image.frombytes('RGBA', (self.sizeX, self.sizeY), self.data.read())
        else:
            raise UnknownPixelFormatException(f"Unsupported pixel format {self.pixel_format.name}")
