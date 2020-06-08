import click

from . import test


@click.group(help="start/stop/kill/register pbench tools")
@click.pass_context
def tool(ctxt):
    pass


tool.add_command(test.list)
