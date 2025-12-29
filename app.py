from flask import Flask, render_template_string, request
from threading import Thread
import requests
import os

app = Flask(__name__)

# HTML com estilo para a Tabela
html_layout = '''
<!DOCTYPE html>
<html>
<head>
    <title>BioInfo Table</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; background-color: #e3f2fd; }
        .container { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); max-width: 800px; margin: auto; }
        h2 { color: #2c3e50; text-align: center; }
        .search-box { display: flex; gap: 10px; margin-bottom: 30px; justify-content: center; }
        input { padding: 12px; width: 60%; border: 2px solid #e0e0e0; border-radius: 6px; outline: none; transition: border-color 0.3s; }
        input:focus { border-color: #007bff; }
        button { padding: 12px 25px; background-color: #007bff; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; }
        button:hover { background-color: #0056b3; }

        table { width: 100%; border-collapse: collapse; margin-top: 20px; background: white; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background-color: #f2f2f2; color: #333; text-transform: uppercase; font-size: 12px; }
        tr:hover { background-color: #f9f9f9; }
        .error { color: #d9534f; background: #fdf7f7; padding: 15px; border-radius: 6px; border: 1px solid #eed3d7; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🧬 Explorador Genético (RSID)</h2>
        <div class="search-box">
            <form method="POST" style="width: 100%; display: flex; justify-content: center; gap: 10px;">
                <input type="text" name="rsid_input" placeholder="Ex: rs53576" required>
                <button type="submit">Analisar</button>
            </form>
        </div>

        {% if erro %}
            <div class="error">{{ erro }}</div>
        {% endif %}

        {% if dados %}
            <h3>Dados da Variante: {{ rsid }}</h3>
            <table>
                <thead>
                    <tr>
                        <th>Propriedade</th>
                        <th>Valor</th>
                    </tr>
                </thead>
                <tbody>
                    {% for chave, valor in dados.items() %}
                    <tr>
                        <td><strong>{{ chave }}</strong></td>
                        <td>{{ valor | string }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    dados_formatados = None
    erro_msg = None
    rsid_solicitado = None

    if request.method == 'POST':
        rsid_solicitado = request.form.get('rsid_input').strip()
        url = f"https://rest.ensembl.org/variation/human/{rsid_solicitado}"
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                # Pegamos o JSON e passamos para o template como um dicionário
                dados_formatados = response.json()
            else:
                erro_msg = f"Variante '{rsid_solicitado}' não encontrada na base Ensembl."
        except Exception as e:
            erro_msg = f"Erro de conexão: {str(e)}"

    return render_template_string(html_layout, dados=dados_formatados, erro=erro_msg, rsid=rsid_solicitado)

def run_app():
    app.run(port=5000, host='0.0.0.0', debug=False)

# Inicia o servidor em Thread
Thread(target=run_app).start()

# Gera o link de acesso público
print("Clique no link abaixo para abrir o seu site:")
!ssh -o StrictHostKeyChecking=no -R 80:localhost:5000 nokey@localhost.run
