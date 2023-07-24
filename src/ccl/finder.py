import ast
import importlib.util
import logging
import pathlib
from shutil import ExecError
from typing import Literal, overload

import click

_log = logging.getLogger("ccl")


def find_cmd_func_name(path: pathlib.Path) -> str:
    """Attempt to read a file's syntax tree and find where the command is located.
    Found by reading decorator and find one that is called "click".

    Parameters
    ----------
    path : pathlib.Path
        The path of where the command is located.

    Returns
    -------
    str
        The name of the function that contains the command execution.
    """
    content = path.read_text()

    try:
        tree = ast.parse(content, path, "exec")
    except ValueError as exception:
        raise ValueError(f"Cannot read source at {path}") from exception

    for item in tree.body:
        if isinstance(item, ast.FunctionDef):
            for decorator in item.decorator_list:
                if isinstance(decorator, ast.Call):
                    if decorator.func.value.id == "click":  # type: ignore
                        return item.name
                elif decorator.value.id == "click":  # type: ignore
                    return item.name
    raise ValueError("Could not find command.")


@overload
def fetch_cmd_func(
    path: pathlib.Path, export_function_name: str, return_type: Literal["command"]
) -> click.Command:
    ...


@overload
def fetch_cmd_func(
    path: pathlib.Path, export_function_name: str, return_type: Literal["group"]
) -> click.Group:
    ...


def fetch_cmd_func(
    path: pathlib.Path, export_function_name: str, return_type: str
) -> click.Command | click.Group:
    """Load a module at path and try to export a function from its name.
    Supposedly to return a click command.

    Parameters
    ----------
    path : pathlib.Path
        Path to the module to read.
    export_function_name : str
        The function's name to export. Can be found using read_and_find_command.

    Returns
    -------
    click.Command
        The export click command function.
    """
    spec = importlib.util.spec_from_file_location(path.parent.name, path)
    if spec is None:
        # figma: noqa
        raise ExecError(f'When loading "{path.resolve()}", spec not found.')
    if spec.loader is None:
        # figma: noqa
        raise ExecError(f'When loading "{path.resolve()}", spec loader not found')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if hasattr(module, export_function_name):
        _log.debug(f"In {path.resolve()}, exporting function {export_function_name}")
        return getattr(module, export_function_name)

    raise ValueError("Could not find command.")
