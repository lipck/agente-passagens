import os
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import schedule
import time
from bs4 import BeautifulSoup

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Função para enviar alertas no Telegram
def enviar_alerta(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": mensagem})

# Base de aeroportos (exemplo simplificado, expandir para 3.000)
aeroportos = pd.DataFrame({
    "codigo": ["GIG","SDU","JFK","MIA","LHR","CDG","LIS","SCL","EZE","ORL","MCO","BUE","MAD","BCN","FRA"],
    "cidade": ["Rio de Janeiro","Rio de Janeiro","Nova York","Miami","Londres","Paris","Lisboa","Santiago","Buenos Aires","Orlando","Orlando","Buenos Aires","Madrid","Barcelona","Frankfurt"],
    "pais": ["Brasil"]*2 + ["EUA","EUA","Reino Unido","França","Portugal","Chile","Argentina","EUA","EUA","Argentina","Espanha","Espanha","Alemanha"]
})

# Gerar rotas automaticamente (origem = RJ)
origem = "RIO DE JANEIRO"
rotas = aeroportos[aeroportos['cidade'] != origem].head(200) # até 200 rotas

# Saldo de milhas
MILHAS_DISPONIVEIS = 80979

# Funções auxiliares
def gerar_datas_ida_volta():
    hoje = datetime.now()
    datas_ida = []
    datas_volta = []
    for _ in range(3):
        dia_ida = random.randint(hoje.day, 28)
        mes_ida = random.randint(hoje.month, 12)
        ano_ida = hoje.year if mes_ida >= hoje.month else hoje.year + 1
        ida = datetime(ano_ida, mes_ida, dia_ida)
        if ida < hoje:
            ida += timedelta(days=30)
        datas_ida.append(ida)

    datas_ida.sort()
    for ida in datas_ida:
        dia_volta = random.randint(ida.day + 1, ida.day + 10)
        mes_volta = ida.month
        ano_volta = ida.year
        if dia_volta > 28:
            dia_volta -= 5
        volta = datetime(ano_volta, mes_volta, dia_volta)
        datas_volta.append(volta)
    datas_volta.sort()
    return datas_ida, datas_volta

def formatar_datas(datas):
    return "\n".join([d.strftime("%d/%m/%Y") for d in datas])

def buscar_precos(destino_codigo):
    """
    Função simulada que retorna preços e milhas.
    Na versão real, você integraria com Google Flights / Skyscanner / Azul
    """
    preco = random.randint(750, 4000)
    preco_km = round(preco / random.randint(4000,12000), 2)
    milhas_necessarias = random.randint(20000, 70000)
    return preco, preco_km, milhas_necessarias

# Função principal do agente
def monitorar_rotas():
    for idx, rota in rotas.iterrows():
        destino = rota['cidade'] + ", " + rota['pais']
        datas_ida, datas_volta = gerar_datas_ida_volta()
        preco, preco_km, milhas_necessarias = buscar_precos(rota['codigo'])

        # Mensagem para passagem em dinheiro
        if preco < 1500:
            msg = f"RIO DE JANEIRO ✈️ {destino}\n\n"
            msg += f"🛫 Ida:\n{formatar_datas(datas_ida)}\n"
            msg += f"🛬 Volta:\n{formatar_datas(datas_volta)}\n\n"
            msg += f"Valor: R$ {preco} (IDA E VOLTA)\n"
            msg += f"Preço por km: {preco_km}\n\n"
            msg += "Pesquisar em:\nGoogle Flights\nhttps://www.google.com/travel/flights\nou\nSkyscanner\nhttps://www.skyscanner.com"
            enviar_alerta(msg)

        # Mensagem para passagem em milhas (apenas se couber no saldo)
        if milhas_necessarias <= MILHAS_DISPONIVEIS:
            msg_milhas = f"RIO DE JANEIRO ✈️ {destino}\n\n"
            msg_milhas += f"🛫 Ida:\n{formatar_datas([datas_ida[0]])}\n"
            msg_milhas += f"Milhas necessárias: {milhas_necessarias}\n"
            msg_milhas += "Programa: Azul Fidelidade\nTipo: Somente IDA\n\n"
            msg_milhas += "Pesquisar em:\nhttps://www.voeazul.com.br"
            enviar_alerta(msg_milhas)

# Rodar o agente a cada 15 minutos usando schedule
schedule.every(15).minutes.do(monitorar_rotas)

print("🚀 Travel Hacker PRO iniciado!")
monitorar_rotas()  # primeira execução imediata

while True:
    schedule.run_pending()
    time.sleep(10)
