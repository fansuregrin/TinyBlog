import re
from abc import ABC, abstractmethod
from marko import Markdown

from .plain_text_ import PlainText
from .rest import ReST


class TextConverter(ABC):
    @abstractmethod
    def convert_to_html(self, text: str) -> str:
        """Convert a paragraph of text to html format.
        :param text: A paragraph of text written in a format other than html.
        :type text: `str`
        :return: A paragraph of text in html format.
        :rtype: `str`
        """
        pass

    def filter_unsafe_tags(self, html: str) -> str:
        """Filter some unsafe elements in html because they may be harmful to our app.
        :param html: A paragraph of text in html format.
        :type html: `str`
        :return: A paragraph of text in html format.
        :rtype: `str`
        """
        pattern = re.compile('<script.*?>.*?</script.*?>')
        new_html = re.sub(pattern, '', html)
        return new_html
    

class PlainTextToHtml(TextConverter, PlainText):
    def convert_to_html(self, text):
        html = super().convert(text)
        return self.filter_unsafe_tags(html)


class MarkdownToHtml(TextConverter, Markdown):
    def convert_to_html(self, text):
        html = super().convert(text)
        return self.filter_unsafe_tags(html)


class ReST2Html(TextConverter, ReST):
    def convert_to_html(self, text):
        pass