from UE4Parse.BinaryReader import BinaryStream
from UE4Parse.Objects.EPixelFormat import EPixelFormat
from .DXTDecoder import *

def switch(format,format2):
    if format.value == format2.value:
        return True
    return False

class TDecoder:
    """Texture Decoder"""
    
    def __init__(self) -> None:
        pass
    

    def DecodeImage(sequence: bytes,  width: int,  height: int,  depth: int, pixelformat: EPixelFormat):
        if switch(pixelformat,EPixelFormat.PF_DXT5):
            data = DecodeDXT5(sequence, width, height, depth)
        elif switch(pixelformat,EPixelFormat.PF_DXT1) :
            data = DecodeDXT1(sequence, width, height, depth)

