from setuptools import setup, find_packages
import pathlib


HERE = pathlib.Path(__file__).parent


README = (HERE / "README.md").read_text()


setup(
    name="UE4Parse",
    version="0.0.1",
    description=".pak and ue4 asset parser",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/MinshuG/UE4Parse",
    author="MinshuG",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=["pycryptodome", "lz4", "pyUsmap", "pillow"],
    packages=find_packages(),
)
