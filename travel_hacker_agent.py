import os
import requests
import random
from datetime import datetime, timedelta

# Configurações Telegram
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SALDO_MILHAS = 80979  # Seu saldo Azul Fidelidade

# Função para enviar mensagem no Telegram
def enviar_alerta(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": mensagem})

# Lista de destinos
destinos = [
    "Nova York, EUA",
    "Lisboa, Portugal",
    "Paris, França",
    "Roma, Itália",
    "João Pessoa, PB",
    "Orlando, EUA",
    "Miami, EUA",
    "Barcelona, Espanha",
    "Buenos Aires, Argentina",
    "São Paulo, Brasil"
    # ...adicione os outros destinos da sua lista completa
]

# Funções auxiliares
def gerar_datas_ida_volta():
    hoje = datetime.now()
    datas_ida = []
    datas_volta = []
    for _ in range(3):
        # Gera data de ida futura
        delta_dias_ida = random.randint(1, 180)
        ida = hoje + timedelta(days=delta_dias_ida)
        datas_ida.append(ida)

        # Gera data de volta >= data de ida
        delta_dias_volta = random.randint(1, 14)
        volta = ida + timedelta(days=delta_dias_volta)
        datas_volta.append(volta)
    datas_ida.sort()
    datas_volta.sort()
    return datas_ida, datas_volta

def formatar_datas(datas):
    return ", ".join([d.strftime("%d/%m/%Y") for d in datas])

def gerar_preco():
    return random.randint(750, 4000)

def gerar_milhas():
    return random.randint(20000, 70000)

# Função principal
def verificar_promocoes():
    for destino in destinos:
        datas_ida, datas_volta = gerar_datas_ida_volta()
        preco = gerar_preco()
        milhas_necessarias = gerar_milhas()

        mensagem_base = f"RIO DE JANEIRO ✈️ {destino}\n\n"

        # Promoção em dinheiro (IDA e VOLTA)
        if preco < 4000:
            mensagem_dinheiro = mensagem_base
            mensagem_dinheiro += f"🛫 Ida: {formatar_datas(datas_ida)}\n"
            mensagem_dinheiro += f"🛬 Volta: {formatar_datas(datas_volta)}\n"
            mensagem_dinheiro += f"Valor: R$ {preco} (IDA E VOLTA)\n"
            mensagem_dinheiro += "Pesquisar em:\nGoogle Flights\nhttps://www.google.com/travel/flights\nou\nSkyscanner\nhttps://www.skyscanner.com\n"
            enviar_alerta(mensagem_dinheiro)

        # Promoção em milhas (IDA ou IDA e VOLTA se possível)
        if milhas_necessarias <= SALDO_MILHAS:
            mensagem_milhas = mensagem_base
            mensagem_milhas += f"🛫 Ida: {datas_ida[0].strftime('%d/%m/%Y')}\n"
            mensagem_milhas += f"🛬 Volta: {datas_volta[0].strftime('%d/%m/%Y')}\n"
            mensagem_milhas += f"Milhas necessárias: {milhas_necessarias}\n"
            mensagem_milhas += "Programa: Azul Fidelidade\n"
            mensagem_milhas += "Tipo: IDA E VOLTA\n"
            mensagem_milhas += "Pesquisar em:\nhttps://www.voeazul.com.br\n"
            enviar_alerta(mensagem_milhas)

# Executar o agente
if __name__ == "__main__":
    verificar_promocoes()
    print("Verificação concluída ✅")
