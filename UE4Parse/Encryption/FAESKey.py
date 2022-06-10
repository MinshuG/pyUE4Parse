from typing import Union
from functools import cached_property

from UE4Parse.Logger import get_logger
logger = get_logger(__name__)

try:
    CryptoAval = True
    from Crypto.Cipher import AES
except ImportError:
    CryptoAval = False
    logger.warn("AES decryption unavailable(pycryptodome is not installed)")

class FAESKey:
    __key: bytearray
    block_size = 16

    @property
    def key_string(self) -> str:
        return self.__key.hex()

    def __init__(self, key: Union[bytearray, bytes, str]):
        if isinstance(key, bytearray):
            assert len(key) == 32
            self.__key = key
        elif isinstance(key, str):
            key = key[2:] if key.lower().startswith("0x") else key
            assert len(key) == 64  # 66 - 2 no 0x
            self.__key = bytearray.fromhex(key)
        elif isinstance(key, bytes):
            assert len(key) == 32
            self.__key = bytearray(key)
        else:
            raise TypeError("key must be bytes, bytearray or str")

    @cached_property
    def decryptor(self) -> AES.new:
        if not CryptoAval:
            raise ImportError("AES decryption unavailable pycryptodome is not installed")
        return AES.new(self.__key, AES.MODE_ECB)

    def decrypt(self, data: Union[bytearray, bytes]) -> bytes:
        return self.decryptor.decrypt(data)
