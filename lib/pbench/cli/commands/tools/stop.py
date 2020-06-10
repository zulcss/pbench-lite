import click

from pbench.agent.config import AgentConfig
from pbench.agent.tools.state import ToolState
from pbench.agent.utils import get_action
from pbench.cli.commands import options
from pbench.cli.commands.base import initialize


@click.command(help="tell pbench to stop your registered tools")
@options.config
@options.debug
@click.option(
    "-g",
    "--group",
    default="default",
    help=("a tool group used in a benchmark" "(the default group is 'default')"),
)
@click.option(
    "-d",
    "--dir",
    "benchmark_dir",
    help="a directory where the benchmark will store and process data",
    type=click.Path(exists=True),
)
def stop(config, debug, group, benchmark_dir):
    c = AgentConfig(config)
    t = ToolState(c)
    initialize(c)
    t.process(group, benchmark_dir, get_action(__name__))
