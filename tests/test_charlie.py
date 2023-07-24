import pathlib

import click
import metadeco

from ccl import register_commands


def test_charlie():
    group = click.Group("Charlie")
    register_commands(group, pathlib.Path(__file__, "..", "charlie", "commands"))

    assert len(group.commands) == 2

    group = [cmd for cmd in group.commands.values() if isinstance(cmd, click.Group)][0]

    assert metadeco.get_metadata(group, "__is_custom__")
    assert [cmd.name for cmd in group.commands.values()] == ["add", "remove"]
