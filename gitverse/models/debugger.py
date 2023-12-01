import click

from gitverse.models.callables import options


def debug(msg, override: bool = False):
    """Print the incoming message in light green."""
    if options['debug'] or override:
        click.secho(message=msg, fg='green')


def info(msg, override: bool = False):
    """Print the incoming message in bright green."""
    if options['debug'] or override:
        click.secho(message=msg, fg='bright_green')


def warning(msg, override: bool = False):
    """Print the incoming message in bright yellow."""
    if options['debug'] or override:
        click.secho(message=msg, fg='bright_yellow')


def error(msg, override: bool = False):
    """Print the incoming message in bright red."""
    if options['debug'] or override:
        click.secho(message=msg, fg='bright_red')
