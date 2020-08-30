from flask import Flask
from flask import request
import requests
import crawler

app = Flask(__name__)


@app.route("/crawl/<int:grau>")
def get_process(grau):
    if grau == 1:
        r = requests.get("https://www2.tjal.jus.br/cpopg/show.do?processo.codigo=01000O7550000&processo.foro=1&uuidCaptcha=sajcaptcha_3065571f7e764a90a8d55727251b85c2")
    else:
        r = requests.get("https://www2.tjal.jus.br/cposg5/search.do?conversationId=&paginaConsulta=1&cbPesquisa=NUMPROC&tipoNuProcesso=UNIFICADO&numeroDigitoAnoUnificado=0806233-85.2019&foroNumeroUnificado=0000&dePesquisaNuUnificado=0806233-85.2019.8.02.0000&dePesquisa=&uuidCaptcha=&pbEnviar=Pesquisar")
    return crawler.get_all_important_info(r.text)

@app.route("/")
def hello_world():
    return "Starting our API."


@app.route("/processo", methods=["GET"])
def get_processo_info():
    content_type = request.headers.get("Content-Type")
    if not _is_valid_content_type(content_type):
        print("not valid content type")
        return "Cannot parse content type"

    json_data = request.get_json(request.data)
    processo = json_data.get("numProcesso")
    numero_digito, ano, jud, trib, origem = processo.split(".")
    jtr_code = jud + "." + trib

    response = ""
    websites = _correct_tribunal_website(jtr_code)
    if websites == "Invalid code": # TODO raise exception
        return "Could not find this process"

    for website in websites:
        print(website)
        r = requests.get(website)
        response += crawler.get_title(r.text)

    return response


def _is_valid_content_type(incoming):
    return incoming == "application/json"


def _correct_tribunal_website(jtr_code):
    known_tribunal = {
        "8.02": [
            "https://www2.tjal.jus.br/cpopg/open.do",
            "https://www2.tjal.jus.br/cposg5/open.do",
        ],
        "8.12": [
            "https://esaj.tjms.jus.br/cpopg5/open.do",
            "ttps://esaj.tjms.jus.br/cposg5/open.do",
        ]
    }

    return known_tribunal.get(jtr_code, "Invalid code")
