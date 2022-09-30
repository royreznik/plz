from pathlib import Path
from typing import Dict

import click

REQUIREMENTS_FILE = "requirements.in"
DEV_REQUIREMENTS_FILE = "dev-requirements.in"


@click.command("init")
@click.pass_obj
def init(config: Dict[str, Path]) -> None:
    requirements_file = config["path"] / REQUIREMENTS_FILE
    dev_requirements_file = config["path"] / DEV_REQUIREMENTS_FILE
    if requirements_file.exists() and dev_requirements_file.exists():
        raise click.BadParameter(
            f"Path {requirements_file} already have {REQUIREMENTS_FILE} and {DEV_REQUIREMENTS_FILE},"
            f"did you meant to run `plz install`?"
        )
    requirements_file.touch()
    dev_requirements_file.write_text("-r requirements.in\n-e .\n")
    click.secho(
        "Requirements file created!" "You can add requirements and run `plz install`",
        fg="green",
    )
