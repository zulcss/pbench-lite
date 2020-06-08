import sys

import click

from pbench.agent.logger import logger
from pbench.agent.fs import rmtree
from pbench.agent.config import AgentConfig
from pbench.cli.commands import options
from pbench.cli.commands.base import initialize


@click.command(
    help="clean up everything, including results and what tools" "have been registered"
)
@options.config
@options.debug
def cleanup(config, debug):
    c = AgentConfig(config)
    try:
        initialize(c)
        (result, errors) = rmtree(c.rundir)
        if not result:
            logger.error("\n".join(errors))
        sys.exit(result)
    except Exception as ex:
        logger.error("Failed to remove %s: %s", c.rundir, ex)
        sys.exit(1)
