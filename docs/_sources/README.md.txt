[![Pypi-version](https://img.shields.io/pypi/v/changelog-generator)](https://pypi.org/project/changelog-generator)
![Python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue)

[![pages-build-deployment](https://github.com/thevickypedia/changelog-generator/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/thevickypedia/changelog-generator/actions/workflows/pages/pages-build-deployment)
[![pypi](https://github.com/thevickypedia/changelog-generator/actions/workflows/python-publish.yml/badge.svg)](https://github.com/thevickypedia/changelog-generator/actions/workflows/python-publish.yml)

[![Pypi-format](https://img.shields.io/pypi/format/changelog-generator)](https://pypi.org/project/changelog-generator/#files)
[![Pypi-status](https://img.shields.io/pypi/status/changelog-generator)](https://pypi.org/project/changelog-generator)

![Maintained](https://img.shields.io/maintenance/yes/2023)
[![GitHub Repo created](https://img.shields.io/date/1630367571)](https://api.github.com/repos/thevickypedia/changelog-generator)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/y/thevickypedia/changelog-generator)](https://api.github.com/repos/thevickypedia/changelog-generator)
[![GitHub last commit](https://img.shields.io/github/last-commit/thevickypedia/changelog-generator)](https://api.github.com/repos/thevickypedia/changelog-generator)

# CHANGELOG generator
Generate CHANGELOG from git commit history

### Installation
```shell
pip install changelog-generator
```

### Usage
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

###### Flags
- `-b` Gather commit notes specific to a branch. Uses `Default branch` if not passed
- `-f` Write the commit notes to a custom filename. Defaults to `CHANGELOG`
- `-t` Title or index line for the file generated. Defaults to `Change Log`

#### Sample
[release_notes.rst][release_notes]

### Linting
`PreCommit` will ensure linting, and the doc creation are run on every commit.

**Requirement**
```shell
pip install sphinx==5.1.1 pre-commit==2.20.0 recommonmark==0.7.1
```

**Usage**
```shell
pre-commit run --all-files
```

## Pypi Package
[![pypi-module](https://img.shields.io/badge/Software%20Repository-pypi-1f425f.svg)](https://packaging.python.org/tutorials/packaging-projects/)

[https://pypi.org/project/changelog-generator/][pypi]

### Runbook
[![made-with-sphinx-doc](https://img.shields.io/badge/Code%20Docs-Sphinx-1f425f.svg)](https://www.sphinx-doc.org/en/master/man/sphinx-autogen.html)

[https://thevickypedia.github.io/changelog-generator/][runbook]

## License & copyright

&copy; Vignesh Sivanandha Rao, Changelog Generator

Licensed under the [MIT License][license]

[release_notes]: https://github.com/thevickypedia/changelog-generator/blob/main/release_notes.rst
[runbook]: https://thevickypedia.github.io/changelog-generator/
[license]: https://github.com/thevickypedia/changelog-generator/blob/master/LICENSE
[pypi]: https://pypi.org/project/changelog-generator/
