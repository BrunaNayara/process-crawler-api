import requests

from bs4 import BeautifulSoup, Comment, Tag
import crawler


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
            r = requests.get(self.format_request_string(website, process_number))
            response_info = self.get_all_important_info(r.text)
            if response_info:
                response[i] = response_info

        return response

    def get_all_important_info(self, html):
        soup = BeautifulSoup(html, "html.parser")
        if not self.found_info(soup):
            print("Não achou a info")
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

    def format_request_string(self, url, processo):
        numero_digito, ano, jud, trib, origem = self.get_process_number_info(processo)
        return url.format(
            numero_digito=numero_digito, ano=ano, origem=origem, processo=processo
        )

    def get_process_number_info(self, process_number):
        numero_digito, ano, jud, trib, origem = process_number.split(".")
        return numero_digito, ano, jud, trib, origem

    def get_basic_attributes(self, soup):
        data = {}
        basic_data_soup = soup.find(id="containerDadosPrincipaisProcesso")

        for item in self.important_basic_attributes:
            attribute = basic_data_soup.find(id=self.important_basic_attributes[item])
            data[item] = crawler.remove_whitespaces(crawler.only_text(attribute))[0]

        basic_detail_soup = soup.find(id="maisDetalhes")
        for item in self.important_basic_detail_attributes:
            attribute = basic_detail_soup.find(id=self.important_basic_detail_attributes[item])
            data[item] = crawler.remove_whitespaces(crawler.only_text(attribute))[0]

        print(data)
        return data

    def get_participants(self, soup):
        participants_table = soup.find(id="tableTodasPartes") or soup.find(
            id="tablePartesPrincipais"
        )
        participants_table = crawler.clean_html(participants_table)
        participants_list = crawler.remove_whitespaces(
            crawler.only_text(participants_table)
        )

        participants = {
            "autores": {"partes": [], "advogados": [],},
            "reus": {"partes": [], "advogados": [],},
        }

        autor = ["autor", "autora", "agravante"]
        reu = ["ré", "réu", "agravado"]
        adv = ["advogado", "advogada", "repreleg"]
        autores = []

        it = iter(participants_list)
        last_participant = None
        for p in it:
            p = p.lower().strip(":")
            if p in autor:
                participants["autores"]["partes"].append(next(it))
                last_participant = "autor"

            elif p in reu:
                participants["reus"]["partes"].append(next(it))
                last_participant = "réu"

            elif p in adv:
                if last_participant in autor:
                    participants["autores"]["advogados"].append(next(it))
                if last_participant in reu:
                    participants["reus"]["advogados"].append(next(it))

        return participants

    def get_activity(self, soup):
        activity_table = soup.find(id="tabelaTodasMovimentacoes") or soup.find(
            id="tabelaUltimasMovimentacoes"
        )
        activity_table = crawler.clean_html(activity_table)

        activity = []
        for tr in activity_table:
            if isinstance(tr, Tag):
                td_list = tr.find_all("td")
                date = td_list[0].text.strip()
                content = crawler.remove_whitespaces(crawler.only_text(td_list[-1]))[0]
                activity.append((date, content))

        return activity

    def found_info(self, soup):
        return not soup.find(id="mensagemRetorno")

    @property
    def important_basic_attributes(self):
        return {
            "classe": "classeProcesso",
            "assunto": "assuntoProcesso",
            "juiz": "juizProcesso",

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
                "https://esaj.tjms.jus.br/cpopg5/show.do?processo.codigo=01001ZB2W0000&processo.foro=1&processo.numero=0821901-51.2018.8.12.0001&uuidCaptcha=sajcaptcha_46b010cc16294f7e81e3cc1fc37f7d0c",
                #"https://esaj.tjms.jus.br/cposg5/search.do?conversationId=&paginaConsulta=0&cbPesquisa=NUMPROC&numeroDigitoAnoUnificado=0821901-51.2018&foroNumeroUnificado=0001&dePesquisaNuUnificado=0821901-51.2018.8.12.0001&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO",
            ],
        }

        return known_tribunal.get(jtr_code, "Invalid code")
