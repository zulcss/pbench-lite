import click

from pbench.agent.config import AgentConfig
from pbench.agent.triggers import Trigger
from pbench.cli.commands import options
from pbench.cli.commands.base import initialize


@click.group(help="pbench triggers")
def triggers():
    """Place holder for pbench-cli subcommand"""
    pass


@click.command(help="list all tool triggers")
@options.config
@options.debug
@click.option(
    "-g", "--group", required=False, help="list the triggers use by this group"
)
def list(config, debug, group):
    initialize(AgentConfig(config))
    Trigger(config).list(group)


@click.command(help="register tool triggers for a given group")
@options.config
@options.debug
@click.option(
    "-g", "--group",
)
@click.option("--start-trigger")
@click.option("--stop-trigger")
def register(config, debug, group, start_trigger, stop_trigger):
    initialize(AgentConfig(config))
    Trigger(config).register(group, start_trigger, stop_trigger)


triggers.add_command(register)
triggers.add_command(list)
