from flask import Flask
from flask import request
import requests
import crawler

from data_manager import DataManager
from tribunal_crawler import TribunalCrawler

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Go to /processo/<numero-do-processo>"


@app.route("/processo/<processo>", methods=["GET"])
def get_processo_info_manager(processo):
    print(processo)

    json_data = request.get_json(request.data)

    dm = DataManager()
    return dm.get_process_data(processo)
