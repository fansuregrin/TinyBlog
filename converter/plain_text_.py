


class PlainText:
    def convert(self, text: str) -> str:
        """Covert a paragraph of plain text to html.
        :param text: A paragraph of plain text.
        :type text: `str`
        :return: A paragraph of text in html format.
        :rtype: `str`
        """
        self.filter_nsfw(text)
        html = ''
        for line in text.split('\n'):
            html += f'<p>{line}</p>'
        return html

    def filter_nsfw(self, text) -> str:
        """Filter some nfsw words, such as words \
        involving minor pornography, violence, and discrimination.
        :param text: A paragraph of plain text.
        :type text: `str`
        :return: A paragraph of filtered human-friendly palin text.
        :rtype: `str`
        """
        return text