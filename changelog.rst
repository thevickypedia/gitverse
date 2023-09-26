Commit History
==============

0.4.6 (09/25/2023)
------------------
- Get releases to honor deleted tags
- Remove MANIFEST.in
- Add dependencies to requirements.txt
- Release alpha version
- Restructure all dependent .py models

0.4.5 (08/30/2023)
------------------
- Set return type to None from NoReturn
- Upgrade to latest flake8 and isort
- Bump version

0.4.4 (08/19/2023)
------------------
- Add ``BearerAuth`` object to authenticate request
- Simply extracting version numbers

0.4.3 (08/18/2023)
------------------
- Extract version numbers explicitly
- Match tags with releases based on numbers
- Update docs

0.4.2 (08/15/2023)
------------------
- Add a new command for generic help

0.4.1 (08/10/2023)
------------------
- Reuse options via callables.py
- Reduce the usage of conditional debug
- Add more debug statements
- Update docs and bump version

0.4.0 (08/10/2023)
------------------
- Release v2.0

0.3.9 (08/10/2023)
------------------
- Add python dotenv to load env vars

0.3.8 (08/10/2023)
------------------
- Get it to a better state

0.3.7 (08/10/2023)
------------------
- Generate release notes based on version tags
- Bump to beta version

0.3.6 (08/09/2023)
------------------
- Update more references

0.3.5 (08/09/2023)
------------------
- Add an option to generate release notes
- Rename project and update references
- Update README.md and add changelog.rst

0.3.4 (07/30/2023)
------------------
- Add ``version`` argument
- Set module to stable

0.3.3 (07/30/2023)
------------------
- Convert to ``pyproject.toml``
- Update type hint, logging, and runtime

0.3.2 (12/18/2022)
------------------
- Update setup.py to include utils package

0.3.1 (12/17/2022)
------------------
- Make title underline consistent across any title
- Add an optional utils package to convert rst to html/dict

0.3.0 (12/17/2022)
------------------
- Add detailed log when git commands fail in debug mode
- Set github actions to build on release tag
- Update README.md and add more classifiers on pypi

0.2.9 (12/14/2022)
------------------
- Update runbook and README.md
- Add a check to block commit if release_notes.txt isn't updated
- Suppress flake8 ``SFS101 String literal formatting using percent operator``

0.2.8 (12/14/2022)
------------------
- Add optional title flag to for the file generated
- Add more generic notes in docstrings
- Remove CHANGELOG

0.2.7 (11/10/2022)
------------------
- Add optional branch name to pull branch specific commits
- Add exception handlers and print messages appropriately
- Enable debug mode by command
- Restructure code and cleanup
- Enable pypi workflow on commit

0.2.6 (07/31/2022)
------------------
- Optimize versions number generation with list comprehension
- Support version numbers of any extent
- Update type hint

0.2.5 (10/23/2021)
------------------
- Add an option to generate `CHANGELOG` in reverse order
- Scrap logger and use secho with colors instead
- Abort if version is not bumped
- Generate CHANGELOG in reverse

0.2.4 (10/14/2021)
------------------
- Add project urls to pypi package

0.2.3 (10/14/2021)
------------------
- Use click to make the changelog-generator to make it as a CLI tool
- Update docstrings and README.md

0.2.2 (10/14/2021)
------------------
- Make Change Log the title as a heading

0.2.1 (10/14/2021)
------------------
- Add title to the generated CHANGELOG

0.2.0 (08/31/2021)
------------------
- Remove timestamp from CHANGELOG

0.1.9 (08/31/2021)
------------------
- Update CHANGELOG

0.1.8 (08/31/2021)
------------------
- Support up to 6 digit version numbers
- Fix versions() getting called repeatedly
- Add logger info

0.1.7 (08/31/2021)
------------------
- bump version to run build

0.1.6 (08/31/2021)
------------------
- Update sample code in README.md
- Bump version to 0.1.6

0.1.5 (08/31/2021)
------------------
- Alter time counter in destructor method
- Update README.md, .gitignore, CHANGELOG
- Bump version

0.1.4 (08/31/2021)
------------------
- auto upload to pypi when tagged a release version

0.1.3 (08/31/2021)
------------------
- revert change on python-publish.yml

0.1.2 (08/30/2021)
------------------
- Create a pypi package
- Move generator.py within a source directory
- Add __init__.py, CHANGELOT, LICENSE, MANIFEST.in, setup.cfg, setup.py, version.py

0.1.1 (08/30/2021)
------------------
- auto upload to pypi when tagged a release version

0.1.0 (08/30/2021)
------------------
- onboard docs.yml but only prints a statement

0.0.9 (08/30/2021)
------------------
- Add sphinx documentation
- README markdown and __init__ support for sphinx documentation
- Create gen_docs.sh
- Hook up the doc generation process to pre-commit

0.0.8 (08/30/2021)
------------------
- Add pre-commit for linting, isort and flake8

0.0.7 (08/30/2021)
------------------
- Get the commit info from the trunk branch
- Add a destructor method
- Add docstrings

0.0.6 (08/30/2021)
------------------
- Wrap everything inside a class
- Print run time at the end

0.0.5 (08/30/2021)
------------------
- Get the number of commits automatically
- Add three digit version numbers

0.0.4 (08/30/2021)
------------------
- Add version numbers for each change
- Rename variable names

0.0.3 (08/30/2021)
------------------
- Get content required for a CHANGELOG

0.0.2 (08/30/2021)
------------------
- Add basic way to get details from `git log`

0.0.1 (08/30/2021)
------------------
- Initial commit
