from bs4 import BeautifulSoup

def get_title(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.title.string
