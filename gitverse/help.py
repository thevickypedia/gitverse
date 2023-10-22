import click

import gitverse


@click.command()
@click.pass_context
@click.option("-V", "-v", "--version", required=False, is_flag=True, help="Get version of the package")
def main(*args, version: bool = False) -> None:
    """Generate a reStructuredText/Markdown file using GitHub releases or commit history.

    Run 'gitverse-release --help' to get release notes' specific information.

    Run 'gitverse-commit --help' to get commit history specific information.

    Run 'gitverse -V' or 'gitverse --v' to get the version information.
    """
    if version:
        click.secho(click.style("v" + gitverse.version, fg='green'))
