import pickle

import pandas as pd
from flask import Flask, render_template, request

# molezinha, só tem que setar as pastas de template e assets
app = Flask(__name__, template_folder='template', static_folder='template/assets')

# Treina lá, usa cá
modelo_pipeline = pickle.load(open('./models/pipe.pkl', 'rb'))

@app.route('/')
def home():
    return render_template("homepage.html")


@app.route('/dados_cliente')
def dados_cliente():
    return render_template("form.html")


def get_data():
    sexo = request.form.get('sexo')
    range_valorContrato = request.form.get('range_valorContrato')
    range_idade = request.form.get('range_idade')
    range_estadoRendaPercapita = request.form.get('range_estadoRendaPercapita')
    range_tempoRelacionamento = request.form.get('range_tempoRelacionamento')
    range_cidadeRendaPercapita = request.form.get('range_cidadeRendaPercapita')
    range_rendaMensal = request.form.get('range_rendaMensal')
    uf = request.form.get('uf')
    
    d_dict = {'sexo': [sexo], 'range_valorContrato': [range_valorContrato], 'range_idade': [range_idade],
              'range_estadoRendaPercapita': [range_estadoRendaPercapita], 'range_tempoRelacionamento': [range_tempoRelacionamento], 'range_cidadeRendaPercapita': [range_cidadeRendaPercapita],
              'range_rendaMensal': [range_rendaMensal]}

    print(d_dict)     
    return pd.DataFrame.from_dict(d_dict, orient='columns')


@app.route('/send', methods=['POST'])
def show_data():
    df = get_data()
    df = df[['sexo', 'range_cidadeRendaPercapita', 
       'range_estadoRendaPercapita', 'range_idade',
       'range_tempoRelacionamento', 'range_rendaMensal',
       'range_valorContrato']]

    prediction = modelo_pipeline.predict(df)
    outcome = 'Existe maior risco de inadimplência nesse perfil de cliente, solicitar a gerência o histórico de relacionamento para validar a oferta.'
           
    
    if prediction == 0:
        outcome = 'Perfil de cliente aprovado para crédito'
        

    return render_template('result.html', tables=[df.to_html(classes='data', header=True, col_space=10)],
                           result=outcome)


if __name__ == "__main__":
    app.run(debug=True)
