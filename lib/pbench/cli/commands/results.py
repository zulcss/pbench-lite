import os
import pathlib
import shutil
import click

from pbench.agent.logger import logger
from pbench.agent.config import AgentConfig
from pbench.cli.commands import options
from pbench.cli.commands.base import initialize


@click.group(help="benchmark results")
def results():
    """Place holder for pbench-cli subcommand"""
    pass


@click.command(help="delete all benchmark results")
@options.config
@options.debug
def clear(config, debug):
    c = AgentConfig(config)
    initialize(c)
    rundir = pathlib.Path(c.rundir)

    if rundir.exists():
        for path in rundir.glob("*"):
            if not (
                path.name.startswith("tmp")
                or path.name.startswith("tools")
                or path.name == "pbench.log"
            ):
                if path.is_file():
                    try:
                        os.unlink(path)
                    except Exception as ex:
                        logger.error("Failed to remove %s: %s", path, ex)
                if path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except Exception as ex:
                        logger.error("Failed to remove %s: %s", path, ex)


results.add_command(clear)
