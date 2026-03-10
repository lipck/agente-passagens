import os
import requests
import random
import time

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


origem = "RIO DE JANEIRO"

destinos = [
"JOÃO PESSOA",
"MIAMI",
"ORLANDO",
"PARIS",
"ROMA",
"MADRI",
"LISBOA",
"SANTIAGO",
"BUENOS AIRES"
]


meses = {
"Março": list(range(1,31)),
"Abril": list(range(1,31)),
"Maio": list(range(1,31))
}


def gerar_datas():

    ida = random.sample(range(1,30), random.randint(3,8))
    volta = random.sample(range(1,30), random.randint(3,8))

    ida.sort()
    volta.sort()

    return ida, volta


def formatar_lista(lista):

    return ", ".join(str(x) for x in lista)


def verificar_promocoes():

    for destino in destinos:

        preco = random.randint(700,1500)

        milhas = random.randint(25000,70000)

        mensagem = f"{origem} ✈️ {destino}\n\n"

        for mes in meses:

            ida, volta = gerar_datas()

            mensagem += f"🗓 Mês de {mes}\n\n"
            mensagem += f"🛫 Ida: {formatar_lista(ida)}\n"

            if random.choice([True, False]):
                mensagem += f"🛬 Volta: {formatar_lista(volta)}\n"

            mensagem += "\n"

        if random.choice([True, False]):

            mensagem += f"Valor: R$ {preco} (IDA E VOLTA)\n\n"

        else:

            mensagem += f"Milhas necessárias: {milhas}\n"
            mensagem += "Programa: Azul Fidelidade\n\n"

        mensagem += "Encontrar passagem em:\n\n"

        mensagem += "Google Flights\n"
        mensagem += "https://www.google.com/travel/flights\n\n"

        mensagem += "ou\n\n"

        mensagem += "Skyscanner\n"
        mensagem += "https://www.skyscanner.com\n"

        enviar_alerta(mensagem)


while True:

    verificar_promocoes()

    print("Verificação concluída")

    time.sleep(900)
