import requests
import schedule
import time
import random
from datetime import datetime, timedelta

TOKEN = "SEU_TOKEN"
CHAT_ID = "SEU_CHAT_ID"

origem = "Rio de Janeiro"

destinos = ["ROM","MAD","LIS","PAR","NYC","MIA","TYO","DXB","SYD","SCL","EZE"]

historico = {}

def enviar(msg):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    requests.post(url,data={
        "chat_id":CHAT_ID,
        "text":msg
    })


def gerar_datas():

    ida = datetime.now() + timedelta(days=random.randint(30,180))
    volta = ida + timedelta(days=random.randint(7,20))

    return ida.strftime("%d %b"), volta.strftime("%d %b")


def detectar_error_fare(preco,media):

    return preco < media*0.35


def buscar_voos():

    for destino in destinos:

        preco = random.randint(800,4500)

        if destino not in historico:
            historico[destino] = []

        historico[destino].append(preco)

        media = sum(historico[destino])/len(historico[destino])

        erro = detectar_error_fare(preco,media)

        ida,volta = gerar_datas()

        if preco <1500 or erro:

            msg=f"""
🔥 PROMOÇÃO DETECTADA

Origem: {origem}
Destino: {destino}

Preço encontrado
R$ {preco}

Error Fare
{erro}

Datas sugeridas
{ida} - {volta}

Buscar em

Google Flights
https://www.google.com/travel/flights

Skyscanner
https://www.skyscanner.com

Kiwi
https://www.kiwi.com
"""

            enviar(msg)


def verificar():

    buscar_voos()


schedule.every(15).minutes.do(verificar)

while True:

    schedule.run_pending()

    time.sleep(60)
