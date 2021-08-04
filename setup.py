try:
    from Cython.Build import cythonize
except:
    cythonize = None

from setuptools import Extension, setup, find_packages
import pathlib

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

extensions = [
    Extension(
        name="tex_utils",
        sources=["UE4Parse/Assets/Exports/Textures/utils.pyx"])
]

if cythonize:
    extensions = cythonize(extensions)

setup(
    name="UE4Parse",
    version="0.0.1",
    description="ue4 asset parser",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/MinshuG/UE4Parse",
    author="MinshuG",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=["pycryptodome", "lz4", "pyUsmap", "pillow", "quicktex", "astc_decomp"],
    packages=find_packages(),
    ext_modules=extensions
)
