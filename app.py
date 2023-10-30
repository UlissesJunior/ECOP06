from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    nome = None
    if request.method == 'POST' and 'nome' in request.form:
      nome = request.form['nome']
    return render_template('index.html', nome=nome)

if __name__ == "main":
   app.run(debug=True)