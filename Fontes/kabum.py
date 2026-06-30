import requests
import json
from bs4 import BeautifulSoup

url = "https://www.kabum.com.br/busca/rtx-5070"

headers = {
    "User-Agent": "Mozilla/5.0"
}

html = requests.get(url, headers=headers).text

soup = BeautifulSoup(html, "lxml")

dados = json.loads(soup.find("script", id="__NEXT_DATA__").string)

# Procura recursivamente por qualquer chave chamada "products"

def procurar(obj, caminho=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            novo = f"{caminho}.{k}" if caminho else k

            if k.lower() == "products":
                print("\nACHOU!")
                print(novo)
                print(type(v))
                print(v if isinstance(v, list) else list(v.keys())[:10])

            procurar(v, novo)

    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            procurar(item, f"{caminho}[{i}]")

procurar(dados)