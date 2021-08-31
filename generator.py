from datetime import datetime
from os import path, system, remove
from subprocess import check_output
from time import perf_counter


class Generator:
    def __init__(self):
        self.source = 'source_change_log.txt'
        self.change = 'CHANGELOG'
        system(f'git log --reverse > {self.source}')
        if path.isfile(self.change):
            remove(self.change)

    @staticmethod
    def get_commits():
        return int(check_output(f"git rev-list --count master", shell=True).decode('utf-8').split('\n')[0])

    # noinspection PyTypeChecker
    def versions(self) -> list:
        version_info = []
        for n in range(1, self.get_commits + 1):
            version = str(n)
            if len(version) == 1:
                version_info.append(f'0.0.{version}')
            elif len(version) == 2:
                version_info.append(f'0.{version[0]}.{version[1]}')
            elif len(version) == 3:
                version_info.append(f'{version[0]}.{version[1]}.{version[2]}')
        return version_info

    def run(self) -> None:
        with open(self.source, 'r') as file:
            log = file.read().splitlines()
        iterator = 0
        with open(self.change, 'a') as file:
            for index, element in enumerate(log):
                element = element.strip()
                if not element.startswith('commit') and not element.startswith('Author'):
                    if element.startswith('Date'):
                        ind = log.index(element)
                        element = ' '.join(element.lstrip('Date:').strip().split()[0:-1])
                        datetime_obj = datetime.strptime(element, "%a %b %d %H:%M:%S %Y")
                        element = f'{self.versions()[iterator]} ({datetime_obj.strftime("%m/%d/%Y - %H:%M:%S")})'
                        iterator += 1
                        log[ind + 1] = '-' * len(element)
                        # log.pop(ind + 1)  # Use this to leave a blank line instead of '----'
                    elif element:
                        if element[0].isdigit():
                            element = element.replace(element[0:2], '-')
                        if not element[0] == '-':
                            element = f'- {element}'
                    file.write(element + '\n')
        remove(self.source)
        print(f'Run Time: {round(float(perf_counter()), 2)}s')


if __name__ == '__main__':
    Generator().run()
