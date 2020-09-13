from bs4 import BeautifulSoup, Comment, Tag


def is_tag(item):
    return isinstance(item, Tag)

def get_string_list(soup):
    soup = remove_comments(soup)
    string_list = remove_whitespaces(only_text(soup))
    return string_list


def find_any_from_id(soup, one, another):
    return soup.find(id=one) or soup.find(id=another)


def remove_comments(html):
    for element in html(text=lambda text: isinstance(text, Comment)):
        element.extract()
    return html


def get_clean_text(soup):
    return remove_whitespaces(only_text(soup))

def remove_whitespaces(strings):
    return [s.strip() for s in strings if s.strip() != ""]


def only_text(html):
    return html.find_all(text=True)
