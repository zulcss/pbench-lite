import click

from . import clear
from . import list


@click.group(help="start/stop/kill/register pbench tools")
@click.pass_context
def tools(ctxt):
    pass


tools.add_command(clear.clear)
tools.add_command(list.list)
