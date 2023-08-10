from click import secho


def debug(msg):
    """Print the incoming message in light green."""
    secho(message=msg, fg='green')


def info(msg):
    """Print the incoming message in bright green."""
    secho(message=msg, fg='bright_green')


def warning(msg):
    """Print the incoming message in bright yellow."""
    secho(message=msg, fg='bright_yellow')


def error(msg):
    """Print the incoming message in bright red."""
    secho(message=msg, fg='bright_red')
