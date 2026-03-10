import os
import requests
import random
from datetime import datetime, timedelta

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Função para enviar mensagem no Telegram
def enviar_alerta(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": mensagem})


# Lista de destinos (resumida aqui, mas você pode incluir todos da sua lista)
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

# Funções auxiliares para gerar datas e preços simulados
def gerar_datas_ida_volta():
    hoje = datetime.now()
    ano_atual = hoje.year
    ano_proximo = ano_atual + 1

    # Gera 3 datas de ida e 3 datas de volta por mês, garantindo consistência
    datas_ida = []
    datas_volta = []
    for _ in range(3):
        dia_ida = random.randint(1, 28)
        mes_ida = random.randint(hoje.month, 12)
        ano_ida = ano_atual if mes_ida >= hoje.month else ano_proximo
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

def gerar_preco():
    return random.randint(750, 4000)

def gerar_milhas():
    return random.randint(20000, 70000)

# Função principal do agente
def verificar_promocoes():
    for destino in destinos:
        datas_ida, datas_volta = gerar_datas_ida_volta()
        preco = gerar_preco()
        preco_km = round(preco / random.randint(4000, 12000), 2)
        milhas_necessarias = gerar_milhas()

        mensagem = f"RIO DE JANEIRO ✈️ {destino}\n\n"

        # Caso seja promoção em dinheiro
        if preco < 1500:
            mensagem += f"🛫 Ida:\n{formatar_datas(datas_ida)}\n"
            mensagem += f"🛬 Volta:\n{formatar_datas(datas_volta)}\n\n"
            mensagem += f"Valor: R$ {preco} (IDA E VOLTA)\n"
            mensagem += f"Preço por km: {preco_km}\n\n"
            mensagem += "Pesquisar em:\nGoogle Flights\nhttps://www.google.com/travel/flights\nou\nSkyscanner\nhttps://www.skyscanner.com\n"
            enviar_alerta(mensagem)

        # Caso seja promoção em milhas (IDA somente)
        if milhas_necessarias <= 80979:
            mensagem_milhas = f"RIO DE JANEIRO ✈️ {destino}\n\n"
            mensagem_milhas += f"🛫 Ida:\n{formatar_datas([datas_ida[0]])}\n"
            mensagem_milhas += f"Milhas necessárias: {milhas_necessarias}\n"
            mensagem_milhas += "Programa: Azul Fidelidade\n"
            mensagem_milhas += "Tipo: Somente IDA\n\n"
            mensagem_milhas += "Pesquisar em:\nhttps://www.voeazul.com.br\n"
            enviar_alerta(mensagem_milhas)

# Rodar o agente uma vez
verificar_promocoes()
print("Verificação concluída")
