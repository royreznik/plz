import shlex
from pathlib import Path

from click.testing import CliRunner

from plz.__main__ import cli
from plz.commands.consts import DEFAULT_REQUIREMENTS_FILE


def test_init_create_expected_files_in_cwd(
    runner: CliRunner, isolated_dir: Path
) -> None:
    # noinspection PyTypeChecker
    result = runner.invoke(cli, "init")
    assert "Requirements file created" in result.stdout

    assert (isolated_dir / DEFAULT_REQUIREMENTS_FILE).exists()


def test_init_create_expected_files_in_path(
    runner: CliRunner, isolated_dir: Path
) -> None:
    new_dir = isolated_dir / "dir"
    new_dir.mkdir()
    # noinspection PyTypeChecker
    result = runner.invoke(cli, shlex.split("-p dir init"))
    assert "Requirements file created" in result.stdout

    assert (new_dir / DEFAULT_REQUIREMENTS_FILE).exists()


def test_init_fails_on_files_already_exists(
    runner: CliRunner, isolated_dir: Path
) -> None:
    (isolated_dir / DEFAULT_REQUIREMENTS_FILE).touch()
    # noinspection PyTypeChecker
    result = runner.invoke(cli, "init")
    assert result.exit_code != 0
    assert "already have requirements.in" in result.stderr
