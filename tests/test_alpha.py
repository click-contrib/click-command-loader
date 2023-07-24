import pathlib

import click

from ccl import register_commands


def test_alpha():
    group = click.Group("Alpha")
    register_commands(group, pathlib.Path(__file__, "..", "alpha", "commands"))

    assert len(group.commands) == 3
    assert list(group.commands) == ["create", "delete", "list"]
