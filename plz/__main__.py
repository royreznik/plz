from pathlib import Path

import click

from .commands import init, lock, install


# noinspection PyTypeChecker
@click.group()
@click.pass_context
@click.option("-p", "--path", type=click.Path(exists=True, path_type=Path, file_okay=False))
def cli(ctx: click.Context, path: Path) -> None:
    path = path or Path.cwd()
    ctx.obj = {
        "path": path
    }


# noinspection PyTypeChecker
cli.add_command(init)
# noinspection PyTypeChecker
cli.add_command(lock)
# noinspection PyTypeChecker
cli.add_command(install)

if __name__ == "__main__":
    cli()
