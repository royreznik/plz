import click

from .commands import init


@click.group()
def cli() -> None:
    pass


# noinspection PyTypeChecker
cli.add_command(init)


if __name__ == "__main__":
    cli()
