from typing import Dict

import click

DEFAULT_REQUIREMENTS_FILE = "requirements.in"


@click.command("init")
@click.pass_obj
def init(config: Dict) -> None:
    requirements_file = config["path"] / DEFAULT_REQUIREMENTS_FILE
    if requirements_file.exists():
        raise click.BadParameter(
            f"Path {requirements_file} already have {DEFAULT_REQUIREMENTS_FILE},"
            f"did you meant to run `plz install`?"
        )
    requirements_file.touch()
    click.secho(
        "Requirements file created!" "You can add requirements and run `plz install`",
        fg="green",
    )
