
import requests
import json
import os

# ==========================
# CONFIG
# ==========================

def carregar_config():
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)

# ==========================
# PRODUTOS
# ==========================

def carregar_produtos():
    with open("produtos.json", "r", encoding="utf-8") as f:
        return json.load(f)

# ==========================
# HISTORICO
# ==========================

def carregar_historico():

    if not os.path.exists("historico.json"):
        return {}

    with open("historico.json", "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_historico(historico):

    with open("historico.json", "w", encoding="utf-8") as f:
        json.dump(
            historico,
            f,
            indent=4,
            ensure_ascii=False
        )

# ==========================
# TELEGRAM
# ==========================

def enviar(token, group_id, mensagem):

    resposta = requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data={
            "chat_id": group_id,
            "text": mensagem
        }
    )

    print("Telegram:", resposta.status_code)

# ==========================
# MONITORAMENTO
# ==========================

def verificar():

    config = carregar_config()

    token = config["token"]
    group_id = config["group_id"]

    produtos = carregar_produtos()

    historico = carregar_historico()

    print("Produtos monitorados:")

    for produto, preco_alvo in produtos.items():

        print(f"{produto} -> R$ {preco_alvo}")

        chave = produto.lower()

        if chave in historico:
            continue

        mensagem = f"""
🚀 PROMOCOP

🔍 Monitorando:
{produto}

💰 Preço alvo:
R$ {preco_alvo}

✅ Produto registrado com sucesso.
"""

        enviar(token, group_id, mensagem)

        historico[chave] = {
            "preco_alvo": preco_alvo
        }

    salvar_historico(historico)

    print("Finalizado!")

# ==========================
# MAIN
# ==========================

if __name__ == "__main__":
    verificar()
