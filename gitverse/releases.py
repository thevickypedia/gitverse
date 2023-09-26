import os
import subprocess
import time
from datetime import datetime
from typing import Dict, List, Union

import click
import dotenv
import requests

from gitverse import version as pkg_version
from gitverse.models import debugger
from gitverse.models.auth_bearer import BearerAuth
from gitverse.models.callables import options


def get_api_releases() -> Dict[str, List[str]]:
    """Get release notes via git api.

    Returns:
        Dict[str, List[str]]:
        Returns release notes in the form of release version and description as key-value pairs gathered via GitHub API.
    """
    gh_token = os.getenv('GIT_TOKEN') or os.getenv('git_token')
    session = requests.Session()
    if git_config := run_git_cmd(cmd=r"git config --get remote.origin.url | sed 's/.*\/\([^ ]*\/[^.]*\).*/\1/'",
                                 raw=True):
        owner, repo_name = git_config.split('/')
        if gh_token:
            debugger.info("Loading bearer auth with git token")
            session.auth = BearerAuth(token=gh_token)
        else:
            debugger.warning("Trying to collect release notes without github token")
        response = session.get(url=f'https://api.github.com/repos/{owner}/{repo_name}/releases')
        if response.ok:
            debugger.info("Collected release notes via GitHub API")
            try:
                return {resp['name']: resp['body'].splitlines() for resp in response.json()}
            except requests.JSONDecodeError as error:
                debugger.error(error)
        else:
            debugger.error(f"{response.status_code} - {response.text}")


def run_git_cmd(cmd: str, raw: bool = False) -> Union[str, List[str]]:
    """Run the git command.

    Args:
        Takes the command as an argument.

    Returns:
        list:
        Returns the output of the git command split by lines.
    """
    try:
        output = subprocess.check_output(cmd, shell=True).decode(encoding='UTF-8').strip()
        if raw:
            return output
        return output.splitlines()
    except (subprocess.CalledProcessError, subprocess.SubprocessError, Exception) as error:
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
            cmd='git tag --format "%(refname:short) %(creatordate:format:%s)"'
    ):
        return {line.split()[0]: int(line.split()[1]) for line in dates_values}


def get_releases() -> Union[List[Dict[str, Union[str, List[str], int, str]]], None]:
    """Get releases mapped with the timestamp.

    Returns:
        Union[List[Dict[str, Union[str, List[str], int, str]]], None]:
        Returns all the releases information as list of dictionaries.
    """
    dates = get_dates()
    tags = run_git_cmd(cmd='git tag -l -n99')
    if not dates:
        debugger.error("Failed to fetch dates information.")
        return
    if not tags:
        debugger.error("Failed to fetch tags information.")
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
        elif current_version:
            version_updates[current_version]['description'].append(tag.strip())  # adds next line to previous desc
    version_updates = list(version_updates.values())
    debugger.info(f"Git tags gathered: {len(version_updates)}")
    if len(version_updates) != len(dates):
        debugger.error("Git tag has a conflict with the number of tags and dates present.")
    # Update release notes for each version, if available via GitHub API
    if release_api := get_api_releases():
        debugger.info(f"Release notes gathered: {len(release_api)}")
        refinery = {''.join([k for k in key if k.isdigit() or k == '.']): value for key, value in release_api.items()}
        for version_update in version_updates:
            if api_description := release_api.get(version_update['version'], refinery.get(version_update['version'])):
                version_update['description'] = api_description
    if options['reverse']:
        debugger.warning('Converting snippets to reverse order')
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


def run(filename: str, title: str) -> None:
    """Handler for generator functions that writes the release notes into a file.

    Args:
        filename: Name of the file that where the release notes has to be stored.
        title: Title under which the release notes has to be stored.
    """
    run_git_cmd(cmd="git fetch origin refs/tags/*:refs/tags/* --prune")
    run_git_cmd(cmd="git pull")
    snippets = generate_snippets()
    if not snippets:
        return
    if os.path.isfile(filename):
        debugger.warning(f'WARNING: Found existing {filename!r}. Recreating now.')
        os.remove(filename)
    with open(filename, 'a') as file:
        file.write('%s\n%s\n\n' % (title, '=' * len(title)))
        for index, each_snippet in enumerate(snippets):
            file.write(f'{each_snippet}\n' if index + 1 < len(snippets) else each_snippet)
    debugger.info(f"{filename!r} was created in: {round(float(time.time() - options['start']), 2)}s")


@click.command()
@click.pass_context
@click.argument('reverse', required=False)
@click.argument('debug', required=False)
@click.option("-v", "--version", required=False, is_flag=True, help="Get version of the package")
@click.option("-f", "--filename", help="Filename where the commit notes should be stored")
@click.option("-t", "--title", help="Title under which the commit notes should be stored")
@click.option("-e", "--env", help="Filename/filepath for .env file to load the environment variables")
def main(*args, reverse: str = None, debug: str = None,
         version: str = None, filename: str = None, title: str = None, env: str = None) -> None:
    """Generate a reStructuredText/Markdown file using GitHub releases.

    Run 'gitverse-release reverse' to generate release notes in reverse order.

    Run 'gitverse-release debug' to enable debug mode.
    """
    if version:
        debugger.info(pkg_version)
        return
    options['start'] = time.time()
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
    if env is None:
        env = '.env'
    kwargs = dict(dotenv_path=env, override=True, verbose=False)
    if options['debug']:
        kwargs['verbose'] = True
    dotenv.load_dotenv(**kwargs)
    run(filename=filename, title=title)


if __name__ == '__main__':
    main()
