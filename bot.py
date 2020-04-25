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

import time
import telebot
from flask import Flask, request
import os
TOKEN = "1051111158:AAFvK-O_b3OYY_9yG90i3etabjl_-xBGOVE"
#lista_usuarios recoge todos los usuarios registrados
lista_usuarios = ""
datos_usuarios = []
bot = telebot.TeleBot(TOKEN)
vector_meses =['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
paso0 = []
paso1 = []
paso2 = []
paso3 = []
paso4 = []
def compruebatelefono(numero):
    comp1 = numero.isdigit()
    if comp1 == True:
        numero = int(numero)
        if numero > 600000000 and numero < 800000000:
            return True
        else:
            return False
    else:
        return False
def compruebaedad(edad):
    comp1 = edad.isdigit()
    if comp1 == True:
        edad = int(edad)
        if edad > 1900 and edad < 2002:
            return True
        else:
            return False
    else:
        return False
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
@bot.message_handler(func=lambda message: True)#Aqui­ hacemos el primer listado de pregunta-respuesta. Podemos hacer asi­ los que hagan falta
def echo_all(message):
    bloqueo = False#Este bloqueo hará que solo entremos a un bloque por interacción
    chatid = message.chat.id #id personal de cada usuario
    chatod = str(chatid)
    a=message.text
    if chatod not in lista_usuarios:
        
        if a == 'Comenzar mi registro ✔️' and chatod in paso0 and bloqueo == False:
            bloqueo = True
            bot.send_message(chatid, "Para poder ponerte en contacto con los otros viajeros, necesito que me des un número de teléfono con el que puedan localizarte")
            bot.send_message(chatid, "Por favor, indícame tu número de teléfono")
            paso0.remove(chatod)
            paso1.append(chatod)
   
        if chatod in paso1 and bloqueo == False:
            bloqueo = True
            comprueba_numero = compruebatelefono(a)
            if comprueba_numero == True:
                bot.send_message(chatid, "El número introducido es el "+a+"")
                markup=types.ReplyKeyboardMarkup()
                markup.row('Sí, es correcto! 😁')     
                markup.row('No, me he equivocado 😅') 
                bot.send_message(chatid, "¿Es correcto?", None, None, markup)
                paso1.remove(chatod)
                paso2.append(chatod)
            else:
                bot.send_message(chatid, "El número introducido es incorrecto...☹️ Por favor, introduce un número valido")

        if chatod in paso2 and bloqueo == False:
            bloqueo = True
            if a == 'Sí, es correcto! 😁':
                bot.send_message(chatid, "Genial! Me gustaría por último conocer tu fecha de nacimiento, así las personas que compartan coche podrán tener más información sobre tí")
                markup=types.ReplyKeyboardMarkup()
                markup.row('1','2','3','4','5','6','7','8')     
                markup.row('9','10','11','12','13','14','15','16')
                markup.row('17','18','19','20','21','22','23','24')     
                markup.row('25','26','27','28','29','30','31')
                bot.send_message(chatid, "Indica el día de tu fecha de nacimiento", None, None, markup)
                datos_usuarios.append(chatid)
                datos_usuarios.append(a)
                paso2.remove(chatod)
                paso3.append(chatod)                
            elif a == 'No, me he equivocado 😅':
                bot.send_message(chatid, "No te preocupes, no pasa nada. Vuelve a indicarme el número de teléfono")
                paso1.append(chatod)
                paso2.remove(chatod)
            else:
                bot.send_message(chatid, "Lo siento, no te he entendido ☹️")
                markup=types.ReplyKeyboardMarkup()
                markup.row('Sí, es correcto! 😁')     
                markup.row('No, me he equivocado 😅') 
                bot.send_message(chatid, "¿Es correcto el número que has introducido?", None, None, markup)                

        if chatod in paso3 and bloqueo == False:
            bloqueo = True
            markup=types.ReplyKeyboardMarkup()
            markup.row('Enero','Febrero','Marzo','Abril')
            markup.row('Mayo','Junio','Julio','Agosto')
            markup.row('Septiembre','Octubre','Noviembre','Diciembre')
            bot.send_message(chatid, "Ahora indícame el mes", None, None, markup)   
            if a in vector_meses:
                bot.send_message(chatid, "Genial, solo me queda saber en que año naciste")
                paso3.remove(chatod)
                paso4.append(chatod)
                pos = datos_usuarios.index(chatod)
                datos_usuarios[pos+2] = a
        if chatod in paso4 and bloqueo == False:
            bloqueo = True
            comprueba_edad = compruebaedad(a)
            if comprueba_edad == True:
                markup=types.ReplyKeyboardMarkup()
                markup.row('Publicar un viaje 🚘','Buscar un viaje 🔎')     
                markup.row('Ver mis viajes activos ⏲️','Cambiar mis datos 📝') 
                bot.send_message(chatid, "¡Enhorabuena! Ya formas parte de nuestra gran comunidad 🎉", None, None, markup)    
                bot.send_message(chatid, "A partir de ahora podrás compartir viajes sin pagar ninguna comisión 💶")
                pos = datos_usuarios.index(chatod)
                datos_usuarios[pos+3] = a
                lista_usuarios.append(chatod)
                markup=types.ReplyKeyboardMarkup()
 
                
print("El bot se esta ejecutando")
try:
        bot.infinity_polling(True)
except Exception as err:
        logger.error(err)
        time.sleep(5)
        print("Error de internet")

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://conamm.herokuapp.com/' + TOKEN)
    return "!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

"""
print(browser.find_element_by_name("quantityBox"))
print(browser.context)
browser.close()
"""
        