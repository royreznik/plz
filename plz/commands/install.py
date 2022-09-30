import sys
from pathlib import Path
from typing import Any, Dict

import click
import virtualenv
from piptools.__main__ import sync as _sync
from virtualenv.discovery.py_info import PythonInfo

VIRTUALENV_DIR_NAME = ".venv"


# TODO: allow users to pass arguments to virtualenv
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
def install(
    obj: Dict[str, Path],
    ctx: click.Context,
    production: bool,
    *args: Any,
    **kwargs: Any
) -> None:
    production = ctx.params.pop("production")

    src_files = [str(obj["path"] / "requirements.txt")]
    if not production:
        src_files.append(str(obj["path"] / "dev-requirements.txt"))

    kwargs["src_files"] = src_files

    if kwargs["python_executable"] is not None:
        ctx.forward(_sync.cli, *args, **kwargs)
        return

    venv_dir = obj["path"] / VIRTUALENV_DIR_NAME  # type: Path
    if not venv_dir.exists():
        virtualenv.cli_run([str(venv_dir)])
    kwargs["python_executable"] = (
        venv_dir
        / PythonInfo().install_path("scripts")
        / Path("python").with_suffix(".exe" if sys.platform == "win32" else "")
    )
    ctx.forward(_sync.cli, *args, **kwargs)


install.params += _sync.cli.params
