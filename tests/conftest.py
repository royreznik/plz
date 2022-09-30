from pathlib import Path
from typing import Generator, Tuple

import pytest as pytest
from click.testing import CliRunner


@pytest.fixture
def runner_and_path() -> Generator[Tuple[CliRunner, Path], None, None]:
    cli_runner = CliRunner(mix_stderr=False)
    with cli_runner.isolated_filesystem() as path:
        yield cli_runner, Path(path)


@pytest.fixture
def runner(runner_and_path: Tuple[CliRunner, Path]) -> Generator[CliRunner, None, None]:
    yield runner_and_path[0]


@pytest.fixture
def isolated_dir(
    runner_and_path: Tuple[CliRunner, Path]
) -> Generator[Path, None, None]:
    yield runner_and_path[1]


pytest.register_assert_rewrite(".utils")
