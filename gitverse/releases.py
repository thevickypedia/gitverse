import os
import re
import subprocess
import time
from datetime import datetime
from typing import Dict, List, NoReturn, Union

import click

from gitverse import debugger
from gitverse import version as pkg_version

options = {'debug': False, 'reverse': False, 'start': 0.0}


def run_git_cmd(cmd: str) -> List[str]:
    """Run the git command.

    Args:
        Takes the command as an argument.

    Returns:
        list:
        Returns the output of the git command split by lines.
    """
    try:
        return subprocess.check_output(cmd, shell=True).decode(encoding='UTF-8').strip().splitlines()
    except (subprocess.CalledProcessError, subprocess.SubprocessError, Exception) as error:
        if options['debug']:
            if isinstance(error, subprocess.CalledProcessError):
                result = error.output.decode(encoding='UTF-8').strip()
                debugger.error(f"[{error.returncode}]: {result}")
            else:
                debugger.error(error)


def get_dates() -> Dict[str, int]:
    """Get timestamp for each release.

    Returns:
        Dict[str, int]:
        Returns the release version and the timestamp as key-value pairs.
    """
    if dates_values := run_git_cmd(
            cmd='git for-each-ref --shell --format="ref=%(refname:short) dt=%(creatordate:format:%s)" "refs/tags/*"'
    ):
        version_timestamps = {}
        for line in dates_values:
            ref, dt = re.search(r"ref='([^']+)'\s+dt='([^']+)'", line).groups()
            version_timestamps[ref] = int(dt)
        return version_timestamps


def get_releases() -> Union[List[Dict[str, Union[str, List[str], int, str]]], None]:
    """Get releases mapped with the timestamp.

    Returns:
        Union[List[Dict[str, Union[str, List[str], int, str]]], None]:
        Returns all the releases information as list of dictionaries.
    """
    dates = get_dates()
    tags = run_git_cmd(cmd='git tag -l -n99')
    if not dates:
        debugger.error("Failed to fetch dates information.") if options['debug'] else None
        return
    if not tags:
        debugger.error("Failed to fetch tags information.") if options['debug'] else None
        return
    current_version = None
    version_updates = {}
    for tag in tags:
        if tag.split()[0] in dates.keys():
            current_version = tag.split()[0]
            version_updates[current_version] = {
                    "version": current_version,
                    "description": [' '.join(tag.split()[1:])],
                    "timestamp": dates[current_version],
                    "date": datetime.fromtimestamp(dates[current_version]).strftime("%m/%d/%Y")
                }
        else:
            version_updates[current_version]['description'].append(tag.strip())  # adds next line to previous desc
    version_updates = list(version_updates.values())
    if options['reverse']:
        debugger.warning('Converting snippets to reverse order') if options['debug'] else None
        version_updates = sorted(version_updates, key=lambda x: x['timestamp'], reverse=True)
    else:
        version_updates = sorted(version_updates, key=lambda x: x['timestamp'])
    return version_updates


def generate_snippets() -> List[str]:
    """Generate snippets based on the releases information.

    Returns:
        List[str]:
        Returns a list of snippets ready to be loaded into a markdown or rst file.
    """
    if loaded := get_releases():
        snippets = []
        for each_tag in loaded:
            if each_tag['version'].startswith('v') or each_tag['version'].startswith('V'):
                each_tag['version'] = each_tag['version'].replace('v', '').replace('V', '')
            line1 = f"{each_tag['version']} ({each_tag['date']})"
            line2 = "-" * len(line1)
            description = []
            for desc in each_tag['description']:
                if desc.startswith('-'):
                    description.append(desc)
                else:
                    description.append('- ' + desc)
            line3 = "\n".join(description)
            line = line1 + "\n" + line2 + "\n" + line3 + "\n"
            snippets.append(line)
        return snippets


def run(filename: str, title: str) -> NoReturn:
    """Handler for generator functions that writes the release notes into a file.

    Args:
        filename: Name of the file that where the release notes has to be stored.
        title: Title under which the release notes has to be stored.
    """
    snippets = generate_snippets()
    if not snippets:
        return
    if os.path.isfile(filename):
        debugger.warning(f'WARNING: Found existing {filename!r}. Recreating now.') if options['debug'] else None
        os.remove(filename)
    with open(filename, 'a') as file:
        file.write('%s\n%s\n\n' % (title, '=' * len(title)))
        for index, each_snippet in enumerate(snippets):
            file.write(f'{each_snippet}\n' if index + 1 < len(snippets) else each_snippet)
    if options['debug']:
        debugger.info(f"{filename!r} was created in: {round(float(time.time() - options['start']), 2)}s")


@click.command()
@click.pass_context
@click.argument('reverse', required=False)
@click.argument('debug', required=False)
@click.option("-v", "--version", required=False, is_flag=True, help="Get version of the package")
@click.option("-f", "--filename", help="Filename where the commit notes should be stored")
@click.option("-t", "--title", help="Title under which the commit notes should be stored")
def main(*args, reverse: str = None, debug: str = None,
         version: str = None, filename: str = None, title: str = None) -> None:
    """Generate a reStructuredText/Markdown file using github releases.

    Run 'gitverse-commit reverse' to generate release notes in reverse order.

    Run 'gitverse-commit debug' to enable debug mode.
    """
    if version:
        debugger.info(pkg_version)
        return
    reverse = reverse or ''
    debug = debug or ''

    err_msg = 'The only allowed commands are:\n\t1. releasenotes\n\t2. releasenotes reverse\n\t3. releasenotes debug'
    # The following makes arguments interchangeable for convenience
    if reverse.lower() == 'reverse':
        options['reverse'] = True
    elif reverse.lower() == 'debug':
        options['debug'] = True
    elif reverse:
        debugger.error(err_msg)
        return

    if debug.lower() == 'debug':
        options['debug'] = True
    elif debug.lower() == 'reverse':
        options['reverse'] = True
    elif debug:
        debugger.error(err_msg)
        return

    if filename is None:
        filename = 'ReleaseNotes'
    if title is None:
        title = 'Release Notes'
    options['start'] = time.time()
    run(filename=filename, title=title)


if __name__ == '__main__':
    main()