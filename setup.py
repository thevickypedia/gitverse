from os import path

from setuptools import setup

from version import version_info

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: MacOS :: MacOS X',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.9',
    'Topic :: Software Development :: Version Control :: Git',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'Operating System :: Microsoft :: Windows :: Windows 11',
    'Topic :: Documentation :: Sphinx'
]


def read(name: str) -> str:
    """https://pythonhosted.org/an_example_pypi_project/setuptools.html#setting-up-setup-py - reference."""
    with open(path.join(path.dirname(__file__), name)) as file:
        content = file.read()
    return content


setup(
    name='changelog-generator',
    version='.'.join(str(c) for c in version_info),
    description='Python module to, generate well formatted commit notes from git commit history.',
    long_description=read('README.md'),
    url='https://github.com/thevickypedia/changelog-generator',
    author='Vignesh Sivanandha Rao',
    author_email='svignesh1793@gmail.com',
    License='MIT',
    classifiers=classifiers,
    keywords='changelog, commits, automate',
    packages=['.changemaker'],
    install_requires=['click'],
    include_package_data=True,
    python_requires=">=3.7",
    entry_points={
            'console_scripts': [
                'changelog = changemaker.generator:main'
            ]
    },
    project_urls={
        'Source': 'https://github.com/thevickypedia/changelog-generator',
        'Docs': 'https://thevickypedia.github.io/changelog-generator',
        'Release Notes': 'https://github.com/thevickypedia/changelog-generator/blob/main/release_notes.rst',
        'Tracker': 'https://github.com/thevickypedia/changelog-generator/issues'
    }
)
