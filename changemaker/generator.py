from datetime import datetime
from os import path, remove, system
from subprocess import check_output
from time import perf_counter
from typing import List, NoReturn

from click import argument, command, pass_context, secho, option


class Generator:
    """Initiates Generator object to generate ``CHANGELOG`` from output of ``git log`` command.

    >>> Generator

    See Also:
        Pre-requisite:
            - ``git`` command should be working in CLI.
    """

    def __init__(self, branch: str):
        """Instantiates the Generator object.

        - If the branch is not passed then we check if trunk branch has ``master`` or ``main``
        - Then gets the commit information from the trunk branch.
        - Stores the output of ``git log`` to a ``source_change_log.txt`` file.
        - Removes ``CHANGELOG`` if a previous version is available.
            - Older versions are not required, since ``git log`` captures all the commits anyway.
        """
        if branch:
            self.trunk = branch
        else:
            branches = check_output("git branch", shell=True).decode('utf-8').replace('* ', '').strip().split('\n')
            self.trunk = 'main' if 'main' in branches else 'master'
        secho(message=f'Identified trunk branch to be {self.trunk}', fg='bright_green')
        self.source = 'source_change_log.txt'
        self.change = 'CHANGELOG'
        secho(message='Writing git log into a temp file.', fg='bright_green')
        system(f'git log --reverse > {self.source}')
        if path.isfile(self.change):
            secho(message='WARNING: Found existing CHANGELOG. Recreating now.', fg='bright_yellow')
            remove(self.change)

    def __del__(self):
        """Removes the source file as it is temporary and prints the run time."""
        secho(message='Removing temp file.', fg='bright_green')
        remove(self.source)
        secho(message=f'CHANGELOG was created in: {round(float(perf_counter()), 2)}s', fg='bright_green')

    def get_commits(self) -> int:
        """Scans for the number of commits in the ``trunk`` branch.

        Returns:
            int:
            Number of commits.
        """
        commits = int(check_output(f"git rev-list --count {self.trunk}", shell=True).decode('utf-8').split('\n')[0])
        secho(message=f'Number of commits: {commits}', fg='bright_green')
        return commits

    def get_source(self) -> List[str]:
        """Reads the source file and splits it by lines to return it as a list.

        Returns:
            list:
            Content of the source file: ``git log``.
        """
        with open(self.source, 'r') as file:
            log = file.read().splitlines()
        return log

    def generator(self) -> List[str]:
        """Triggers the conversion process.

        Notes:
            - Calls the ``get_source()`` method.
            - Ignores lines containing commit sha and Author information.
            - Converts git datetime into a different format.
            - Adds ``-`` in front of the lines in description for all changes.

        See Also:
            - Destructor ``__del__`` method executes upon exit which deletes the ``source_change_log.txt`` file.

        Returns:
            list:
            List of snippets that has to be written to ``CHANGELOG`` file.
        """
        versions = ['.'.join(v for v in "{:03d}".format(n)) for n in range(1, self.get_commits() + 1)]
        log = self.get_source()
        secho(message='Generating CHANGELOG', fg='bright_green')
        iterator = 0
        output = []
        for index, element in enumerate(log):
            element = element.strip()
            if element.startswith('commit') or element.startswith('Author'):
                continue
            if element.startswith('Date'):
                ind = log.index(element)
                element = ' '.join(element.lstrip('Date:').strip().split()[0:-1])
                datetime_obj = datetime.strptime(element, "%a %b %d %H:%M:%S %Y")
                element = f'{versions[iterator]} ({datetime_obj.strftime("%m/%d/%Y")})'
                iterator += 1
                log[ind + 1] = '-' * len(element)
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

    def run(self, reverse: bool = False) -> NoReturn:
        """Writes the snippets into a ``CHANGELOG`` file.

        Args:
            reverse: Takes a boolean argument whether to generate the ``CHANGELOG`` in reverse.
        """
        snippets = self.generator()
        snippets.reverse() if reverse else None
        with open(self.change, 'a') as file:
            file.write('Change Log\n==========\n\n')
            for index, each_snippet in enumerate(snippets):
                file.write(f'{each_snippet}\n' if index + 1 < len(snippets) else each_snippet)


@command()
@pass_context
@argument('reverse', required=False)
@option("-b", "--branch", help="The branch to read the commit history from")
def main(*args, reverse: str = None, branch: str = None) -> None:
    """Generate change log file.

    Run 'changelog reverse' to generate changelog in reverse order.
    """
    if reverse:
        if reverse.lower() == 'reverse':
            secho(message='Generating CHANGELOG from commit history in reverse order.', fg='bright_yellow')
            Generator(branch).run(reverse=True)
        else:
            secho(message='The only allowed options are:\n\t1. changelog\n\t2. changelog reverse\n\t3. branch to use for changelog', fg='bright_red')
    else:
        Generator(branch).run()


if __name__ == '__main__':
    main()
