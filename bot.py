# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 02:56:28 2020

@author: Usuario

http://www.tuxrincon.com/blog/python-multihilo-ejemplos/

PARA CAMBIAR A WEBHOOK (Nos busca Telegram)
https://api.telegram.org/bot1051111158:AAFvK-O_b3OYY_9yG90i3etabjl_-xBGOVE/setWebHook?url=https://conamm.herokuapp.com/

SI QUEREMOS CAMBIAR A POLLING (NOSOTROS LEEMOS LA BANDEJA DE TELEGRAM)
https://api.telegram.org/bot<BOT_TOKEN>/setWebHook?url=

"""

import time
import telebot
from flask import Flask, request
import os

TOKEN = '1051111158:AAFvK-O_b3OYY_9yG90i3etabjl_-xBGOVE'
bot = telebot.TeleBot(token=TOKEN)
server = Flask(__name__)

@bot.message_handler(commands=['start'])
def send_info(message):
   text = (
   "<b>Welcome to the Medium 🤖!</b>\n"
   "Say Hello to the bot to get a reply from it!"
   )
   bot.send_message(message.chat.id, text, parse_mode='HTML')

@bot.message_handler(func=lambda msg: msg.text is not None)
def reply_to_message(message):
   if 'hello'in message.text.lower():
      sendMessage(message, 'Hello! How are you doing today?')
      
@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
   bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
   return "!", 200@server.route("/")
def webhook():
   bot.remove_webhook()
   bot.set_webhook(url='https://conamm.herokuapp.com/' + TOKEN)
   return "!", 200
if __name__ == "__main__":
   server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))