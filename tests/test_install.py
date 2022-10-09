import shlex
import subprocess
import sys
from pathlib import Path
from typing import cast

import click
import pytest
from click.testing import CliRunner
from virtualenv.discovery.py_info import PythonInfo

from plz.plz_cli import VIRTUALENV_DIR_NAME, cli
from tests.utils import assert_cli_output


def test_install_create_virtualenv(runner: CliRunner, isolated_dir: Path) -> None:
    create_python_package_files(isolated_dir)
    result = runner.invoke(cast(click.Command, cli), shlex.split("install"))
    assert_cli_output(result)
    assert (isolated_dir / VIRTUALENV_DIR_NAME).exists()


def test_install_sync_requirements(runner: CliRunner, isolated_dir: Path) -> None:
    create_python_package_files(isolated_dir)
    (isolated_dir / "requirements.txt").write_text("0")
    # noinspection DuplicatedCode
    result = runner.invoke(cast(click.Command, cli), shlex.split("install"))
    assert_cli_output(result)
    python_path = (
        isolated_dir
        / VIRTUALENV_DIR_NAME
        / PythonInfo().install_path("scripts")
        / Path("python").with_suffix(".exe" if sys.platform == "win32" else "")
    )
    assert subprocess.run(
        [python_path, "-c", "import importlib;importlib.import_module('0')"], check=True
    )


def test_install_sync_dev_requirements(runner: CliRunner, isolated_dir: Path) -> None:
    create_python_package_files(isolated_dir)
    (isolated_dir / "dev-requirements.txt").write_text("0")
    # noinspection DuplicatedCode
    result = runner.invoke(cast(click.Command, cli), shlex.split("install"))
    assert_cli_output(result)
    python_path = (
        isolated_dir
        / VIRTUALENV_DIR_NAME
        / PythonInfo().install_path("scripts")
        / Path("python").with_suffix(".exe" if sys.platform == "win32" else "")
    )
    assert subprocess.run(
        [python_path, "-c", "import importlib;importlib.import_module('0')"], check=True
    )


def test_install_sync_only_production_requirements(
    runner: CliRunner, isolated_dir: Path
) -> None:
    create_python_package_files(isolated_dir)
    (isolated_dir / "requirements.txt").write_text("0")
    (isolated_dir / "dev-requirements.txt").write_text("requests")
    result = runner.invoke(
        cast(click.Command, cli), shlex.split("install --production")
    )
    assert_cli_output(result)
    python_path = (
        isolated_dir
        / VIRTUALENV_DIR_NAME
        / PythonInfo().install_path("scripts")
        / Path("python").with_suffix(".exe" if sys.platform == "win32" else "")
    )
    assert subprocess.run(
        [python_path, "-c", "import importlib;importlib.import_module('0')"], check=True
    )
    with pytest.raises(subprocess.CalledProcessError):
        assert subprocess.run(
            [python_path, "-c", "import importlib;importlib.import_module('requests')"],
            check=True,
        )


def test_install_sync_root(runner: CliRunner, isolated_dir: Path) -> None:
    create_python_package_files(isolated_dir)
    result = runner.invoke(cast(click.Command, cli), shlex.split("install"))
    assert_cli_output(result)
    python_path = (
        isolated_dir
        / VIRTUALENV_DIR_NAME
        / PythonInfo().install_path("scripts")
        / Path("python").with_suffix(".exe" if sys.platform == "win32" else "")
    )
    assert subprocess.run([python_path, "-Ic", "import wtf"], check=True)


def test_install_sync_no_root(runner: CliRunner, isolated_dir: Path) -> None:
    create_python_package_files(isolated_dir)
    # noinspection PyTypeChecker
    result = runner.invoke(cli, shlex.split("install --no-root"))
    assert_cli_output(result)
    python_path = (
        isolated_dir
        / VIRTUALENV_DIR_NAME
        / PythonInfo().install_path("scripts")
        / Path("python").with_suffix(".exe" if sys.platform == "win32" else "")
    )
    with pytest.raises(subprocess.CalledProcessError):
        assert subprocess.run([python_path, "-Ic", "import wtf"], check=True)


def create_python_package_files(isolated_dir: Path) -> None:
    (isolated_dir / "requirements.txt").touch()
    (isolated_dir / "dev-requirements.txt").touch()
    (isolated_dir / "setup.py").write_text(
        "from setuptools import setup; setup(name='wtf', packages=['wtf'])"
    )
    (isolated_dir / "wtf").mkdir()
    (isolated_dir / "wtf" / "__init__.py").touch()
