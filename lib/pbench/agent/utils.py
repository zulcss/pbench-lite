import os
import sys
import pathlib

import six

from pbench.agent.logger import logger

tools_group_prefix = "tools-v1"


def init_wrapper(config):
    if six.PY2:
        logger.error("python3 is not installed")

    pbench_run = pathlib.Path(config.rundir)
    if pbench_run.exists():
        if os.access(pbench_run, os.W_OK) is not True:
            logger.error("%s is not writable", pbench_run)
            sys.exit(1)
        pbench_tmp = pathlib.Path(pbench_run, "tmp")
        if not pbench_run.exists():
            # the pbench temporary directory is always relative to pbench run
            pbench_tmp.mkdir(parents=True, exists_ok=True)
    else:
        logger.error("the provided pbench run directory %s does not exist.", pbench_run)
        sys.exit(1)
    pbench_install_dir = pathlib.Path(config.installdir)
    if not pbench_install_dir.exists():
        logger.error(
            "pbench installation directory %s does not exist", pbench_install_dir
        )
        sys.exit(1)
    print(pbench_install_dir)


def gen_tools_group_list(pbench_run):
    if isinstance(pbench_run, str):
        pbench_run = pathlib.Path(pbench_run)
    pbench_run = pathlib.Path(pbench_run)
    if not pbench_run.exists():
        logger.error("pbench run directory %s does not exist", pbench_run)
        sys.exit(1)
    print(pbench_run)


def get_action(cmd):
    return cmd.split(".")[-1]
