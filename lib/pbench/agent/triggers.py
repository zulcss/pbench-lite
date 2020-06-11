from pathlib import Path
import sys

from pbench.agent.logger import logger
from pbench.agent.config import AgentConfig
from pbench.agent.tools import verify_tool_group, get_tools_group_list


class Trigger:
    def __init__(self, config):
        self.config = AgentConfig(config)
        self.rundir = Path(self.config.rundir)

    def list(self, group):
        if not self.rundir.exists():
            # Silently exit if we don't have a pbench run directory
            sys.exit(0)

        if group:
            if group in get_tools_group_list(self.rundir):
                tg_dir = Path(verify_tool_group(self.rundir, group), "__trigger__")
                if tg_dir.exist():
                    print(tg_dir.read_text())
        else:
            groups = get_tools_group_list(self.rundir)
            for group in groups:
                tg_dir = Path(verify_tool_group(self.rundir, group), "__trigger__")
                if tg_dir.exists():
                    print("%s: %s" % group, tg_dir.read_text())

    def register(self, group, start, stop):
        if not group:
            logger.error("A look group is required")
            sys.exit(1)

        if start is None or stop is None:
            logger.error("both --start-trigger and --stop-trigger is required")
            sys.exit(1)
        if ":" in start:
            logger.error("the start trigger cannot have a colon in it: %s", start)
            sys.exit(1)
        if ":" in stop:
            logger.error("the stop trigger cannot have a colon in it: %s", stop)
            sys.exit(1)

        tg_dir = Path(verify_tool_group(self.rundir, group), "__trigger__")
        tg_dir.write_text("%s: %s\n", start, stop)
        logger.info(
            "tool trigger strings for start: %s and for stop: %s are"
            "are not registered for tool group: %s",
            start,
            stop,
            group,
        )
