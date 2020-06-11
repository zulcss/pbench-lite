import sys

import click

from pbench.agent.config import AgentConfig
from pbench.agent.sysinfo import Sysinfo
from pbench.cli.commands import options
from pbench.cli.commands.base import initialize


@click.group(help="collect host system information")
def sysinfo():
    """Place holder for pbench-cli subcommand"""
    pass


@click.command(help="collect benchmark results")
@options.config
@options.debug
@click.option(
    "-d",
    "--dir",
    "sysinfo_dir",
    type=click.Path(exists=True),
    help="A directory that will store and process data",
)
@click.option(
    "-g",
    "--group",
    default="default",
    help="A tool group used in a benchmark (default group is 'default')",
)
@click.option(
    "--sysinfo", help="a comma seperated values of system information to be collected"
)
@click.option(
    "--check",
    help="checks if sysinfo is set to one of the accepted values",
    is_flag=True,
)
@click.option("--option", required=False, is_flag=True)
@click.argument("args")
def collect(config, debug, sysinfo_dir, group, sysinfo, check, option, args):
    initialize(AgentConfig(config))

    s = Sysinfo(config, group, sysinfo_dir, sysinfo)
    if check:
        s.check()
        sys.exit(1)
    if option:
        s.show_options()
        sys.exit(0)

    s.collect()


sysinfo.add_command(collect)
