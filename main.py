import os.path
import json
from func_flask import new_parser
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/contacts/')
def contacts():
    contxt = {'name': 'Сергей Шишов',
              'creation_date': '01-02-2023',
              'phone': '+7 (912) 391-44-23'
              }
    return render_template('contacts.html', **contxt)


@app.route('/results/')
def results():
    # if os.path.exists('results.json'):
    #     with open('results.json', 'r') as f:
    #         text = json.load(f)
    # else:
    text = 'Результата нет'
    return render_template('results.html', text=text)


@app.route('/run/', methods=['GET'])
def run_get():
    # if os.path.exists('results.json'):
    #     with open('results.json', 'r') as f:
    #         text = json.load(f)
    # else:
    #     text = ''
    return render_template('form.html') #, text=text)


@app.route('/run/', methods=['POST'])
def run_post():
    text = []
    qq = request.form['input_text']
    ct = request.form['where']
    if qq != '':
        result = new_parser(qq, ct)
        if result != 'Данных нет':
            text.append(result)
        else:
            text = 'Результата нет'
            print(text)
    else:
        text = 'Результата нет'
        print('Пустое поле')

    return render_template('results.html', text=text)


if __name__ == "__main__":
    app.run(debug=True)
