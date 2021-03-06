import configparser
import errno
import pathlib
import sys

import click

from pbench.common import configtools
from pbench.common import exceptions


def lookup_agent_configuration(filename=None):
    """Return config file PATH"""
    path = pathlib.Path(filename)
    if not path.exists():
        click.secho(f"Unable to find configuration: {filename}")
        sys.exit(1)

    config_files = configtools.file_list(filename)
    config_files.reverse()

    try:
        config = configparser.ConfigParser()
        config.read(config_files)
    except configparser.Error as e:
        raise e
    except IOError as err:
        if err.errno == errno.ENOENT:
            raise exceptions.ConfigFileNotFound()
        if err.errno == errno.EACCES:
            raise exceptions.ConfigFileAccessDenied()
        raise
    return config


class AgentConfig:
    def __init__(self, cfg_name=None):
        self.cfg_name = cfg_name
        self.pbench_config = lookup_agent_configuration(self.cfg_name)
        try:
            self.agent = self.pbench_config["pbench-agent"]
        except KeyError:
            raise exceptions.BadConfig()

        try:
            self.results = self.pbench_config["results"]
        except KeyError:
            self.results = {}

        try:
            self.tools = self.pbench_config["pbench/tools"]
        except KeyError:
            self.tools = {}

    def get_agent(self):
        """Return the agent section"""
        return self.agent

    def get_results(self):
        """Return the results section"""
        return self.results

    def get_tools(self):
        return self.tools

    def toolset(self, toolset):
        return self.tools.get(f"{toolset}-tool-set", None)

    @property
    def rundir(self):
        """Return the pbench run_dir"""
        return self.agent.get("pbench_run", "/var/lib/pbench-agent")

    @property
    def installdir(self):
        """Return the pbench install-dir"""
        return self.agent.get("install-dir", "/opt/pbench-agent")

    @property
    def logdir(self):
        """Return the pbench log_dir"""
        return self.agent.get("pbench_log", None)

    @property
    def user(self):
        """Return the pbench user"""
        return self.agent.get("pbench_user", "pbench")

    @property
    def group(self):
        """Return the pbench group"""
        return self.agent.get("pbench_group", "pbench")
