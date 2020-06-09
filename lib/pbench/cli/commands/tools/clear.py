import click

from pbench.agent.config import AgentConfig
from pbench.agent.tools.state import ToolState
from pbench.cli.commands import options
from pbench.cli.commands.base import initialize


@click.command(help="clear all tools or filter by name or group")
@options.config
@options.debug
@click.option(
    "-n",
    "--name",
    help=(
        "A specific tool to be removed.\n"
        "if no tool is specificed all tools in the group are removed"
    ),
)
@click.option(
    "-g",
    "--group",
    default="default",
    help=(
        "The group from which tools should be removed\n"
        "(the default group is 'default')"
    ),
)
@click.option(
    "-r",
    "--remote",
    help=(
        "A specific rmote on which tools needs to be cleared.\n"
        "If no remote is specified, all the tools on all remotes are removed"
    ),
    required=False,
)
def clear(config, debug, name, group, remote):
    c = AgentConfig(config)
    t = ToolState(c)
    initialize(c)
    t.clear(name, group, remote)
