from pathlib import Path
from typing import Optional

import click

from .consts import REQUIREMENTS_FILE


# noinspection PyTypeChecker
@click.command("init")
@click.option("-p", "--path", type=click.Path(exists=True, path_type=Path))
def init(path: Optional[Path] = None) -> None:
    path = path or Path.cwd()
    requirements_file = path / REQUIREMENTS_FILE
    if requirements_file.exists():
        raise click.BadParameter(
            f"Path {requirements_file} already have {REQUIREMENTS_FILE},"
            f"did you meant to run `plz install`?"
        )
    requirements_file.touch()
    click.secho('Requirements file created!'
                'You can add requirements and run `plz install`', fg='green')
