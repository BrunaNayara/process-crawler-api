import requests

from tribunal_crawler import TribunalCrawler


class DataManager:
    def __init__(self):
        pass

    def get_process_data(self, process_number):
        tribunal_crawler = TribunalCrawler()

        numero_digito, ano, jud, trib, origem = self.get_jtr_code(process_number)

        response = {}
        i = 0
        for website in tribunal_crawler.websites:
            i += 1
            website = website.format(numero_digito=numero_digito, ano=ano, origem=origem, processo=process_number)
            print("website:" + website)
            r = requests.get(website)
            response_info = tribunal_crawler.get_all_important_info(r.text)
            if(response_info):
                response[i] = response_info


        return response

    def get_jtr_code(self, process_number):
        numero_digito, ano, jud, trib, origem = process_number.split(".")
        return numero_digito, ano, jud, trib, origem
        # jtr_code = jud + "." + trib
        # return jtr_code
