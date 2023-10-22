Release Notes
=============

2.7.1 (10/22/2023)
------------------
- Include version number option for bare ``gitverse`` command

2.7 (09/25/2023)
----------------
- Includes a bug fix to honor deleted tags in ``gitverse-release``

2.6b (09/25/2023)
-----------------
- Implement a bug fix on honoring deleted tags
- Release beta version

2.6a (09/25/2023)
-----------------
- Get releases to honor deleted tags
- Remove MANIFEST.in
- Add dependencies to requirements.txt
- Release alpha version
- Restructure all dependent .py models

v2.5 (08/30/2023)
-----------------
- Restructure version naming in output files
- Includes some minor modifications in type hinting

v2.4 (08/19/2023)
-----------------
- Improved security for API authentication
- Includes minor simplifications

v2.3 (08/18/2023)
-----------------
- Improved accuracy on release notes mapping from git

v2.2 (08/15/2023)
-----------------
- Add a new command for generic help

v2.1 (08/10/2023)
-----------------
- Performance improvements and more clear logging

v2.0 (08/10/2023)
-----------------
- Release v2.0

v2.0b (08/10/2023)
------------------
- Use ``python-dotenv`` to load env vars for ``git_token``
- Add CLI option to pass filename/filepath for dot env

v2.0a (08/10/2023)
------------------
- Use ``git pull`` before any operation
- Make an API call to github to get accurate release information (if available)
- Improve accuracy

v0.7 (07/30/2023)
-----------------
- Add ``version`` argument
- Set module to stable

v0.7b (07/30/2023)
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

0.2.2 (10/14/2021)
------------------
- Make Change Log the title as a heading

0.2.1 (10/14/2021)
------------------
- Add title to the generated CHANGELOG

0.2.0 (08/31/2021)
------------------
- Remove timestamp from CHANGELOG

0.1.8 (08/31/2021)
------------------
- Update CHANGELOG

0.1.7 (08/31/2021)
------------------
- bump version to run build

0.1.5 (08/31/2021)
------------------
- Alter time counter in destructor method
- Update README.md, .gitignore, CHANGELOG
- Bump version

0.1.4 (08/31/2021)
------------------
- Clean up the CHANGELOG after creation
- Update README.md, .gitignore, CHANGELOG
- Bump version

0.1.6 (08/31/2021)
------------------
- Update CHANGELOG

0.0.1 (08/31/2021)
------------------
- Update CHANGELOG
