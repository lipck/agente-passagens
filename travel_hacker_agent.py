import os
import requests
import random
import time
from datetime import datetime, timedelta
from collections import defaultdict

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

MILHAS_DISPONIVEIS = 80979

origem_nome = "RIO DE JANEIRO"
origens = ["GIG","SDU"]

destinos = {
"LIS":"LISBOA",
"FCO":"ROMA",
"MAD":"MADRID",
"CDG":"PARIS",
"BCN":"BARCELONA",
"MIA":"MIAMI",
"MCO":"ORLANDO",
"JFK":"NOVA YORK",
"SCL":"SANTIAGO",
"EZE":"BUENOS AIRES",
"LIM":"LIMA",
"GRU":"SÃO PAULO",
"REC":"RECIFE",
"SSA":"SALVADOR",
"JPA":"JOÃO PESSOA"
}

def enviar_alerta(msg):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": msg
        }
    )

def gerar_datas():

    hoje = datetime.now()
    limite = hoje + timedelta(days=550)

    datas = []

    while hoje < limite:

        if random.random() < 0.1:
            datas.append(hoje)

        hoje += timedelta(days=1)

    return datas

def agrupar_por_mes(datas):

    grupos = defaultdict(list)

    for d in datas:

        chave = (d.year, d.month)

        grupos[chave].append(d)

    return grupos

def gerar_preco():
    return random.randint(500,2500)

def gerar_milhas():
    return random.randint(20000,70000)

def distancia_estimada():
    return random.randint(2000,10000)

def verificar():

    for codigo, destino in destinos.items():

        datas_ida = gerar_datas()
        datas_volta = gerar_datas()

        grupos_ida = agrupar_por_mes(datas_ida)
        grupos_volta = agrupar_por_mes(datas_volta)

        for chave in grupos_ida:

            if chave not in grupos_volta:
                continue

            ano, mes = chave

            nome_mes = datetime(ano,mes,1).strftime("%B %Y")

            ida = grupos_ida[chave][:4]
            volta = grupos_volta[chave][:4]

            preco = gerar_preco()
            distancia = distancia_estimada()

            preco_km = round(preco/distancia,2)

            milhas = gerar_milhas()

            mensagem = f"""
{origem_nome} ✈️ {destino}

🗓 Mês: {nome_mes}

🛫 Ida:
"""

            for d in ida:
                mensagem += d.strftime("%d/%m/%Y") + "\n"

            mensagem += "\n🛬 Volta:\n"

            for d in volta:
                mensagem += d.strftime("%d/%m/%Y") + "\n"

            mensagem += f"""

Valor: R$ {preco} (IDA E VOLTA)
Preço por km: {preco_km}

"""

            if milhas <= MILHAS_DISPONIVEIS:

                mensagem += f"""
Milhas necessárias: {milhas}
Programa: Azul Fidelidade
Tipo: Ida e Volta
"""

            mensagem += """

Pesquisar em:

Google Flights
https://www.google.com/travel/flights

ou

Skyscanner
https://www.skyscanner.com
"""

            if preco < 1500 or milhas <= MILHAS_DISPONIVEIS:

                enviar_alerta(mensagem)

def executar():

    print("Iniciando busca de passagens...")

    verificar()

    print("Busca finalizada")

while True:

    executar()

    time.sleep(900)
