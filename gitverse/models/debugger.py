import click

from gitverse.models.callables import options


def debug(msg):
    """Print the incoming message in light green."""
    if options['debug']:
        click.secho(message=msg, fg='green')


def info(msg):
    """Print the incoming message in bright green."""
    if options['debug']:
        click.secho(message=msg, fg='bright_green')


def warning(msg):
    """Print the incoming message in bright yellow."""
    if options['debug']:
        click.secho(message=msg, fg='bright_yellow')


def error(msg):
    """Print the incoming message in bright red."""
    if options['debug']:
        click.secho(message=msg, fg='bright_red')
