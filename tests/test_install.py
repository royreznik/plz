import shlex
import subprocess
import sys
from pathlib import Path

from click.testing import CliRunner
from virtualenv.discovery.py_info import PythonInfo

from plz.__main__ import cli
from plz.commands.install import VIRTUALENV_DIR_NAME


def test_install_create_virtualenv(runner: CliRunner, isolated_dir: Path) -> None:
    # noinspection PyTypeChecker
    runner.invoke(cli, shlex.split("install"))
    assert (isolated_dir / VIRTUALENV_DIR_NAME).exists()


def test_install_sync_requirements(runner: CliRunner, isolated_dir: Path) -> None:
    (isolated_dir / "requirements.txt").write_text("0")
    # noinspection PyTypeChecker
    runner.invoke(cli, shlex.split("install"))
    python_path = (
        isolated_dir
        / VIRTUALENV_DIR_NAME
        / PythonInfo().install_path("scripts")
        / Path(sys.executable).name
    )
    assert subprocess.run(
        [python_path, "-c", "import importlib;importlib.import_module('0')"], check=True
    )
