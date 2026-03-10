import os
import requests
import random
import time
from datetime import datetime

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def enviar_alerta(mensagem):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": mensagem
        }
    )


origem = "RIO DE JANEIRO"

destinos = [
"JOÃO PESSOA","LISBOA","MADRID","PARIS","ROMA",
"ORLANDO","MIAMI","NOVA YORK",
"SANTIAGO","BUENOS AIRES","LIMA",
"TÓQUIO","SEUL","DUBAI"
]


meses = [
"Janeiro","Fevereiro","Março","Abril","Maio","Junho",
"Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"
]


def gerar_datas():

    ida = sorted(random.sample(range(1,28), random.randint(3,8)))
    volta = sorted(random.sample(range(1,28), random.randint(2,6)))

    ida = ", ".join(map(str, ida))
    volta = ", ".join(map(str, volta))

    return ida, volta


def gerar_preco():

    return random.randint(700,2000)


def gerar_distancia():

    return random.randint(3000,10000)


def gerar_milhas():

    return random.randint(20000,70000)


def gerar_alerta(destino):

    preco = gerar_preco()
    distancia = gerar_distancia()
    preco_km = round(preco/distancia,2)

    mes1, mes2, mes3 = random.sample(meses,3)

    ida1, volta1 = gerar_datas()
    ida2, volta2 = gerar_datas()
    ida3, volta3 = gerar_datas()

    mensagem = f"""
{origem} ✈ {destino}

🗓 Mês de {mes1}

🛫 Ida: {ida1}

🛬 Volta: {volta1}


🗓 Mês de {mes2}

🛫 Ida: {ida2}
🛬 Volta: {volta2}


🗓 Mês de {mes3}

🛫 Ida: {ida3}
🛬 Volta: {volta3}


Valor: R$ {preco} (IDA E VOLTA)

Preço por km: {preco_km}

Pesquisar em:

Google Flights
https://www.google.com/travel/flights

ou

Skyscanner
https://www.skyscanner.com
"""

    enviar_alerta(mensagem)


def gerar_alerta_milhas(destino):

    milhas = gerar_milhas()

    if milhas > 80979:
        return

    ida, volta = gerar_datas()

    mensagem = f"""
{origem} ✈ {destino}

✈ PROMOÇÃO COM MILHAS

Programa:
Azul Fidelidade

Milhas necessárias:
{milhas}

🛫 Ida: {ida}
🛬 Volta: {volta}

Tipo:
IDA E VOLTA

Pesquisar em:
https://www.voeazul.com.br
"""

    enviar_alerta(mensagem)


def verificar_rotas():

    for destino in destinos:

        if random.random() < 0.35:
            gerar_alerta(destino)

        if random.random() < 0.25:
            gerar_alerta_milhas(destino)


while True:

    verificar_rotas()

    print("varredura concluída")

    time.sleep(900)
