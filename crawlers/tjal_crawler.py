import requests

from bs4 import BeautifulSoup, Comment, Tag
from crawlers import soup_helper, crawler_helper


class TJALCrawler:
    def __init__(self):
        self.websites = self._correct_tribunal_website("8.02")

    def extract_data_from_all_graus(self, process_number):
        response = {}
        i = 0
        for website in self.websites:
            i += 1
            r = requests.get(crawler_helper.format_request_string(website, process_number))
            response_info = self.get_all_important_info(r.text)
            if response_info:
                response[i] = response_info

        return response

    def get_all_important_info(self, html):
        soup = BeautifulSoup(html, "html.parser")
        if not self.found_info(soup):
            print("Não achou informação sobre o processo")
            return "No info"
        basic_info = self.get_basic_attributes(soup)
        participants = self.get_participants(soup)
        activity = self.get_activity(soup)
        all_data = {
            "dados do processo": basic_info,
            "partes": participants,
            "movimentacoes": activity,
        }
        return all_data

    def get_basic_attributes(self, soup):
        table_data = soup.findAll("table", "secaoFormBody")[1]
        info_list = soup_helper.get_string_list(table_data)
        attributes = crawler_helper.map_data(info_list, self.important_basic_attributes)
        return attributes

    def get_participants(self, soup):
        participants_table = soup_helper.find_any_from_id(soup,
            "tableTodasPartes", "tablePartesPrincipais"
        )

        participants_list = soup_helper.get_string_list(participants_table)
        participants = crawler_helper.get_participants(participants_list)
        return participants

    def get_activity(self, soup):
        activity_table = soup_helper.find_any_from_id(soup,
            "tabelaTodasMovimentacoes", "tabelaUltimasMovimentacoes"
        )
        activity_table = soup_helper.remove_comments(activity_table)
        activity = crawler_helper.get_activity(activity_table)
        return activity

    def found_info(self, soup):
        return not soup.find(id="mensagemRetorno")

    @property
    def important_basic_attributes(self):
        return [
            "classe",
            "área",
            "assunto",
            "distribuição",
            "juiz",
            "valor da ação",
        ]

    def _correct_tribunal_website(self, jtr_code):
        known_tribunal = {
            "8.02": [
                "https://www2.tjal.jus.br/cpopg/search.do?conversationId=&dadosConsulta.localPesquisa.cdLocal=-1&cbPesquisa=NUMPROC&dadosConsulta.tipoNuProcesso=UNIFICADO&numeroDigitoAnoUnificado={numero_digito}.{ano}&foroNumeroUnificado={origem}&dadosConsulta.valorConsultaNuUnificado={processo}&dadosConsulta.valorConsulta=&uuidCaptcha=",
                "https://www2.tjal.jus.br/cposg5/search.do?conversationId=&paginaConsulta=1&cbPesquisa=NUMPROC&tipoNuProcesso=UNIFICADO&numeroDigitoAnoUnificado={numero_digito}.{ano}&foroNumeroUnificado={origem}&dePesquisaNuUnificado={processo}&dePesquisa=&uuidCaptcha=&pbEnviar=Pesquisar",
            ],
            "8.12": [
                "https://esaj.tjms.jus.br/cpopg5/open.do",
                "ttps://esaj.tjms.jus.br/cposg5/open.do",
            ],
        }

        return known_tribunal.get(jtr_code, "Invalid code")
