import os
import requests
import random
from datetime import datetime, timedelta

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def enviar_alerta(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": mensagem})

# Origem fixa
origem = "RIO DE JANEIRO"

# Lista de destinos (exemplo reduzido, inclua todos que você mencionou)
destinos = [
    "LISBOA", "PARIS", "ROMA", "NOVA YORK", "MIAMI", "ORLANDO", "JOÃO PESSOA", "SALVADOR", "RECIFE"
]

# Simula preços e datas
def gerar_voos():
    voos = {}
    hoje = datetime.now()
    ano_atual = hoje.year
    ano_prox = ano_atual + 1

    for destino in destinos:
        voos_destino = []

        # Simula entre 1 e 3 meses de viagens
        for _ in range(random.randint(1,3)):
            mes_ida = random.randint(1,12)
            ano_ida = random.choice([ano_atual, ano_prox])

            # Gerar datas de ida (3 opções)
            datas_ida = sorted([hoje + timedelta(days=random.randint(30, 365)) for _ in range(3)])
            datas_ida = [d for d in datas_ida if d > hoje and d.month == mes_ida]

            # Gerar datas de volta (3 opções) sempre depois da menor ida
            if datas_ida:
                menor_ida = min(datas_ida)
                datas_volta = sorted([menor_ida + timedelta(days=random.randint(1,30)) for _ in range(3)])
            else:
                datas_volta = []

            preco = random.randint(700,1500)
            preco_km = round(preco / random.randint(4000,10000), 2)
            milhas = random.randint(20000,70000)

            voos_destino.append({
                "mes": datas_ida[0].strftime("%B") if datas_ida else "Indefinido",
                "ano": ano_ida,
                "ida": [d.strftime("%d/%m/%Y") for d in datas_ida],
                "volta": [d.strftime("%d/%m/%Y") for d in datas_volta],
                "preco": preco,
                "preco_km": preco_km,
                "milhas": milhas
            })
        voos[destino] = voos_destino
    return voos

def formatar_mensagem(voos):
    for destino, lista_voos in voos.items():
        for voo in lista_voos:
            mensagem = f"{origem} ✈️ {destino}\n\n"
            mensagem += f"🗓 Mês: {voo['mes']} {voo['ano']}\n\n"
            if voo['ida']:
                mensagem += "🛫 Ida:\n" + "\n".join(voo['ida']) + "\n\n"
            if voo['volta']:
                mensagem += "🛬 Volta:\n" + "\n".join(voo['volta']) + "\n\n"

            if voo['preco'] <= 1500:
                mensagem += f"Valor: R$ {voo['preco']} (IDA E VOLTA)\n"
                mensagem += f"Preço por km: {voo['preco_km']}\n\n"

            if voo['milhas'] <= 80979:  # sua quantidade atual de pontos
                mensagem += f"Milhas necessárias: {voo['milhas']}\n"
                mensagem += "Programa: Azul Fidelidade\n"
                mensagem += "Tipo: Ida e Volta\n\n"

            mensagem += "Pesquisar em:\nGoogle Flights\nhttps://www.google.com/travel/flights\n\nou\nSkyscanner\nhttps://www.skyscanner.com"

            enviar_alerta(mensagem)

# Loop principal
if __name__ == "__main__":
    while True:
        voos = gerar_voos()
        formatar_mensagem(voos)
        print("Verificação concluída")
        # 15 minutos
        import time
        time.sleep(900)
