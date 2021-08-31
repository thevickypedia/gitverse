from datetime import datetime
from os import path, system
from subprocess import check_output

commits = int(check_output("git rev-list --count master", shell=True).decode('utf-8').split('\n')[0])

versions = []
for n in range(1, commits + 1):
    ver = str(n)
    if len(ver) == 1:
        versions.append(f'0.0.{ver}')
    elif len(ver) == 2:
        versions.append(f'0.{ver[0]}.{ver[1]}')
    elif len(ver) == 3:
        versions.append(f'{ver[0]}.{ver[1]}.{ver[2]}')

system('git log --reverse > source_change_log.txt')

with open('source_change_log.txt', 'r') as file:
    log = file.read().splitlines()

if path.isfile('CHANGELOG'):
    system('rm CHANGELOG')
n = 0
with open('CHANGELOG', 'a') as file:
    for index, element in enumerate(log):
        element = element.strip()
        if not element.startswith('commit') and not element.startswith('Author'):
            if element.startswith('Date'):
                ind = log.index(element)
                element = ' '.join(element.lstrip('Date:').strip().split()[0:-1])
                datetime_obj = datetime.strptime(element, "%a %b %d %H:%M:%S %Y")
                element = f'{versions[n]} ({datetime_obj.strftime("%m/%d/%Y")})'
                n += 1
                log[ind + 1] = '-' * len(element)
                # log.pop(ind + 1)  # Use this leave it with a blank line instead of '----'
            elif element:
                if element[0].isdigit():
                    element = element.replace(element[0:2], '-')
                if not element[0] == '-':
                    element = f'- {element}'
            file.write(element + '\n')
