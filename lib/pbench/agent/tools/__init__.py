from pathlib import Path
import sys

# constants
DEFAULT_GROUP = "default"
TOOLS_GROUP_PREFIX = "tools-v1"


def verify_rundir(rundir):
    """Verify rundir pathlib object"""
    if isinstance(rundir, str):
        rundir = Path(rundir)
    if not rundir.exists():
        sys.exit()
    return rundir


def verify_tool_group(rundir, group):
    """Verify that that the tool group directory exists"""
    rundir = verify_rundir(Path(rundir, f"{TOOLS_GROUP_PREFIX}-{group}"))
    if not rundir.exists():
        sys.exit(1)
    return rundir


def get_tools_group_list(rundir):
    """Generate a tools group list"""
    rundir = verify_rundir(rundir)
    return [
        p.name.split(f"{TOOLS_GROUP_PREFIX}-")[1] for p in rundir.glob("tools-v1-*")
    ]
