import click

from pbench.cli.commands import options
from pbench.cli.commands import base


class List(base.Base):
    def execute(self):
        print("chuck")


@click.command()
@options.config
@options.debug
def list(config, debug):
    command_args = {}
    List(config, command_args).execute()
