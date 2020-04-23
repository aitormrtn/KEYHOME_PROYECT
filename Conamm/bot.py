# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 02:56:28 2020

@author: Usuario

http://www.tuxrincon.com/blog/python-multihilo-ejemplos/

PARA CAMBIAR A WEBHOOK (Nos busca Telegram)
https://api.telegram.org/bot1051111158:AAFvK-O_b3OYY_9yG90i3etabjl_-xBGOVE/setWebHook?url=https://git.heroku.com/conamm.git

SI QUEREMOS CAMBIAR A POLLING (NOSOTROS LEEMOS LA BANDEJA DE TELEGRAM)
https://api.telegram.org/bot1051111158:AAFvK-O_b3OYY_9yG90i3etabjl_-xBGOVE/setWebHook?url=

"""
bot = telebot.TeleBot('1051111158:AAFvK-O_b3OYY_9yG90i3etabjl_-xBGOVE')
import telebot
@bot.message_handler(commands=["start","help"])
def send_welcome(message):
    
    chatid = message.chat.id #id personal de cada usuario
    chatod = str(chatid)
    nombreUsuario = message.chat.first_name #nombre de usuario
    print(str(message))
    if chatod not in lista_usuarios:
        saludo = "Hola {nombre}, soy Concabot, tu asistente de viaje, y estoy encantado de conocerte 😀"
        bot.send_message(chatid, saludo.format(nombre=nombreUsuario))
        markup=types.ReplyKeyboardMarkup()
        markup.row('Comenzar mi registro ✔️')
        bot.send_message(chatid, "Conmigo no volverás a pagar nunca más por compartir coche, pero antes de empezar, me gustaría conocerte un poco 😊", None, None, markup)
        paso0.append(chatod)
    else:
        bot.send_message(chatid, "Hola {nombre}! No sabes cuanto me alegra volverte a ver por aquí. 😃")
        bot.send_message(chatid, "¿En qué puedo ayudarte?")  

try:
        bot.infinity_polling(True)
except Exception as err:
        logger.error(err)
        time.sleep(5)
        print("Error de internet")