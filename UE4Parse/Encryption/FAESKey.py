from typing import Union
from functools import cached_property
from Crypto.Cipher import AES


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
        return AES.new(self.__key, AES.MODE_ECB)

    def decrypt(self, data: Union[bytearray, bytes]) -> bytes:
        assert len(data) % 16 == 0
        return self.decryptor.decrypt(data)
