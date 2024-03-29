import json
import os
import tempfile
from typing import Dict, Iterable, OrderedDict, Union

try:
    import docutils.core
except ImportError:
    raise ImportError(
        "This is an additional package. Please install requirements using 'python3 -m pip install docutils>=0.17.1'"
    )

try:
    import xmltodict
except ImportError:
    raise ImportError(
        "This is an additional package. Please install requirements using 'python3 -m pip install xmltodict>=0.13.0'"
    )


def rst2html(src: Union[os.PathLike, str], dst: Union[os.PathLike, str]) -> bool:
    """Converts RST files to HTML.

    Args:
        src: Source filename or filepath.
        dst: Destination filename or filepath.

    Returns:
        bool:
        A boolean flag if conversion was successful.
    """
    if dst.split('.')[-1] not in ('html', 'htm', 'html5'):
        dst += '.html'
    docutils.core.publish_file(
        source_path=src,
        destination_path=dst,
        writer_name="html"
    )
    if os.path.isfile(dst):
        return True


def rst2dict(filename: Union[os.PathLike, str], regular_dict: bool = False) -> Union[OrderedDict, Dict]:
    """Converts RST file to a python dictionary.

    Args:
        filename: Source filename or filepath.
        regular_dict: Boolean flag to return as regular dict. Defaults to ``OrderedDict``

    Returns:
        Union[OrderedDict, Dict]:
        Output as regular dict or ordered dict based on arg passed.
    """
    temp_file = f"{tempfile.NamedTemporaryFile(dir=tempfile.gettempdir(), delete=False).name}.xml"
    docutils.core.publish_file(
        source_path=filename,
        destination_path=temp_file,
        writer_name="xml"
    )
    with open(temp_file) as file:
        dict_ = xmltodict.parse(xml_input=file.read())
    os.remove(temp_file)
    if regular_dict:
        return json.loads(json.dumps(dict_))  # OrderedDict to regular dict
    else:
        return dict_


def get_release_notes(filename: Union[os.PathLike, str], version: str = None) -> Iterable[str]:
    """Get release notes from an RST file. Tested for files generated by this module.

    Args:
        filename: Name of the source file.
        version: Version number to get release notes of a particular version.

    Returns:
        Iterable:
        Returns an iterable string.
    """
    converted = rst2dict(filename=filename, regular_dict=True)
    for section in converted['document']['section']:
        if version and not section['title'].startswith(version):
            continue
        bulletins = section['bullet_list']['list_item']
        if isinstance(bulletins, dict):
            yield bulletins['paragraph']
        elif isinstance(bulletins, list):
            for item in bulletins:
                yield item['paragraph']
