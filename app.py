from flask import Flask
from flask import request
import requests
import crawler

app = Flask(__name__)


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
