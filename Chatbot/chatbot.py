from supbot import Supbot
from estrutura import aimlbot

bot = aimlbot()


def message_received(contact_name: str, message: str):
    resposta = bot.response(message)
    if type(resposta) == list:
        resposta = resposta[::-1]
        for x in resposta:
            supbot.send_message(contact_name,x)
    else:
        supbot.send_message(contact_name,resposta)
    

with Supbot(message_received=message_received) as supbot:
    supbot.wait_for_finish()