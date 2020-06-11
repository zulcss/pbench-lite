import click

from pbench.agent.config import AgentConfig
from pbench.agent.tools.state import ToolState
from pbench.cli.commands import options
from pbench.cli.commands.base import initialize


@click.command(help="tell pbench to stop your registered tools")
@options.config
@options.debug
@click.option("--name")
@click.option("--group", default="default")
@click.option("--no-install", is_flag=True, required=False)
@click.option("--remotes")
@click.option("--labels")
@click.argument("args", required=False)
def register(config, debug, name, group, no_install, remotes, labels, args):
    c = AgentConfig(config)
    t = ToolState(c)
    initialize(c)
    t.register(name, group, no_install, remotes, labels, args)
