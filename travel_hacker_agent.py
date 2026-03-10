import os
import requests
import random
from datetime import datetime, timedelta

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Função para enviar mensagens no Telegram
def enviar_alerta(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": mensagem})

# Lista de origens (somente Brasil)
origens = [
    "RIO DE JANEIRO", "SÃO PAULO", "BRASÍLIA", "BELO HORIZONTE", 
    "PORTO ALEGRE", "CURITIBA", "SALVADOR", "RECIFE", "FORTALEZA",
    "MANAUS", "BELÉM", "GOIÂNIA", "VITÓRIA", "NATAL"
]

# Lista de destinos (nacional + internacional)
destinos = [
    "JOÃO PESSOA", "MACEIÓ", "ORLANDO", "MIAMI", "LISBOA", "PARIS", 
    "ROMA", "BARCELONA", "MADRI", "NOVA YORK", "LOS ANGELES", "SAN FRANCISCO",
    "LAS VEGAS", "CHICAGO", "VANCOUVER", "TORONTO", "MONTREAL", "CANCÚN",
    "CIDADE DO MÉXICO", "SAN JOSÉ", "PUNTA CANA", "HAVANA", "SAN JUAN",
    "BELIZE CITY", "KINGSTON", "BUENOS AIRES", "SANTIAGO", "CARTAGENA",
    "MEDLLÍN", "QUITO", "MONTEVIDÉU", "LONDRES", "AMSTERDÃ", "VIEENA",
    "BERLIM", "DUBAI", "SYDNEY", "MELBOURNE", "AUCKLAND", "QUEENSTOWN"
    # Adicione todos os destinos da sua lista conforme necessário
]

# Função para gerar datas simuladas (somente a partir de hoje)
def gerar_datas():
    hoje = datetime.now()
    # gerar mês e ano aleatório do mês atual ou posterior
    mes = random.randint(hoje.month, 12)
    ano = hoje.year if mes >= hoje.month else hoje.year + 1
    # gerar datas de ida
    ida = sorted([(hoje + timedelta(days=random.randint(1, 365))).strftime("%d/%m/%Y") for _ in range(random.randint(2,5))])
    volta = sorted([(hoje + timedelta(days=random.randint(1, 365))).strftime("%d/%m/%Y") for _ in range(random.randint(2,5))])
    return mes, ano, ida, volta

# Função para gerar preço aleatório
def gerar_preco():
    return random.randint(750, 4000)

# Função para gerar milhas simuladas
def gerar_milhas():
    return random.randint(20000, 80000)

# Função principal para simular promoções
def verificar_promocoes():
    for origem in origens:
        for destino in destinos:
            mes, ano, datas_ida, datas_volta = gerar_datas()

            # Simulação preço
            preco = gerar_preco()
            distancia = random.randint(4000, 12000)
            preco_km = round(preco/distancia, 2)

            # Formatar mensagem de preço
            msg = f"{origem} ✈️ {destino}\n\n"
            msg += f"🗓 Mês: {datetime(ano, mes, 1).strftime('%B %Y')}\n\n"
            msg += "🛫 Ida:\n" + "\n".join(datas_ida) + "\n\n"
            msg += "🛬 Volta:\n" + "\n".join(datas_volta) + "\n\n"
            msg += f"Valor: R$ {preco} (IDA E VOLTA)\nPreço por km: {preco_km}\n\n"
            msg += "Google Flights\nhttps://www.google.com/travel/flights\n\nou\n\n"
            msg += "Skyscanner\nhttps://www.skyscanner.com\n"

            enviar_alerta(msg)

            # Simulação milhas (apenas se dentro do saldo)
            milhas = gerar_milhas()
            if milhas <= 80979:  # seu saldo atual
                msg_milhas = f"{origem} ✈️ {destino}\n\n"
                msg_milhas += f"🗓 Mês: {datetime(ano, mes, 1).strftime('%B %Y')}\n\n"
                msg_milhas += "🛫 Ida:\n" + "\n".join(datas_ida) + "\n\n"
                msg_milhas += "🛬 Volta:\n" + "\n".join(datas_volta) + "\n\n"
                msg_milhas += f"Milhas necessárias: {milhas}\nPrograma: Azul Fidelidade\nTipo: Ida e Volta\n\n"
                msg_milhas += "https://www.voeazul.com.br\n"

                enviar_alerta(msg_milhas)

# Rodar o agente uma vez (GitHub Actions irá rodar a cada 15 minutos via cron)
verificar_promocoes()
print("Verificação concluída")
