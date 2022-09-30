from pathlib import Path
from typing import Any, Dict

import click
from piptools.__main__ import compile as _compile


@click.command("lock")
@click.pass_context
@click.pass_obj
def lock(obj: Dict[str, Path], ctx: click.Context, *args: Any, **kwargs: Any) -> None:
    kwargs["src_files"] = [
        str(obj["path"] / "requirements.in"),
    ]
    ctx.forward(_compile.cli, *args, **kwargs)
    kwargs["src_files"] = [
        str(obj["path"] / "dev-requirements.in"),
    ]
    ctx.forward(_compile.cli, *args, **kwargs)
    click.secho("Successfully lock requirements.")


lock.params += _compile.cli.params
