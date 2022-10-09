import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, cast

import click
import virtualenv
from piptools.__main__ import compile as _compile
from piptools.__main__ import sync as _sync
from virtualenv.discovery.py_info import PythonInfo

REQUIREMENTS_FILE = "requirements.in"
COMPILED_REQUIREMENTS_FILE = "requirements.txt"
DEV_REQUIREMENTS_FILE = "dev-requirements.in"
COMPILED_DEV_REQUIREMENTS_FILE = "dev-requirements.txt"
VIRTUALENV_DIR_NAME = ".venv"


def _forward(
    ctx: click.Context, command: click.Command, *args: Any, **kwargs: Any
) -> Any:
    """
    This function is really important!
    ctx.forward can raise SystemExit even on a successful run, but we don't want it to stop our execution
    """
    try:
        return ctx.forward(command, *args, **kwargs)
    except SystemExit as e:
        if e.code == 0:
            return 0
        raise


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


# TODO: allow users to pass arguments to virtualenv
# noinspection PyUnusedLocal
@click.command("install")
@click.pass_context
@click.pass_obj
@click.option(
    "--production",
    "-p",
    is_flag=True,
    default=False,
    help="If True, dev requirements won't be installed",
)
@click.option(
    "--no-root",
    is_flag=True,
    default=False,
    help="If set, root package will not be installed",
)
def install(
    obj: Dict[str, Path],
    ctx: click.Context,
    production: bool,
    no_root: bool,
    *args: Any,
    **kwargs: Any,
) -> None:
    production = ctx.params.pop("production")
    no_root = ctx.params.pop("no_root")

    src_files = [str(obj["path"] / COMPILED_REQUIREMENTS_FILE)]
    if not production:
        src_files.append(str(obj["path"] / COMPILED_DEV_REQUIREMENTS_FILE))

    kwargs["src_files"] = src_files

    if kwargs["python_executable"] is not None:
        _forward(ctx, cast(click.Command, _sync.cli), *args, **kwargs)

    else:
        venv_dir = obj["path"] / VIRTUALENV_DIR_NAME  # type: Path
        if not venv_dir.exists():
            virtualenv.cli_run([str(venv_dir)])
        kwargs["python_executable"] = (
            venv_dir
            / PythonInfo().install_path("scripts")
            / Path("python").with_suffix(".exe" if sys.platform == "win32" else "")
        )
        _forward(ctx, cast(click.Command, _sync.cli), *args, **kwargs)

    if not no_root:
        result = subprocess.run(
            [
                kwargs["python_executable"],
                "-m",
                "pip",
                "install",
                "-e",
                f"{obj['path']}",
            ],
            capture_output=True,
        )
        click.echo(f"pip stdout:\n{result.stdout!r}")
        click.echo(f"pip stderr:\n{result.stderr!r}")
        if result.returncode != 0:
            raise click.BadParameter(
                f"Failed to install root\n" f"command: {result.args}\n"
            )


install.params += _sync.cli.params


@click.command("lock")
@click.pass_context
@click.pass_obj
def lock(obj: Dict[str, Path], ctx: click.Context, *args: Any, **kwargs: Any) -> None:
    kwargs["src_files"] = [
        str(obj["path"] / "requirements.in"),
    ]
    _forward(ctx, cast(click.Command, _compile.cli), *args, **kwargs)
    kwargs["src_files"] = [
        str(obj["path"] / "dev-requirements.in"),
    ]
    _forward(ctx, cast(click.Command, _compile.cli), *args, **kwargs)
    click.secho("Successfully lock requirements.")


lock.params += _compile.cli.params


# noinspection PyTypeChecker
@click.group()
@click.pass_context
@click.option(
    "-p", "--path", type=click.Path(exists=True, path_type=Path, file_okay=False)
)
def cli(ctx: click.Context, path: Path) -> None:
    path = path or Path(".")
    ctx.obj = {"path": path}


# noinspection PyTypeChecker
cli.add_command(init)
# noinspection PyTypeChecker
cli.add_command(lock)
# noinspection PyTypeChecker
cli.add_command(install)

if __name__ == "__main__":
    cli()
