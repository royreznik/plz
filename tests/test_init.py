import shlex
from pathlib import Path

from click.testing import CliRunner

from plz.plz_cli import REQUIREMENTS_FILE, cli
from tests.utils import assert_cli_output


def test_init_create_expected_files_in_cwd(
    runner: CliRunner, isolated_dir: Path
) -> None:
    # noinspection PyTypeChecker
    result = runner.invoke(cli, "init")
    assert "Requirements file created" in result.stdout

    assert (isolated_dir / REQUIREMENTS_FILE).exists()


def test_init_create_expected_files_in_path(
    runner: CliRunner, isolated_dir: Path
) -> None:
    new_dir = isolated_dir / "dir"
    new_dir.mkdir()
    # noinspection PyTypeChecker
    result = runner.invoke(cli, shlex.split("-p dir init"))
    assert "Requirements file created" in result.stdout

    assert (new_dir / REQUIREMENTS_FILE).exists()


def test_init_fails_on_files_already_exists(
    runner: CliRunner, isolated_dir: Path
) -> None:
    (isolated_dir / REQUIREMENTS_FILE).touch()
    # noinspection PyTypeChecker
    result = runner.invoke(cli, "init")
    assert_cli_output(
        result,
    )
