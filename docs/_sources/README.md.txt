[![Pypi-version](https://img.shields.io/pypi/v/changelog-generator)](https://pypi.org/project/changelog-generator)
![Python](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue)

[![pages-build-deployment](https://github.com/thevickypedia/changelog-generator/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/thevickypedia/changelog-generator/actions/workflows/pages/pages-build-deployment)
[![pypi](https://github.com/thevickypedia/changelog-generator/actions/workflows/python-publish.yml/badge.svg)](https://github.com/thevickypedia/changelog-generator/actions/workflows/python-publish.yml)

[![Pypi-format](https://img.shields.io/pypi/format/changelog-generator)](https://pypi.org/project/changelog-generator/#files)
[![Pypi-status](https://img.shields.io/pypi/status/changelog-generator)](https://pypi.org/project/changelog-generator)

![Maintained](https://img.shields.io/maintenance/yes/2022)
[![GitHub Repo created](https://img.shields.io/date/1630367571)](https://api.github.com/repos/thevickypedia/changelog-generator)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/y/thevickypedia/changelog-generator)](https://api.github.com/repos/thevickypedia/changelog-generator)
[![GitHub last commit](https://img.shields.io/github/last-commit/thevickypedia/changelog-generator)](https://api.github.com/repos/thevickypedia/changelog-generator)

# CHANGELOG generator
Generate CHANGELOG from git commit history

### Pypi Module
[https://pypi.org/project/changelog-generator/](https://pypi.org/project/changelog-generator/)

### Usage
###### Navigate to the repository and run:
```shell
pip install changelog-generator
```

###### Regular CHANGELOG
```shell
changelog
```

###### Regular CHANGELOG in debug mode
```shell
changelog debug
```

###### CHANGELOG in reverse order
```shell
changelog reverse
```

###### Use a branch other than `master` or `main`
```shell
changelog -b <branch name>
```

### Pre-Commit
Install `pre-commit` to run `flake8` and `isort` for linting and `sphinx` for documentation generator.

`pip install --no-cache --upgrade sphinx pre-commit recommonmark`

`pre-commit run --all-files`

### Runbook
[GitHub Docs](https://thevickypedia.github.io/changelog-generator/)

## License & copyright

&copy; Vignesh Sivanandha Rao, Changelog Generator

Licensed under the [MIT License](https://github.com/thevickypedia/changelog-generator/blob/master/LICENSE)
