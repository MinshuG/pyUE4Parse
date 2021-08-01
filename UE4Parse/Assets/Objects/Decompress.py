

def Decompress(buffer: bytes, method, decompressSize = 0) -> bytes:
    if method == "Oodle":
        from UE4Parse.Oodle import Decompress as OoDecompress
        result = OoDecompress(buffer=buffer, decompressLength=decompressSize)
        assert len(result) == decompressSize
        return result
    elif method == "Gzip":
        from gzip import decompress as gDecompress
        result = gDecompress(buffer)
        assert len(result) == decompressSize
        return result
    elif method == "Zlib":
        from zlib import decompress as zDecompress
        result = zDecompress(buffer, bufsize=decompressSize)
        assert len(result) == decompressSize
        return result
    elif method == "LZ4":
        from lz4.frame import LZ4FrameDecompressor
        lz4Decompress = LZ4FrameDecompressor().decompress
        result = lz4Decompress(buffer, max_length=decompressSize)
        assert len(result) == decompressSize
        return result
    else:
        raise NotImplementedError("Unknown Compression Method " + str(method))
