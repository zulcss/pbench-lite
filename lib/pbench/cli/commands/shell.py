import click

from pbench.cli.commands.tools import tools
from pbench.cli.commands import cleanup
from pbench.cli.commands import config
from pbench.cli.commands import results
from pbench.cli.commands import sysinfo


@click.group()
def main():
    pass


main.add_command(tools)
main.add_command(cleanup.cleanup)
main.add_command(config.config)
main.add_command(results.results)
main.add_command(sysinfo.sysinfo)
