import re

md_link_pattern = re.compile(r'\[([^\]]+)]\(([^)]+)\)')  # noqa
options = {'debug': False, 'reverse': False, 'start': 0.0, 'ext': None}
