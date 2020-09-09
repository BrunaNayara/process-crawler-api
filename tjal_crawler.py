import requests

from bs4 import BeautifulSoup, Comment, Tag
import crawler


class TJALCrawler:
    def __init__(self):
        self.websites = self._correct_tribunal_website("8.02")

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
        table_data = soup.findAll("table", "secaoFormBody")[1]
        clean_table = crawler.clean_html(table_data)
        info_list = crawler.remove_whitespaces(crawler.only_text(clean_table))

        data = {}
        it = iter(info_list)
        for key in it:
            if key.strip(":").lower().strip() in self.important_basic_attributes:
                data[key] = next(it)

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
        adv = ["advogado", "advogada"]
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
