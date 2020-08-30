from bs4 import BeautifulSoup, Comment


def clean_html(html):
    for element in html(text=lambda text: isinstance(text, Comment)):
        element.extract()
    return html

def remove_whitespaces(strings):
    return [s.strip() for s in strings if s.strip() != '']


def only_text(html):
    return html.find_all(text=True)


def get_title(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.title.string


def get_table(html):
    soup = BeautifulSoup(html, 'html.parser')
    table_data = soup.findAll("table", "secaoFormBody")[1]
    return table_data

def get_info_table(html):
    soup = BeautifulSoup(html, 'html.parser')
    table_data = soup.findAll("table", "secaoFormBody")[1]
    clean_table = clean_html(table_data)
    info_list = remove_whitespaces(only_text(clean_table))
    print(len(info_list))

    data = {}
    it = iter(info_list)
    for key in it:
        if key.strip(':').lower() in important_attributes():
            data[key] = next(it)

    for i in data.keys():
        print(i, data[i])
    return data

def important_attributes():
    return [
        'classe',
        'área',
        'assunto',
        'distribuição',
        'juiz',
        'valor da ação',
    ]

def get_string_from_span(tags):
    print(tags)
    print(tags.parent)
    td = tags.find_next_siblings("td")
    print(td)
    for t in span:
        print(t.string)
    return tags
