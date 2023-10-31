import requests
import json

def OCR(filename, lang='por'):
    payload = {'isOverlayRequired': False,
           'apikey': 'K83917025188957',
           'language': lang,
           }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                        files={filename: f},
                        data=payload,
                        )
    s = r.content.decode() # resultado em string json
    dic = json.loads(s) # converte string json para dicionario
    return dic

from flask import Flask, request, render_template
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    texto = None
    if request.method == 'POST':
        file = request.files['file']
        file.save(file.filename)
        res = OCR(file.filename) # puxei o ocr aqui
        texto = res['ParsedResults'][0]['ParsedText']
        
    return f'''<!DOCTYPE HTML>
    <html>
    <head>
        <title>UNIFEI-OCR</title>
        <style>
            body {{
                margin: 0;
                border: 0;
                box-sizing: border-box;
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
            }}

            .form {{
                width: 100%;
                height: 240px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                flex-direction: column;
            }}

            input,
            button {{
                border-radius: 8px;
                outline: none;
            }}

            button {{
                background: #e06391;
                border: 0;
                color: #fff;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <form method="POST" enctype="multipart/form-data" class="form">
            <h3>Faça o upload da imagem</h3>
            <label style="width: 300px; height: 50px; background-color: #dfe6f9; border-radius: 8px;">
            <input type="file" name="file" style="display: none">
            </label>
            <button type="submit" name="submit" style="width: 300px; height: 50px;" value="Enviar">
                Send
            </button>
        </form>
        <h3>Texto da imagem enviada: {texto}!</h3>
    </body>
    </html>'''


if __name__ == '__main__':
    app.run(debug=True)