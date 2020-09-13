from crawlers import soup_helper


def format_request_string(url, processo):
    numero_digito, ano, jud, trib, origem = get_process_number_info(processo)
    return url.format(
        numero_digito=numero_digito, ano=ano, origem=origem, processo=processo
    )

def get_process_number_info(process_number):
    numero_digito, ano, jud, trib, origem = process_number.split(".")
    return numero_digito, ano, jud, trib, origem


def map_data(info_list, expected_attributes):
    data = {}
    it = iter(info_list)
    for key in it:
        if key.strip(":").lower().strip() in expected_attributes:
            data[key] = next(it)

    return data


def get_activity(table):
    activity = []
    for tr in table:
        if soup_helper.is_tag(tr):
            td_list = tr.find_all("td")
            date = td_list[0].text.strip()
            content = soup_helper.get_clean_text(td_list[-1])[0]
            activity.append((date, content))

    return activity


def get_participants(participants_list):
    participants = {
        "autores": {"partes": [], "advogados": [],},
        "reus": {"partes": [], "advogados": [],},
    }

    autor = ["autor", "autora", "agravante", "apelante"]
    reu = ["ré", "réu", "agravado", "apelado"]
    adv = ["advogado", "advogada", "repreleg", "proc. do estado"]
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
