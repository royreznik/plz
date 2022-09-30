from pathlib import Path

from setuptools import setup

DEPENDENCIES = Path("requirements.in").read_text().split()

setup(
    name="plz",
    version="0.0.0",
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
