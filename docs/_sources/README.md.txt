[![Pypi-version](https://img.shields.io/pypi/v/gitverse)](https://pypi.org/project/gitverse)
![Python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue)

[![pages-build-deployment](https://github.com/thevickypedia/gitverse/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/thevickypedia/gitverse/actions/workflows/pages/pages-build-deployment)
[![pypi-publish](https://github.com/thevickypedia/gitverse/actions/workflows/python-publish.yml/badge.svg)](https://github.com/thevickypedia/gitverse/actions/workflows/python-publish.yml)

[![Pypi-format](https://img.shields.io/pypi/format/gitverse)](https://pypi.org/project/gitverse/#files)
[![Pypi-status](https://img.shields.io/pypi/status/gitverse)](https://pypi.org/project/gitverse)

![Maintained](https://img.shields.io/maintenance/yes/2023)
[![GitHub Repo created](https://img.shields.io/date/1630367571)](https://api.github.com/repos/thevickypedia/gitverse)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/y/thevickypedia/gitverse)](https://api.github.com/repos/thevickypedia/gitverse)
[![GitHub last commit](https://img.shields.io/github/last-commit/thevickypedia/gitverse)](https://api.github.com/repos/thevickypedia/gitverse)

# GitVerse

### Installation
```shell
pip install gitverse
```

### Usage
#### Release Notes (Tags)
Generate release notes from releases tagged in GitHub
```shell
gitverse-release
```

Generate commit history from git log
#### Commit History
```shell
gitverse-commit
```

##### Options
- `debug` - Enable debug mode for logging.
- `reverse` - Generate commit history/release notes in reverse order.

##### Flags
- `-b` Gather commit notes specific to a branch. Uses `Default branch` if not passed. (Only for `gitverse-commit`)
- `-f` Write the commit notes to a custom filename.
- `-t` Title or index line for the file generated.

#### Sample
[release_notes.rst][release_notes]

[changelog.rst][changelog]

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

[https://pypi.org/project/gitverse/][pypi]

### Runbook
[![made-with-sphinx-doc](https://img.shields.io/badge/Code%20Docs-Sphinx-1f425f.svg)](https://www.sphinx-doc.org/en/master/man/sphinx-autogen.html)

[https://thevickypedia.github.io/gitverse/][runbook]

## License & copyright

&copy; Vignesh Sivanandha Rao, GitVerse

Licensed under the [MIT License][license]

[release_notes]: https://github.com/thevickypedia/gitverse/blob/main/release_notes.rst
[changelog]: https://github.com/thevickypedia/gitverse/blob/main/changelog.rst
[runbook]: https://thevickypedia.github.io/gitverse/
[license]: https://github.com/thevickypedia/gitverse/blob/master/LICENSE
[pypi]: https://pypi.org/project/gitverse/
