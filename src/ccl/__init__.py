import logging
import pathlib
from importlib.metadata import distribution as __dist
import typing

import click

from ccl import finder

__version__ = __dist("clickloader").version
__author__ = __dist("clickloader").metadata["Author"]

_log = logging.getLogger("ccl")


def register_commands(
    group: click.Group,
    source: typing.Union[str, pathlib.Path],
) -> None:
    path = pathlib.Path(source)
    _log.debug(f"Started registering commands in {path.resolve()}")

    commands = fetch_commands_for_group(path)

    for command in commands:
        _log.info(
            f"Adding commands from group {command.name}"
            if isinstance(command, click.Group)
            else f"Adding command {command.name}"
        )
        group.add_command(command)


def fetch_commands_for_group(source: pathlib.Path) -> typing.List[typing.Union[click.Command, click.Group]]:
    """Return a list of click's commands or groups.

    Parameters
    ----------
    source : pathlib.Path
        Path to the source that should be read.
    """
    entities: typing.List[typing.Union[click.Command, click.Group]] = []

    for file in source.iterdir():
        if file.is_file():
            if file.name.startswith("__"):
                continue

            _log.debug(f"Found {file.name}")
            function_name = finder.find_cmd_func_name(file)
            command = finder.fetch_cmd_func(file, function_name, "command")

            entities.append(command)

        if file.is_dir():

            _log.debug(f"Found directory {file.resolve()}, looping inside...")

            if (file / "__init__.py").exists():
                _log.debug("Found __init__.py, trying to extract group")
                func_name = finder.find_cmd_func_name(file / "__init__.py")
                group = finder.fetch_cmd_func(file / "__init__.py", func_name, "group")
                group.name = file.name
            else:
                group = click.Group(file.name)

            if file.name.startswith("__"):
                continue

            commands = fetch_commands_for_group(file)
            for command in commands:
                group.add_command(command)

            entities.append(group)

    return entities
