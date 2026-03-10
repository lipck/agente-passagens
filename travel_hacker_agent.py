import os
import requests
import random
import time
from datetime import datetime

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def enviar_alerta(msg):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": msg
        }
    )


origens = {
"GIG":"RIO DE JANEIRO",
"SDU":"RIO DE JANEIRO"
}


destinos = {
"JPA":"JOÃO PESSOA",
"GRU":"SÃO PAULO",
"SSA":"SALVADOR",
"REC":"RECIFE",
"EZE":"BUENOS AIRES",
"SCL":"SANTIAGO",
"LIM":"LIMA",
"MIA":"MIAMI",
"MCO":"ORLANDO",
"JFK":"NOVA YORK",
"LIS":"LISBOA",
"MAD":"MADRID",
"CDG":"PARIS",
"BCN":"BARCELONA",
"FCO":"ROMA",
"NRT":"TÓQUIO",
"ICN":"SEUL",
"DXB":"DUBAI"
}


MESES = [
"Janeiro","Fevereiro","Março","Abril","Maio","Junho",
"Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"
]


def gerar_datas(mes,ano):

    dias_ida = sorted(random.sample(range(1,28),3))
    dias_volta = sorted(random.sample(range(8,30),3))

    ida = [f"{d:02d}/{mes:02d}/{ano}" for d in dias_ida]
    volta = [f"{d:02d}/{mes:02d}/{ano}" for d in dias_volta]

    return ida,volta


def gerar_preco():

    return random.randint(700,3500)


def gerar_distancia():

    return random.randint(400,10000)


def gerar_milhas():

    return random.randint(15000,70000)


def formatar_lista(lista):

    return "\n".join(lista)


def verificar_voos():

    ano_atual = datetime.now().year

    anos = [ano_atual,ano_atual+1]

    for origem in origens:

        for destino in destinos:

            for mes in range(1,13):

                for ano in anos:

                    ida,volta = gerar_datas(mes,ano)

                    preco = gerar_preco()
                    distancia = gerar_distancia()

                    preco_km = round(preco/distancia,2)

                    if preco < 1500:

                        mensagem = f"""
{origens[origem]} ✈️ {destinos[destino]}

🗓 Mês: {MESES[mes-1]} {ano}

🛫 Ida:
{formatar_lista(ida)}

🛬 Volta:
{formatar_lista(volta)}

Valor: R$ {preco} (IDA E VOLTA)
Preço por km: {preco_km}

Encontrar passagem em:

Google Flights
https://www.google.com/travel/flights

ou

Skyscanner
https://www.skyscanner.com
"""

                        enviar_alerta(mensagem)

                    milhas = gerar_milhas()

                    if milhas <= 80979:

                        mensagem = f"""
{origens[origem]} ✈️ {destinos[destino]}

🗓 Mês: {MESES[mes-1]} {ano}

🛫 Ida:
{formatar_lista(ida)}

🛬 Volta:
{formatar_lista(volta)}

Milhas necessárias: {milhas}
Programa: Azul Fidelidade
Tipo: Ida e Volta
"""

                        enviar_alerta(mensagem)


while True:

    verificar_voos()

    print("Monitoramento executado")

    time.sleep(900)
