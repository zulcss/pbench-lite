import click

from pbench.cli.commands import options
from pbench.cli.commands import base


@click.command()
@options.config
@options.debug
def list(config, debug):
    base.initialize(config)
