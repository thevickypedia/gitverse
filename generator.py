import os

os.system(f'git log --reverse > commits.txt')

with open('commits.txt', 'r') as file:
    log = file.read().splitlines()

for i, s in enumerate(log):
    s = s.strip()
    if not s.startswith('commit') and not s.startswith('Author'):
        if s.startswith('Date'):
            ind = log.index(s)
            log.pop(ind + 1)
        if s:
            if s[0].isdigit():
                s = s.replace(s[0:1], '-')
        print(s)
