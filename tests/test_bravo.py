import pathlib

import click

from ccl import register_commands


def test_bravo():
    group = click.Group("Bravo")
    register_commands(group, pathlib.Path(__file__, "..", "bravo", "commands"))

    assert len(group.commands) == 2

    group = [cmd for cmd in group.commands.values() if isinstance(cmd, click.Group)][0]

    assert [cmd.name for cmd in group.commands.values()] == ["add", "remove"]
