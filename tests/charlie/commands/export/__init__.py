import click
import metadeco


@metadeco.metadata("__is_custom__", True)
@click.group()
def test():
    pass
