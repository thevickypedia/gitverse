import os
import subprocess
import time
from datetime import datetime
from typing import List, NoReturn

import click

from changemaker import debugger
from changemaker import version as pkg_version

options = {'debug': False, 'reverse': False, 'start': 0.0}


def get_branches() -> List[str]:
    """Runs ``git branch`` command to get the branches available for the repo.

    Returns:
        list:
        Returns a list of branches available.
    """
    try:
        branches = subprocess.check_output("git branch",
                                           shell=True).decode(encoding='UTF-8').replace('* ', '').strip().splitlines()
        return branches
    except (subprocess.CalledProcessError, subprocess.SubprocessError, Exception) as error:
        if options['debug']:
            if isinstance(error, subprocess.CalledProcessError):
                result = error.output.decode(encoding='UTF-8').strip()
                debugger.error(f"[{error.returncode}]: {result}")
            else:
                debugger.error(error)


def get_gitlog(branch: str) -> List[str]:
    """Runs the command ``git log`` to get the all commit messages excluding merges and in reverse order.

    Args:
        branch: Branch name.

    Returns:
        list:
        Returns the output of gitlog as a list.
    """
    try:
        return subprocess.check_output(f'git log --no-merges --reverse {branch}',
                                       shell=True).decode(encoding='UTF-8').splitlines()
    except (subprocess.CalledProcessError, subprocess.SubprocessError, Exception) as error:
        if options['debug']:
            if isinstance(error, subprocess.CalledProcessError):
                result = error.output.decode(encoding='UTF-8').strip()
                debugger.error(f"[{error.returncode}]: {result}")
            else:
                debugger.error(error)


def get_commits(trunk: str) -> int:
    """Scans for the number of commits in the ``trunk`` branch.

    Args:
        trunk: Branch name.

    Returns:
        int:
        Number of commits.
    """
    try:
        commits = int(subprocess.check_output(f"git rev-list --count {trunk}",
                                              shell=True).decode('utf-8').splitlines()[0])
        debugger.info(f'Number of commits: {commits}') if options['debug'] else None
        return commits
    except subprocess.SubprocessError as error:
        debugger.error(error) if options['debug'] else None


def generator(versions: List[str], gitlog: List[str]) -> List[str]:
    """Triggers the conversion process.

    Returns:
        list:
        List of snippets that has to be written to the output file.
    """
    iterator = 0
    output = []
    for index, element in enumerate(gitlog):
        element = element.strip()
        if element.startswith('commit') or element.startswith('Author'):
            continue
        if element.startswith('Date'):
            ind = gitlog.index(element)
            element = ' '.join(element.lstrip('Date:').strip().split()[0:-1])
            datetime_obj = datetime.strptime(element, "%a %b %d %H:%M:%S %Y")
            element = f'{versions[iterator]} ({datetime_obj.strftime("%m/%d/%Y")})'
            iterator += 1
            gitlog[ind + 1] = '-' * len(element)
            # log.pop(ind + 1)  # Use this to leave a blank line instead of '----'
        elif element:
            if element[0].isdigit():
                element = element.replace(element[0:2], '-')
            if not element[0] == '-':
                element = f'- {element}'
        if not element:
            output.append('^^')
        else:
            output.append(element + '\n')
    return [snippet for snippet in ''.join(output).split('^^')]


def run(branch: str, filename: str, title: str) -> NoReturn:
    """Handler for generator functions that writes the commit history into a file.

    Args:
        branch: Name of the branch.
        filename: Name of the file that where the commit history has to be stored.
        title: Title under which the commit history has to be stored.
    """
    branches = get_branches()
    if branch and branch not in branches:
        debugger.error(f"{branch!r} is not available.") if options['debug'] else None
        debugger.info(f"Available branches: {', '.join(branches)}") if options['debug'] else None
        return
    elif not branch:
        branch = 'main' if 'main' in branches else 'master'
    debugger.info(f'Identified trunk branch to be {branch!r}') if options['debug'] else None

    debugger.info(f'Getting commit history for branch {branch!r}') if options['debug'] else None
    commits = get_commits(trunk=branch)
    if not commits:
        return

    debugger.info(f'Getting git log for the branch {branch!r}') if options['debug'] else None
    gitlog = get_gitlog(branch=branch)
    if not gitlog:
        debugger.error('No commit message found.') if options['debug'] else None
        return

    debugger.info('Generating snippets') if options['debug'] else None
    snippets = generator(gitlog=gitlog,
                         versions=['.'.join(v for v in "{:03d}".format(n)) for n in range(1, commits + 1)])
    if not snippets:
        return

    if options['reverse']:
        debugger.warning('Converting snippets to reverse order') if options['debug'] else None
        snippets.reverse()

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
@click.option("-b", "--branch", help="The branch to read the commit notes from")
@click.option("-f", "--filename", help="Filename where the commit notes should be stored")
@click.option("-t", "--title", help="Title under which the commit notes should be stored")
def main(*args, reverse: str = None, debug: str = None, version: str = None,
         branch: str = None, filename: str = None, title: str = None) -> None:
    """Generate a reStructuredText/Markdown file using github commit notes.

    Run 'changelog reverse' to generate changelog in reverse order.

    Run 'changelog debug' to enable debug mode.
    """
    if version:
        debugger.info(pkg_version)
        return
    reverse = reverse or ''
    debug = debug or ''

    # The following makes arguments interchangeable for convenience
    if reverse.lower() == 'reverse':
        options['reverse'] = True
    elif reverse.lower() == 'debug':
        options['debug'] = True
    elif reverse:
        debugger.error('The only allowed commands are:\n\t1. changelog\n\t2. changelog reverse\n\t3. changelog debug')
        return

    if debug.lower() == 'debug':
        options['debug'] = True
    elif debug.lower() == 'reverse':
        options['reverse'] = True
    elif debug:
        debugger.error('The only allowed commands are:\n\t1. changelog\n\t2. changelog reverse\n\t3. changelog debug')
        return

    if filename is None:
        filename = 'CHANGELOG'
    if title is None:
        title = 'Change Log'
    options['start'] = time.time()
    run(branch=branch, filename=filename, title=title)


if __name__ == '__main__':
    main()
