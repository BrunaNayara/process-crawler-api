from bs4 import BeautifulSoup, Comment, Tag
import crawler

class TribunalCrawler:
    def __init__(self, websites):
        self.websites = websites

    def get_all_important_info(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        basic_info = self.get_basic_attributes(soup)
        participants = self.get_participants(soup)
        activity = self.get_activity(soup)
        all_data = {
            'dados do processo': basic_info,
            'partes': participants,
            'movimentacoes': activity,
        }
        return all_data

    def get_basic_attributes(self, soup):
        table_data = soup.findAll("table", "secaoFormBody")[1]
        clean_table = crawler.clean_html(table_data)
        info_list = crawler.remove_whitespaces(crawler.only_text(clean_table))

        data = {}
        it = iter(info_list)
        for key in it:
            if key.strip(':').lower().strip() in self.important_basic_attributes:
                data[key] = next(it)

        return data

    def get_participants(self,soup):
        participants_table = soup.find(id="tableTodasPartes") or soup.find(id="tablePartesPrincipais")
        participants_table = crawler.clean_html(participants_table)
        participants_list = crawler.remove_whitespaces(crawler.only_text(participants_table))
        print(participants_list)

        participants = {
            'autores': {
                'partes': [],
                'advogados': [],
            },
            'reus': {
                'partes': [],
                'advogados': [],
            }
        }

        autor = ['autor', 'autora', 'agravante']
        reu = ['ré', 'réu', 'agravado']
        adv = ['advogado', 'advogada']
        autores = []

        it = iter(participants_list)
        last_participant = None
        for p in it:
            p = p.lower().strip(':')
            if p in autor:
                participants['autores']['partes'].append(next(it))
                last_participant = 'autor'

            elif p in reu:
                participants['reus']['partes'].append(next(it))
                last_participant = 'réu'

            elif p in adv:
                if last_participant in autor:
                    participants['autores']['advogados'].append(next(it))
                if last_participant in reu:
                    participants['reus']['advogados'].append(next(it))

        print(participants)
        return participants

    def get_activity(self, soup):
        activity_table = soup.find(id="tabelaTodasMovimentacoes") or soup.find(id="tabelaUltimasMovimentacoes")
        activity_table = crawler.clean_html(activity_table)

        activity = []
        for tr in activity_table:
            if isinstance(tr, Tag):
                td_list = tr.find_all('td')

                date = td_list[0].text.strip()
                content = crawler.remove_whitespaces(crawler.only_text(td_list[-1]))[0]

                activity.append((date, content))

        return activity


    @property
    def important_basic_attributes(self):
        return [
            'classe',
            'área',
            'assunto',
            'distribuição',
            'juiz',
            'valor da ação',
        ]
