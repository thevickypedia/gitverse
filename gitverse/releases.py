import os
import subprocess
import time
from collections.abc import Generator
from datetime import datetime
from typing import Dict, List, Union

import click
import dotenv
import requests

from gitverse import version as pkg_version
from gitverse.models import debugger
from gitverse.models.auth_bearer import BearerAuth
from gitverse.models.callables import md_link_pattern, options


def get_api_releases() -> Dict[str, List[str]]:
    """Get release notes via git api.

    Returns:
        Dict[str, List[str]]:
        Returns release notes in the form of release version and description as key-value pairs gathered via GitHub API.
    """
    gh_token = os.getenv('GIT_TOKEN') or os.getenv('git_token')
    session = requests.Session()
    if git_config := run_git_cmd(r"git config --get remote.origin.url | sed 's/.*\/\([^ ]*\/[^.]*\).*/\1/'"):
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


def run_git_cmd(cmd: str) -> str:
    """Run the git command.

    Args:
        Takes the command as an argument.

    Returns:
        list:
        Returns the output of the git command split by lines.
    """
    try:
        return subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL).decode(encoding='UTF-8').strip()
    except (subprocess.CalledProcessError, subprocess.SubprocessError, Exception) as error:
        if isinstance(error, subprocess.CalledProcessError):
            result = error.output.decode(encoding='UTF-8').strip()
            debugger.error(f"[{error.returncode}]: {result}")
        else:
            debugger.error(error)


def get_tags() -> Generator[Dict[str, Union[str, int, List[str]]]]:
    """Get all tags for repo and create a dictionary by iterating over each tag for it's subject.

    Yields:
        Dict[str, int]:
        Yields the release version, description, timestamp and the date for each tag.
    """
    # Alternate: git for-each-ref --sort='-creatordate' --format '%(refname:short) %(creatordate:iso8601)' refs/tags
    if dates_values := run_git_cmd('git tag --format "%(refname:short)||%(creatordate:format:%s)"'):
        dates_values = dates_values.splitlines()
        for line in dates_values:
            tag_line = line.split('||')
            tag_name = tag_line[0]
            timestamp = int(tag_line[1])
            if notes := run_git_cmd(f'git tag -l -n99 {tag_name}'):
                yield dict(
                    version=tag_name,
                    description=[v.strip() for v in notes.lstrip(tag_name).splitlines()],
                    timestamp=timestamp,
                    date=datetime.fromtimestamp(timestamp).strftime("%m/%d/%Y")
                )
            else:
                raise ValueError(f"Failed to get release notes for the tag {tag_name}")
    else:
        raise ValueError("Failed to get tags information")


def get_releases() -> Union[List[Dict[str, Union[str, List[str], int, str]]], None]:
    """Get releases mapped with the timestamp.

    Returns:
        Union[List[Dict[str, Union[str, List[str], int, str]]], None]:
        Returns all the releases information as list of dictionaries.
    """
    try:
        tags = list(get_tags())
    except ValueError as error:
        debugger.error(error.__str__())
        return
    debugger.info(f"Git tags gathered: {len(tags)}")
    # Update release notes for each version, if available via GitHub API
    if release_api := get_api_releases():
        debugger.info(f"Release notes gathered: {len(release_api)}")
        for tag in tags:
            if api_description := release_api.get(tag['version']):
                tag['description'] = api_description
            else:
                debugger.warning(f"{tag['version']} could not be found in releases")
    if options['reverse']:
        debugger.warning('Converting snippets to reverse order')
        version_updates = sorted(tags, key=lambda x: x['timestamp'], reverse=True)
    else:
        version_updates = sorted(tags, key=lambda x: x['timestamp'])
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
            if options['ext'] == '.rst':
                line3 = md_link_pattern.sub(r'`\1 <\2>`_', '\n'.join(description))
            else:
                line3 = '\n'.join(description)
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
    debugger.info(f"{filename!r} was generated in: {round(float(time.time() - options['start']), 2)}s", True)


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
        filename = 'release_notes.md'
    if title is None:
        title = 'Release Notes'
    if env is None:
        env = '.env'

    name, extension = os.path.splitext(filename.lower())
    if name and extension in ('.rst', '.md'):
        options['ext'] = extension
    else:
        debugger.info("Module generates the notes in markdown or restructured text format")
        debugger.warning(f"Using {filename!r} may render unexpected format")
    kwargs = dict(dotenv_path=env, override=True, verbose=False)
    if options['debug']:
        kwargs['verbose'] = True
    dotenv.load_dotenv(**kwargs)
    run(filename=filename, title=title)


if __name__ == '__main__':
    main()
