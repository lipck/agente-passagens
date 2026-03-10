import os
import requests
import random
import time

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


origens = ["GIG","SDU"]

destinos = [
"JFK","MIA","LAX","MCO",
"LHR","CDG","MAD","BCN",
"FCO","LIS","AMS","FRA",
"ZRH","DXB","DOH",
"SCL","EZE","LIM",
"YYZ","YUL",
"NRT","HND","ICN"
]

def gerar_preco():
    return random.randint(800,4000)

def gerar_distancia():
    return random.randint(4000,10000)

def verificar_promocoes():

    for origem in origens:
        for destino in destinos:

            preco = gerar_preco()
            distancia = gerar_distancia()

            preco_km = preco/distancia

            if preco < 1500:

                mensagem = f"""
🔥 PROMOÇÃO DETECTADA

Origem: {origem}
Destino: {destino}

Preço: R$ {preco}

Preço por km: {round(preco_km,2)}

Pesquisar em:
Google Flights
https://www.google.com/travel/flights

ou

Skyscanner
https://www.skyscanner.com
"""

                enviar_alerta(mensagem)

            milhas = random.randint(20000,70000)

            if milhas <= 80000:

                mensagem = f"""
✈️ PROMOÇÃO COM MILHAS

Origem: {origem}
Destino: {destino}

Milhas necessárias: {milhas}

Programa:
Azul Fidelidade

Datas sugeridas:
flexível próximos 6 meses

Pesquisar em:
https://www.voeazul.com.br
"""

                enviar_alerta(mensagem)


while True:

    verificar_promocoes()

    print("Verificação concluída")

    time.sleep(900)
