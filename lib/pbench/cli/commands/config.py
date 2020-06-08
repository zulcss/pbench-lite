import pathlib
import shutil
import sys

import click

from pbench.agent.logger import logger
from pbench.agent.config import AgentConfig
from pbench.cli.commands import options
from pbench.cli.commands.base import initialize


@click.group(help="agent administrative commands")
def config():
    """Place holder for pbench-cli subcommand"""
    pass


@click.command(help="copy the configuration file to the destination")
@options.debug
# don't use the agent default here because the configuration should
# exist at this point
@click.argument("config", type=click.Path(exists=True))
def activate(debug, config):
    c = AgentConfig(config)
    initialize(c)
    src = pathlib.Path(config)
    dest = pathlib.Path(c.installdir, "config", "pbench-agent.cfg")

    if not dest.exists():
        try:
            shutil.copyfile(src, dest)
        except Exception as ex:
            logger.error("Failed to copy %s: %s", src, ex)
            sys.exit(1)


@click.command(help="copy ssh key file")
@options.debug
@click.argument("config", type=click.Path(exists=True))
@click.argument("keyfile", type=click.Path(exists=True))
def ssh(debug, config, keyfile):
    c = AgentConfig(config)
    initialize(c)
    src = pathlib.Path(keyfile)
    dest = pathlib.Path(c.installdir, "id_rsa")

    if not dest.exists():
        try:
            shutil.copyfile(src, dest)
        except Exception as ex:
            logger.error("Failed to copy ssh key file %s: %s", src, ex)
            sys.exit(1)


config.add_command(ssh)
config.add_command(activate)
