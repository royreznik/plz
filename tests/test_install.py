import shlex
import subprocess
import sys
from pathlib import Path

import pytest
from click.testing import CliRunner
from virtualenv.discovery.py_info import PythonInfo

from plz.__main__ import cli
from plz.commands.install import VIRTUALENV_DIR_NAME
from tests.utils import assert_cli_output


def test_install_create_virtualenv(runner: CliRunner, isolated_dir: Path) -> None:
    # noinspection PyTypeChecker
    (isolated_dir / "requirements.txt").write_text("")
    (isolated_dir / "dev-requirements.txt").write_text("")

    runner.invoke(cli, shlex.split("install"))
    assert (isolated_dir / VIRTUALENV_DIR_NAME).exists()


def test_install_sync_requirements(runner: CliRunner, isolated_dir: Path) -> None:
    (isolated_dir / "requirements.txt").write_text("0")
    (isolated_dir / "dev-requirements.txt").write_text("")
    # noinspection PyTypeChecker
    result = runner.invoke(cli, shlex.split("install"))
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
    (isolated_dir / "requirements.txt").write_text("")
    (isolated_dir / "dev-requirements.txt").write_text("0")
    # noinspection PyTypeChecker
    result = runner.invoke(cli, shlex.split("install"))
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
    (isolated_dir / "requirements.txt").write_text("0")
    (isolated_dir / "dev-requirements.txt").write_text("requests")
    # noinspection PyTypeChecker
    result = runner.invoke(cli, shlex.split("install --production"))
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
