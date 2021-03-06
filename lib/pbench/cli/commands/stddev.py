import click

from pbench.agent.utils import calculate_stddev


@click.command()
@click.argument("values", nargs=-1, type=click.FLOAT)
def main(values=None):
    (avg, stddev, stddevpct, closest_index) = calculate_stddev(values)

    print("%.4f %.4f %.4f %d" % (avg, stddev, stddevpct, closest_index))
