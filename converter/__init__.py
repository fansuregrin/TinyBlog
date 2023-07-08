from typing import Union

from .converter import (
    TextConverter,
    PlainTextToHtml,
    MarkdownToHtml,
    ReST2Html
)

def create_converter(kind: Union[int, str]) -> TextConverter:
    """A factory function to create specific `TextConverter`.
    :param kind: A id or a name to be specificed to create a `TextConverter`.
    :type kind: `int` or `str`
    :return: A `TextConverter` contains a method which can convert a specific fomart text to html.
    :rtype: `TextConverter`
    """
    if kind == 1 or kind == 'md2html':
        converter = MarkdownToHtml()
    elif kind == 2 or kind == 'txt2html':
        converter = PlainTextToHtml()
    elif kind == 3 or kind == 'rst2html':
        converter = ReST2Html()
    return converter