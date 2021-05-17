# https://github.com/MinshuG/pyUsmap/blob/master/Usmap/Oodle.py

import ctypes
import io
import lzma
import os
import urllib.request


def load_lib() -> bool:
    OODLE_DLL_NAME = "oo2core_8_win64.dll"
    libname = os.path.abspath(
        os.path.join(os.getcwd(), OODLE_DLL_NAME)
    )
    if not os.path.exists(libname):
        HOST = "https://origin.warframe.com"
        indexLink = "https://origin.warframe.com" + "/origin/E926E926/index.txt.lzma"
        print(f"{OODLE_DLL_NAME} not found in cwd, Downloading it...")

        urllib.request.urlretrieve(indexLink, "index.lzma")
        with open("index.lzma", "rb") as f:
            dlldata = lzma.decompress(f.read(), format=lzma.FORMAT_AUTO)

        a = io.BytesIO(dlldata)
        lines = a.readlines()
        for x in lines:
            if OODLE_DLL_NAME in str(x):
                urllib.request.urlretrieve(HOST + str(x).split(",")[0][2:], "dll.lzma")
                with open("dll.lzma", "rb") as dll:
                    with open(libname, "wb") as f:
                        f.write(lzma.decompress(dll.read(), format=lzma.FORMAT_AUTO))
                break

        if not os.path.exists(libname):
            print(f"Failed to download {OODLE_DLL_NAME}")

        filesToDelete = ["index.lzma", "dll.lzma"]
        for x in filesToDelete:
            if os.path.exists(x):
                os.remove(x)

    try:
        global lib
        lib = ctypes.windll.LoadLibrary(libname)
        return True
    except Exception as e:
        print("Failed to load library", e)
        return False


def Decompress(buffer: bytes, decompressLength: int):
    lenBuffer = len(buffer)
    result = ctypes.create_string_buffer(decompressLength)
    decompLength = OodleLZ_Decompress(buffer, lenBuffer, result, decompressLength)
    return result


def OodleLZ_Decompress(
        buffer: bytes,
        bufferSize: int,
        result: bytes,
        outputBufferSize: int,
        a: int = 0,
        b: int = 0,
        c: int = 0,
        d: int = 0,
        e: int = 0,
        f: int = 0,
        g: int = 0,
        h: int = 0,
        i: int = 0,
        ThreadModule: int = 3,
):
    if load_lib():
        data = lib.OodleLZ_Decompress(
            buffer,
            bufferSize,
            result,
            outputBufferSize,
            a,
            b,
            c,
            d,
            e,
            f,
            g,
            h,
            i,
            ThreadModule,
        )
        return data
    else:
        raise Exception("Oodle dll is not loaded")
