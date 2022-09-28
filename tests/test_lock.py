import shlex
from pathlib import Path

from click.testing import CliRunner

from plz.__main__ import cli
from plz.commands.init import DEFAULT_REQUIREMENTS_FILE


# Sanity check
def test_lock_create_lock_file(runner: CliRunner, isolated_dir: Path) -> None:
    (isolated_dir / DEFAULT_REQUIREMENTS_FILE).touch()
    # noinspection PyTypeChecker
    result = runner.invoke(cli, "lock")
    assert "Successfully lock requirements" in result.stdout

    assert (isolated_dir / "requirements.in").exists()


def test_lock_work_with_compile_argument(runner: CliRunner, isolated_dir: Path) -> None:
    (isolated_dir / DEFAULT_REQUIREMENTS_FILE).touch()
    # noinspection PyTypeChecker
    result = runner.invoke(cli, shlex.split("lock --pip-args '--progress-bar off'"))
    assert "Successfully lock requirements" in result.stdout

    assert (isolated_dir / "requirements.in").exists()
