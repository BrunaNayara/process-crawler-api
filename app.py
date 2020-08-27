from flask import Flask
import requests
import crawler

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Starting our API.'

@app.route('/get')
def get_site():
    r = requests.get('https://www2.tjal.jus.br/cpopg/open.do')
    return crawler.get_title(r.text)
