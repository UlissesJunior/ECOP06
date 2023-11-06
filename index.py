import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
from flask import Flask, render_template, request

produtos = []
valores = []

def ofertas(pagina:int):
    # página de ofertas do mercado livre
    URL = 'https://www.mercadolivre.com.br/ofertas?container_id=MLB779362-1&page=' + str(pagina)
    response = requests.get(URL)
    doc = BeautifulSoup(response.text,'html.parser')
    if response.status_code != 200:
        raise Exception('Problemas na URL: {0}'.format(response))
    # nome do produto
    produtos_tags = doc.find_all('p', class_ = 'promotion-item__title')
    for tags in produtos_tags:
        produtos.append(tags.text)
    # preço do produto
    valor_tags = doc.find_all('div', class_ = 'andes-money-amount-combo__main-container')
    for tags in valor_tags:
        valores.append(tags.text.replace('Â',''))

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and 'pagina' in request.form:
        p = request.form['pagina']
        ofertas(p)
        ml = pd.DataFrame({'Produtos': produtos,'Preços': valores})
        ml['Preços'] = ml['Preços'].str.extract(r'(\d+[\.,]?\d*)')
        ml = ml.sort_values('Preços')
        tabela = ml.to_html(index=False)
        return render_template('index.html', tabela=tabela)

    else:
        return render_template('index.html', tabela='')
    
if __name__ == '__main__':
    app.run(debug=True)