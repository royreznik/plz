from pathlib import Path
from setuptools import setup, find_packages

DEPENDENCIES = Path("requirements.in").read_text().splitlines()

__version__ = "0.2.0"

readme = Path("README.md").read_text("UTF-8")

setup(
    name="plz",
    version=__version__,
    author="Roy Reznik",
    author_email="royreznik@gmail.com",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "plz = plz:cli",
        ],
    },
    install_requires=DEPENDENCIES,
    python_requires=">=3.8, <4",
    url="https://github.com/royreznik/plz",
    license="MIT License",
    description="plz is lightweight and simple virtual environment and dependencies manager, wrapping virtualenv and piptools together",
    long_description=readme,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Systems Administration",
        "Typing :: Typed",
    ],
)
