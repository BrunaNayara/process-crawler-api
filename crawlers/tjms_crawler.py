import requests

from bs4 import BeautifulSoup, Comment, Tag
from crawlers import soup_helper, crawler_helper


class TJMSCrawler:
    def __init__(self):
        self.websites = self._correct_tribunal_website("8.12")
        print("TJMS")

    def extract_data_from_all_graus(self, process_number):
        response = {}
        i = 0
        for website in self.websites:
            i += 1
            print("website:" + website)
            r = requests.get(crawler_helper.format_request_string(website, process_number))
            response_info = self.get_all_important_info(r.text)
            if response_info:
                response[i] = response_info

        return response

    def first_grau_data(self, html):
        pass

    def get_all_important_info(self, html):
        soup = BeautifulSoup(html, "html.parser")
        if not self.found_info(soup):
            print("Não achou a info")
            return "No info"
        basic_info = self.get_basic_attributes_without_id(soup)
        participants = self.get_participants(soup)
        activity = self.get_activity(soup)
        all_data = {
            "dados do processo": basic_info,
            "partes": participants,
            "movimentacoes": activity,
        }
        return all_data

    def get_basic_attributes(self, soup):
        data = {}
        basic_data_soup = soup.find(id="containerDadosPrincipaisProcesso")

        for item in self.important_basic_attributes:
            attribute = basic_data_soup.find(id=self.important_basic_attributes[item])
            data[item] = soup_helper.remove_whitespaces(soup_helper.only_text(attribute))[0]

        basic_detail_soup = soup.find(id="maisDetalhes")
        for item in self.important_basic_detail_attributes:
            attribute = basic_detail_soup.find(id=self.important_basic_detail_attributes[item])
            data[item] = soup_helper.remove_whitespaces(soup_helper.only_text(attribute))[0]

        print(data)
        return data

    def get_basic_attributes_without_id(self, soup):
        table_data = soup.findAll("div", "unj-entity-header__summary")[0]
        info_list = soup_helper.get_string_list(table_data)

        table_data = soup.findAll("div", "unj-entity-header__details")[0]
        info_list += soup_helper.get_string_list(table_data)

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
        return {
            "classe": "classeProcesso",
            "assunto": "assuntoProcesso",
            "juiz": "juizProcesso",
            "área": "areaProcesso",
            "distribuição": "dataHoraDistribuicaoProcesso",
            "valor da ação": "valorAcaoProcesso",
        }

    @property
    def important_basic_detail_attributes(self):
        return {
            "area": "areaProcesso",
            "distribuição": "dataHoraDistribuicaoProcesso",
            "valor da ação": "valorAcaoProcesso",
        }

    def _correct_tribunal_website(self, jtr_code):
        known_tribunal = {
            "8.12": [
                #"https://esaj.tjms.jus.br/cpopg5/show.do?processo.codigo=01001ZB2W0000&processo.foro=1&processo.numero=0821901-51.2018.8.12.0001&uuidCaptcha=sajcaptcha_46b010cc16294f7e81e3cc1fc37f7d0c",
                "https://esaj.tjms.jus.br/cposg5/search.do?conversationId=&paginaConsulta=0&cbPesquisa=NUMPROC&numeroDigitoAnoUnificado=0821901-51.2018&foroNumeroUnificado=0001&dePesquisaNuUnificado=0821901-51.2018.8.12.0001&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO",
            ],
        }

        return known_tribunal.get(jtr_code, "Invalid code")
