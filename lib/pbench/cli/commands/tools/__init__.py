import click

from . import clear
from . import list
from . import start
from . import stop
from . import kill
from . import register
from . import postprocess


@click.group(help="start/stop/kill/register/clear/list pbench tools")
@click.pass_context
def tools(ctxt):
    pass


tools.add_command(clear.clear)
tools.add_command(list.list)
tools.add_command(start.start)
tools.add_command(stop.stop)
tools.add_command(kill.kill)
tools.add_command(register.register)
tools.add_command(postprocess.process)
