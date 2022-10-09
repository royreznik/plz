import shlex
from pathlib import Path

from click.testing import CliRunner

from plz.plz_cli import cli
from tests.utils import assert_cli_output


# Sanity check
def test_lock_create_lock_file(runner: CliRunner, isolated_dir: Path) -> None:
    (isolated_dir / "requirements.in").touch()
    (isolated_dir / "dev-requirements.in").touch()
    # noinspection PyTypeChecker
    result = runner.invoke(cli, shlex.split("lock"))
    assert_cli_output(result, expected_stdout="Successfully lock requirements")

    assert (isolated_dir / "requirements.txt").exists()
    assert (isolated_dir / "dev-requirements.txt").exists()


def test_lock_work_with_compile_argument(runner: CliRunner, isolated_dir: Path) -> None:
    (isolated_dir / "requirements.in").touch()
    (isolated_dir / "dev-requirements.in").touch()
    # noinspection PyTypeChecker
    result = runner.invoke(cli, shlex.split("lock --pip-args '--progress-bar off'"))
    assert_cli_output(result, expected_stdout="Successfully lock requirements")

    assert (isolated_dir / "requirements.txt").exists()
    assert (isolated_dir / "dev-requirements.txt").exists()
