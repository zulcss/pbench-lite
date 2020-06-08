import os
import pathlib
import sys

import six

from pbench.agent.logger import logger


def initialize(config):
    """Setup the pbench environment before executing a command"""
    if six.PY2:
        logger.error("python3 is not installed")
        sys.exit(1)

    pbench_run = pathlib.Path(config.rundir)
    if pbench_run.exists():
        if os.access(pbench_run, os.W_OK) is not True:
            logger.error("%s is not writable", pbench_run)
            sys.exit(1)
        pbench_tmp = pathlib.Path(pbench_run, "tmp")
        if not pbench_tmp.exists():
            # the pbench temporary directory is always relative to pbench
            # run
            pbench_tmp.mkdir(parents=True, exist_ok=True)
    else:
        logger.error("the provided pbench run directory %s does not exist", pbench_run)
        sys.exit(1)
