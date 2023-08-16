import click


@click.command()
def main(*args) -> None:
    """Generate a reStructuredText/Markdown file using GitHub releases or commit history.

    Run 'gitverse-release --help' to get release notes' specific information.

    Run 'gitverse-commit --help' to get commit history specific information.
    """
