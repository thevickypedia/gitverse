import os
from datetime import datetime

os.system(f'git log --reverse > commits.txt')

with open('commits.txt', 'r') as file:
    log = file.read().splitlines()

for index, s in enumerate(log):
    s = s.strip()
    if not s.startswith('commit') and not s.startswith('Author'):
        if s.startswith('Date'):
            ind = log.index(s)
            # log.pop(ind + 1)
            s = ' '.join(s.lstrip('Date:').strip().split()[0:-1])
            datetime_obj = datetime.strptime(s, "%a %b %d %H:%M:%S %Y")
            s = datetime_obj.strftime("%m/%d/%Y")
            log[ind + 1] = '-' * len(s)
        elif s:
            if s[0].isdigit():
                s = s.replace(s[0:2], '-')
            if not s[0] == '-':
                s = f'- {s}'
        print(s)
