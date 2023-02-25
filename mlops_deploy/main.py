from flask import Flask, request, jsonify
#from flask_basicauth import BasicAuth
from textblob import TextBlob
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle
import os
import json

# df=pd.read_csv('C:/Users/rpwaltenberg/Downloads/casas.csv')

fls='modelo.sav' in os.listdir('../../models/')
colunas=['tamanho','ano','garagem']
# creds=json.load(open('creds.json','r'))

# verifica se já existe o modelo salvo na pasta local.
# caso não exista, faz a serialização (salva a variavel do modelo em um arquivo, sendo que nas próximas execuções, não será efetuado o cálculo)
if fls is False:
    df=pd.read_csv('../../data/processed/casas.csv')
    X=df.drop('preco', axis=1)
    y=df['preco']

    X_train, X_test, y_train, y_test=train_test_split(X, y, test_size=0.3, random_state=42)
    modelo=LinearRegression()
    modelo.fit(X_train, y_train)

    pickle.dump(modelo, open('../../models/modelo.sav','wb'))

else:
    pass

modelo=pickle.load(open('../../models/modelo.sav', 'rb'))


app=Flask(__name__)
app.config['BASIC_AUTH_USERNAME']=os.environ.get('BASIC_AUTH_USERNAME') # creds['cred_teste']['usr']
app.config['BASIC_AUTH_PASSWORD']=os.environ.get('BASIC_AUTH_PASSWORD') # creds['cred_teste']['psw']

basic_auth=BasicAuth(app)

@app.route('/')
@basic_auth.required
def home():
    return 'Minha primeira API'

@app.route('/sentimento/<frase>')
@basic_auth.required
def sentimento(frase):
    tb=TextBlob(frase)
    tb_en=tb.translate(from_lang='pt_br' ,to='en')

    polaridade=tb_en.sentiment.polarity
    return f'Polaridade: {polaridade}'

@app.route('/cotacao/', methods=['POST'])
@basic_auth.required
def cotacao():
    dados=request.get_json()
    dados_input=[dados[col] for col in colunas]
    preco=modelo.predict([dados_input])
    return jsonify(preco=preco[0])

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0')

# 34.145.70.37 -- ip vm gcp
