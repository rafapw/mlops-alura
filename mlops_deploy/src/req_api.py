import requests
import json

creds=json.load(open('creds.json','r'))
usr=creds['cred_teste']['usr']
psw=creds['cred_teste']['psw']

def consulta(tamanho, ano, garagem):
    url='http://127.0.0.1:5000/cotacao/'
    payload = {'tamanho':tamanho, 'ano':ano, 'garagem':garagem}
    headers = {'content-type': 'application/json'}
    auth=requests.auth.HTTPBasicAuth(usr, psw)
    #, 'usr':creds['cred_teste']['usr'], 'psw':creds['cred_teste']['psw']
    r = requests.post(url, data=json.dumps(payload),headers=headers, auth=auth)
    return r.json()
