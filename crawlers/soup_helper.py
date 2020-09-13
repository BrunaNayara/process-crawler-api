from bs4 import BeautifulSoup, Comment, Tag


def remove_comments(html):
    for element in html(text=lambda text: isinstance(text, Comment)):
        element.extract()
    return html


def remove_whitespaces(strings):
    return [s.strip() for s in strings if s.strip() != ""]


def only_text(html):
    return html.find_all(text=True)
