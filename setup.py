from setuptools import setup
from plz import __version__

DEPENDENCIES = ["pip-tools", "virtualenv", "click"]

setup(
    name="plz",
    version=__version__,
    author="Roy Reznik",
    author_email="royreznik@gmail.com",
    license="MIT License",
    keywords="CLI wrapping over virtualenv and pip-tools",
    packages=["plz"],
    install_requires=DEPENDENCIES,
    entry_points={
        "console_scripts": [
            "plz = plz:cli",
        ],
    },
)
