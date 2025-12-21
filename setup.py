"""Setup script for FileAlchemy package."""
from setuptools import setup, find_packages

# Read the README file for long description
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "Powerful and intuitive Python library for working with files, directories, and text data"

setup(
    name="FileAlchemy",
    version="1.1.1",
    author="GimpNiK",
    description="Powerful and intuitive Python library for working with files, directories, and text data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GimpNiK/FileAlchemy",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Filesystems",
        "Topic :: Utilities",
    ],
    python_requires=">=3.10",
    install_requires=[
        "chardet>=5.0.0",
        "py7zr>=0.20.0",
        "pyzipper>=0.3.6",
        "rarfile>=4.0",
    ],
    extras_require={
        "windows": ["pywin32>=300"],
    },
    include_package_data=True,
    package_data={
        "FileAlchemy": ["*.pyi"],
    },
)

