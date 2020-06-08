import click

from pbench.cli.commands.tools import tool
from pbench.cli.commands import cleanup
from pbench.cli.commands import config


@click.group()
@click.option(
    "-C",
    "--config",
    help=(
        "Path to pbench agent config. if provided pbench will load "
        "this config first, and load the configuration. By default "
        "is looking for config in the _PBENCH_AGENT_CONFIG envrionment "
        "variable."
    ),
    envvar="_PBENCH_AGENT_CONFIG",
    type=click.Path(exists=True),
)
def main(config):
    pass


main.add_command(tool)
main.add_command(cleanup.cleanup)
main.add_command(config.config)
