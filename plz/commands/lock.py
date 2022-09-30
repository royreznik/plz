from typing import Any

import click
from piptools.__main__ import compile as _compile


@click.command("lock")
@click.pass_context
def lock(ctx: click.Context, *args: Any, **kwargs: Any) -> None:
    ctx.forward(_compile.cli, *args, **kwargs)
    click.secho("Successfully lock requirements.")


lock.params += _compile.cli.params
