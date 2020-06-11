import os
from pathlib import Path
import socket
import sys

import sh

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
        self.toolsdir = Path(self.config.installdir, "tool-scripts")
        if not self.toolsdir.exists():
            self.toolsdir = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "../../../agent/tool-scripts",
            )

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

    def list(self, tool, group, options):
        """
        List all tools from all groups,
        list tools from a specific group, or
        list which groups contain a specific tool
        :param tool: the registered tool name
        :param group: the group that the tool belongs too
        """
        if tool is not None and group is not None:
            logger.error("You cannnot specifiy both --group and --name")
            sys.exit(1)

        if tool is None and group is None:
            for p in Path(self.config.rundir).glob("tools-v1-*/*"):
                # ignore empty directories
                if p.is_dir():
                    if next(os.scandir(p), False) is not False:
                        print(
                            "%s:" % str(p.parent).split("tools-v1-")[1],
                            p.name,
                            "[%s]" % ", ".join([x.name for x in Path(p).glob("*")]),
                        )
        elif tool:
            groups = []
            for p in Path(self.config.rundir).rglob(f"tools-v1-*/*/{tool}"):
                group = str(p.parent.parent).split("tools-v1-")[1]
                if group not in groups:
                    groups.append(group)
            if len(groups) != 0:
                print("tool name: %s, groups: %s" % (tool, " ".join(groups)))
        elif group:
            for p in Path(self.config.rundir).glob(f"tools-v1-{group}/*"):
                print(group, p.name, [x.name for x in Path(p).glob("*")])

    def process(self, group, benchmark_dir, action):
        """
        """
        if group is None:
            logger.error("ERROR: required tool group paramanter missing")
            sys.exit(1)

        if benchmark_dir is None:
            logger.error("ERROR: required directory argument missing")
            sys.exit(1)

        rundir = verify_tool_group(group)
        if not rundir:
            sys.exit(1)

        if action == "kill":
            logger.error(
                "kill-tools is a no-op and has been deprecated: "
                "pbench-stop-tools ensure tools are properly cleaned "
                "up."
            )
            sys.exit(1)
        sh.Command("pbench-tool-meister-client", group, benchmark_dir, action)()

    def register(self, name, group, no_install, remotes, labels, args):
        if not name:
            logger.error("Missing required paramenter --name")
            sys.exit(1)
        tool = Path(self.toolsdir, name)
        if not tool.exists():
            logger.error(
                "Could not find %s in %s: has this tool been "
                "integrated into pbench-agent?",
                name,
                self.toolsdir,
            )
            sys.exit(1)

        if remotes:
            if "@" in remotes:
                # We are delaing with a file container the list of remotes
                remotes_file = Path(remotes.split("@")[1])
                if not remotes_file.exists():
                    logger.error(
                        "--remotes=@%s specifies a file that doesnt " "exist",
                        remotes_file,
                    )
                    sys.exit(1)
                remote = remotes_file.read_text().splitlines()
            else:
                remote = remotes.split(",")
        else:
            remote = [(socket.gethostname())]

        tg_dir = verify_tool_group(self.rundir, group)
        tg_dir.mkdir(parents=True, exist_ok=True)

        for r in remote:
            tg_r_dir = Path(tg_dir, r)
            tg_r_dir.mkdir(parents=True, exist_ok=True)

            tool_file = Path(tg_r_dir, name)
            if tool_file.exists():
                tool_file.unlink()
            tool_file.touch()

            if args:
                tool_file.write_text(args)

            install_file = Path(tool_file, f"{name}.__noinstall__")
            if no_install:
                if not install_file.exists():
                    tool_file.symlink_to(install_file)
            else:
                if install_file.exists():
                    install_file.unlink()
        logger.info(
            "%s is not registered for host(s) %s in %s", name, ",".join(remote), group
        )
