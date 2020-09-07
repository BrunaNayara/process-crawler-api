import re
import requests

from tribunal_crawler import TribunalCrawler


class DataManager:
    def __init__(self):
        pass

    def get_process_data(self, process_number):
        if not self._is_valid_process_number(process_number):
            return "Not a valid process number"

        jtr = self.get_jtr_code(process_number)
        tribunal_crawler = self.instatiate_crawler(jtr)

        return tribunal_crawler.extract_data_from_all_graus(process_number)

    def get_jtr_code(self, process_number):
        numero_digito, ano, jud, trib, origem = process_number.split(".")
        return jud + "." + trib

    def instatiate_crawler(self, jtr):
        tribunals = {
            "8.02": TribunalCrawler,
        }

        return tribunals[jtr]()

    def _is_valid_process_number(self, process_number):
        process_format_number = re.compile('([0-9]{7})-([0-9]{2}).([0-9]{4}).([0-9]{1}).([0-9]{2}).([0-9]{4})')
        return bool(process_format_number.match(process_number))
