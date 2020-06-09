import click

from . import clear


@click.group(help="start/stop/kill/register pbench tools")
@click.pass_context
def tools(ctxt):
    pass


tools.add_command(clear.clear)
