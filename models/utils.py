import re
from bs4 import BeautifulSoup


def slugify(s: str) -> str:
    """
    """
    pattern = r'[^\w+]'
    valid_slug = re.sub(pattern, '-', s)
    return valid_slug

def html_to_text(html: str) -> str:
    """
    """
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text().replace('\n', ' ')
    return text