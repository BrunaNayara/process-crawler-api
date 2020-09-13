
def format_request_string(url, processo):
    numero_digito, ano, jud, trib, origem = get_process_number_info(processo)
    return url.format(
        numero_digito=numero_digito, ano=ano, origem=origem, processo=processo
    )

def get_process_number_info(process_number):
    numero_digito, ano, jud, trib, origem = process_number.split(".")
    return numero_digito, ano, jud, trib, origem
