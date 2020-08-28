from flask import Flask
from flask import request
import requests
import crawler

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Starting our API."


@app.route("/processo", methods=["GET"])
def get_site():
    content_type = request.headers.get("Content-Type")
    if not _is_valid_content_type(content_type):
        print("not valid content type")
        return "Cannot parse content type"

    json_data = request.get_json(request.data)
    num_processo = json_data.get("numProcesso")
    print(json_data)

    r = requests.get("https://www2.tjal.jus.br/cpopg/open.do")
    return crawler.get_title(r.text)


def _is_valid_content_type(incoming):
    return incoming == "application/json"
