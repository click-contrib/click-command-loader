# Click Command Loader (CCL)

![Click Command Loader](.github/CCL.png)

Click Command Loader (Referred as CCL) is an additional package for [Click](https://click.palletsprojects.com/) to **load Click commands from a folder.**

As such, by having the following folder structure:

```ascii
my_project/
├─ commands/
│  ├─ create.py
│  ├─ delete.py
│  ├─ list.py
├─ __init__.py
```

The commands `create`, `delete` and `list` will be registered in your Click app!

## Installation

I'm a package that is available on [PyPi](https://pypi.org/project/clickloader)!

With Pip

```sh
pip install clickloader
```

With Poetry

```sh
poetry add clickloader
```

## Example

Let's consider you have the following commands structure:

```ascii
my_project/
├─ commands/
│  ├─ create.py
│  ├─ delete.py
│  ├─ list.py
├─ cli.py
```

Inside your `cli.py`, you should have your base logic for your CLI app.
Originally, this is where all your commands would be registered, but CCL will help you leverage the work here.

Here's is what the content of the `cli.py` would be:

```py
import click
import ccl
import pathlib


path_to_commands = pathlib.Path(__file__, "..", "commands")

my_cli = click.Group("MyCLI")
ccl.register_commands(my_cli, path_to_commands)

if __name__ == "__main__":
    my_cli()
```

And voilà! All commands inside your "commands" folder have been registered!

## Behind the scene

When registering commands, CCL will do the following:

1. List files and folder inside the given source.

2. Iterate over directory, if a file is found, go to step 3, if a folder is found, go to step 2.1

    2.1. If folder, see if a ``__init__.py`` exist, if it exist, attempt to export a function that contains a click decorator **(MUST BE A GROUP)**. If not found, create a click group, then continue to step 3 using the indicated group.

3. If file, attempt to export a function that contains a click decorator **(MUST BE A COMMAND)**, then add it to the given group.

4. Continue until all files/folder have been scanned.
