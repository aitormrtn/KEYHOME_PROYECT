# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 02:56:28 2020

@author: Usuario

http://www.tuxrincon.com/blog/python-multihilo-ejemplos/

PARA CAMBIAR A WEBHOOK (Nos busca Telegram)
https://api.telegram.org/bot1139484979:AAEoxMedvhtQPof_AFa55Exob55yCqFqTW4/setWebHook?url=https://conamm.herokuapp.com/

SI QUEREMOS CAMBIAR A POLLING (NOSOTROS LEEMOS LA BANDEJA DE TELEGRAM)
https://api.telegram.org/bot1051111158:AAFvK-O_b3OYY_9yG90i3etabjl_-xBGOVE/setWebHook?url=

"""
# bot.py
import requests  
import os
from flask import Flask, request
# Add your telegram token as environment variable
BOT_URL = f'https://api.telegram.org/bot{os.environ["1139484979:AAEoxMedvhtQPof_AFa55Exob55yCqFqTW4"]}/'


app = Flask(__name__)


@app.route('/', methods=['POST'])
def main():  
    data = request.json

    print(data)  # Comment to hide what Telegram is sending you
    chat_id = data['message']['chat']['id']
    message = data['message']['text']

    json_data = {
        "chat_id": chat_id,
        "text": message,
    }

    message_url = BOT_URL + 'sendMessage'
    requests.post(message_url, json=json_data)

    return ''


if __name__ == '__main__':  
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
    
    
"""
print(browser.find_element_by_name("quantityBox"))
print(browser.context)
browser.close()
"""
        