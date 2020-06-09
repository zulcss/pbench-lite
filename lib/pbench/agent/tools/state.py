import os
from pathlib import Path
import sys

from pbench.agent.logger import logger
from pbench.agent.tools import (
    verify_tool_group,
    verify_rundir,
    get_tools_group_list,
)


class ToolState:
    def __init__(self, config):
        self.config = config
        self.groups = get_tools_group_list(self.config.rundir)
        self.rundir = verify_rundir(self.config.rundir)

    def clear(self, tool, group, remote):
        """Remove tools that have been registered

        :param name: Tool that is registered
        :param goup: Group for the tool to be removed from
        :param remote: hostname associated with tool
        """
        result = 0
        tools_group_dir = verify_tool_group(self.rundir, group)
        if remote is None:
            # Look for all the hostnames
            remote = "*"
        if tool is None:
            # Remove all register tools
            tool = "*"

        remote_dir = Path(tools_group_dir, remote)
        tools = self._tools(tools_group_dir, tool, remote)
        for p in tools:
            if p.suffix and p.suffix == ".__noinstall__":
                try:
                    os.unlink(p)
                except Exception as ex:
                    logger.error("Failed to remove: %s", ex)
                    result = 1
            try:
                os.unlink(p)
                logger.info(
                    "Removed %s from host, %s, in tools group %s",
                    p.name,
                    remote,
                    tools_group_dir,
                )
            except Exception as ex:
                logger.error("Failed to clear tool %s: %s", p, ex)
                result = 1
        tool_files = self._tools(tools_group_dir, tool, remote)
        if "__label__" in tool_files:
            label = Path(tools_group_dir, f"{tool}/{remote}/__label__")
            try:
                os.unlink(label)
            except Exception as ex:
                logger.error(
                    "Failed to remove label for remote %s: %s",
                    Path(tools_group_dir, tool, remote),
                    ex,
                )
                result = 1
        if len(tool_files) == 0:
            try:
                os.rmdir(remote_dir)
                logger.info("All tools removed from host %s", remote)
            except Exception as ex:
                logger.error("Failed to remove remote directory %s: %s", remote_dir, ex)
                result = 1

        sys.exit(result)

    def _tools(self, tools_group_dir, tname, remote):
        return [p for p in tools_group_dir.rglob(f"{remote}/{tname}")]
