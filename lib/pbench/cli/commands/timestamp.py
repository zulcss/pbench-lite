import time

import click


@click.command()
def main():
    stdin = click.get_text_stream("stdin")
    s = stdin.readline().strip()
    print("%s: %s" % (time.time(), s))
