import click


def config(f):
    """Allow the user to specify the agent configuration"""
    return click.option(
        "-C",
        "--config",
        help=(
            "Path to pbench agent config. if provided pbench will load "
            "this config first, and load the configuration. By default "
            "is looking for config in the _PBENCH_AGENT_CONFIG envrionment "
            "variable."
        ),
        # Pass the _PBENCH_AGENT_CONFIG envrionment variable
        envvar="_PBENCH_AGENT_CONFIG",
        # Check to see if the file exits otherwise terminate
        type=click.Path(exists=True),
    )(f)


def debug(f):
    """Turn on/off debug messages, default is off"""
    return click.option(
        "--debug/--no-debug", default=False, help="Turn on/off debug messages"
    )(f)
