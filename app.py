from flask import Flask, render_template
from parser_1 import Parser, headers, base_url
from work_ua import Parser_work_ua, headers_work, base_url_work
from rabota_ua import Parser_rabota, headers_rabota, base_url_rabota

app = Flask(__name__)

@app.route('/headhunter', methods=['GET', 'POST'])
def parsing():
    content = Parser(base_url=base_url, headers=headers)
    return render_template('parse.html', content=content)

@app.route('/work', methods=['GET', 'POST'])
def parsing_work():
    content = Parser_work_ua(base_url_work=base_url_work, headers_work=headers_work)
    return render_template('work.html', content=content)

@app.route('/rabota', methods=['GET', 'POST'])
def parsing_rabota():
    content = Parser_rabota(base_url_rabota=base_url_rabota, headers_rabota=headers_rabota)
    return render_template('rabota.html', content=content)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
