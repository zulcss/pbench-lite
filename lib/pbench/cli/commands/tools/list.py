import click

from pbench.agent.config import AgentConfig
from pbench.agent.tools.state import ToolState
from pbench.cli.commands import options
from pbench.cli.commands.base import initialize


@click.command(help="tell me what tools I have registered")
@options.config
@options.debug
@click.option(
    "-n",
    "--name",
    help=(
        "list the tool groups in which tool is used\n"
        "Not allowed with the --group option"
    ),
)
@click.option(
    "-g",
    "--group",
    help=("list the tools used in this group\n" "Not allowed with the --name option"),
)
@click.option("-o", "--with-options", "options", help="list the options with each tool")
def list(config, debug, name, group, options):
    c = AgentConfig(config)
    t = ToolState(c)
    initialize(c)
    t.list(name, group, options)
