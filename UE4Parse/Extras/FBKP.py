from typing import Dict, NamedTuple
from UE4Parse.Assets.Objects.Decompress import Decompress
from UE4Parse.BinaryReader import BinaryStream

Entry = NamedTuple('Entry', Size=int, IsEncrypted=bool, Path=str)

class FModelBackupReader:
    entries: Dict[str, Entry]

    def __init__(self, fp: BinaryStream) -> None:
        if not isinstance(fp, BinaryStream):
            stream = BinaryStream(fp)
            assert stream.size != -1
        else:
            stream = fp
        self.entries = {}

        if stream.readUInt32() == 0x184D2204:
            stream.seek(0, 0)
            stream = BinaryStream(Decompress(stream.read(), "LZ4", -1))

        while stream.position < stream.size:
            # stream.seek(8)
            # stream.seek(8)
            stream.seek(16)
            size = stream.readInt64()
            isEncrypted = stream.readFlag()
            stream.seek(4)
            _size = stream.read7BitEncodedInt()
            path = stream.readBytesAsString(_size)
            # path = stream.readBytesAsString(stream.read7BitEncodedInt())
            stream.seek(4)
            self.entries[path] = Entry(size, isEncrypted, path)

    def __getitem__(self, key):
        return self.entries[key]
    
    def get(self, path: str) -> Entry:
        if path in self.entries:
            return self.entries[path]
        return None

    def contains(self, path: str) -> bool:
        return path in self.entries

    def __len__(self):
        return len(self.entries)

# def encodeTo7bit(value):
#     data = []
#     number = abs(value)
#     while number >= 0x80:
#         data.append((number | 0x80) & 0xff)
#         number >>= 7
#     data.append(number & 0xff)
#     return b''.join(int.to_bytes(char, 1, 'little') for char in data)

# class FModelBackupWriter:
#     def __init__(self, fp) -> None:
#         self.fp = BinaryStream(fp)
#         self.read = self.fp.read

#     def write(self, entry: GameFile) -> None:
#         writer = self.fp
#         writer.writeUInt64(0)
#         writer.writeUInt64(0)
#         writer.writeInt64(entry.get_size())
#         writer.writeBool(entry.Encrypted)
#         writer.writeUInt32(0)
#         length = encodeTo7bit(len(entry.Name))
#         writer.write(length)
#         writer.writeBytes(bytes(entry.Name.lower(), 'utf-8'))
#         writer.writeUInt32(0)

#     def close(self) -> None:
#         self.fp.close()
    
#     def get_buffer(self) -> bytes:
#         return self.fp.read()
