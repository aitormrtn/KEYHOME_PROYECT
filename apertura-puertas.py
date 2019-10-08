

# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 09:48:05 2019

@author: Aitor Martín
"""
#import RPi.GPIO as GPIO
import time
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(18, GPIO.OUT) ## GPIO 18 como salida
import telebot
from telebot import types
import unidecode
import random
from datetime import datetime, date, time, timedelta
import calendar
fechasiniciales=[]
fechasfinales=[]
contraseñas=[]
fechainiciousuario=[]
fechafinalusuario=[]
caracteres="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"#62 Carñacteres posibles para las contraseñas
fechas = str(datetime.now())
año = int(fechas[0:4])
mes = int(fechas[5:7])
dia = int(fechas[8:10])
def compruebaentero(dato):#Esta función comprueba que un número es entero
    numeros="0123456789"
    comprobar = True
    tam = 0
    tam = len(dato)
    j=0
    for i in range (tam):
        if dato[i] not in numeros:
            comprobar = False
            j+=1
    if comprobar == True:
        return True
    else:
        return False
def generapass():#Esta función genera una contraseña de n dígitos
    n = 12
    password=""
    for i in range(n):#Creamos una pass de 12 digitos
        digito = random.randrange(62)
        password=password+caracteres[digito]
    return password
def comprobarfecha(fechainic):#Esta función comprueba que una petición se produce después de la fecha mínima
    fechas = str(datetime.now())
    año = int(fechas[0:4])
    mes = int(fechas[5:7])
    dia = int(fechas[8:10])
    hora = int(fechas[11:13])
    añop = int(fechainic[0:4])
    mesp = int(fechainic[5:7])
    diap = int(fechainic[8:10])
    if añop == año and mesp == mes and diap == dia:"""En caso de que sea justo el dia de llegada, habrá que tener en cuenta
                                                    que deberán ser al menos las 12 para poder pasar"""
        if hora >= 12:
            return True
        else:
            return False   
    elif año > añop:
        return True
    elif año == añop and mes > mesp:
        return True
    elif año == añop and mes == mesp and dia >= diap:
        return True
    else:
        return False
def comprobarfechamaxima(fechafin):#Esta función comprueba que una petición se produce antes de la fecha máxima
    fechas = str(datetime.now())
    año = int(fechas[0:4])
    mes = int(fechas[5:7])
    dia = int(fechas[8:10])
    hora = int(fechas[11:13])
    añop = int(fechafin[0:4])
    mesp = int(fechafin[5:7])
    diap = int(fechafin[8:10])
   
    if añop == año and mesp == mes and diap == dia:"""En caso de que sea justo el dia de salida, habrá que tener en cuenta
                                                    que a partir de las 15h ya no se puede pasar"""
        if hora < 15:
            return True
        else:
            return False
    elif añop > año:
        return True
    elif añop == año and mesp > mes:
        return True
    elif añop == año and mesp == mes and diap >= dia:
        return True
    else:
        return False
def comprobarfechaintroducida(fechapalabra):#Comprobamos que han escrito la fecha de manera correcta
    numeros=["0","1","2","3","4","5","6","7","8","9"]
    if len(fechapalabra)==10:
        if fechapalabra[0] in numeros and fechapalabra[1] in numeros and fechapalabra[2] in numeros and fechapalabra[3] in numeros and fechapalabra[5] in numeros and fechapalabra[6] in numeros and fechapalabra[8] in numeros and fechapalabra[9] in numeros:
            return True
        else:
            return False
    else:
        return False
bot = telebot.TeleBot('899647686:AAEcscuaVaC6FrzS8bUzN1EZrWn7RzlQ1LU')
#899647686:AAEcscuaVaC6FrzS8bUzN1EZrWn7RzlQ1LU
usuariosactivos=[]#Creamos un vector dónde almacenaremos los usuarios activos
administradores=[]
paso1=False
paso2=False
paso3=False
"""
def blink():#Esta función nos enciende el led el tiempo que deseemos
        GPIO.setmode(GPIO.BCM)
        print ("Ejecucion iniciada...")
        iteracion = 0
        while iteracion < 1: ## Segundos que durará la función
                GPIO.output(18, True) ## Enciendo el 18
                time.sleep(5) ## Esperamos 1 segundo
                iteracion = iteracion + 2 ## Sumo 2 para salir del bucle
        print ("Ejecucion finalizada")
        GPIO.output(18, False) ## Apago el 18
"""        
@bot.message_handler(commands=["start","help"])
def send_welcome(message):
    
    chatid = message.chat.id #id personal de cada usuario
    nombreUsuario = message.chat.first_name #nombre de usuario
    nombreUsuario = unidecode.unidecode(nombreUsuario)#Le quitamos los acentos al nombre de usuario para que no nos de problemas
    saludo = "Hola {nombre}, bienvenido a KeyHome! Ya estás un paso más cerca de acceder a tu vivienda! Por favor, necesito que me indiques el código que te enviamos al teléfono:"
    bot.send_message(chatid, saludo.format(nombre=nombreUsuario))
    
@bot.message_handler(func=lambda message: True)#Aqui­ hacemos el primer listado de pregunta-respuesta. Podemos hacer asi­ los que hagan falta
def echo_all(message):
    chatid = message.chat.id
    chatod = str(chatid)#Convertimos la id de usuario a String
    a=message.text#Aqui­ recibimos el mensaje
    global paso1, paso2, paso3, fechaentrada, fechasalida, nuevapass, fechainiciousuario, fechafinalusuario
    
    if a == "x8$fG1Z*v9Y?k":#Esta sería la contraseña de administrador.
        mensajetipo="Ahora eres administrador de esta vivienda"
        markup=types.ReplyKeyboardMarkup()
        markup.row('Nueva reserva','Abrir puerta')
        markup.row('Dejar de ser administrador','Ver reservas activas')
        bot.send_message(chatod, mensajetipo, None, None, markup)
        if chatod not in administradores:            
            administradores.append(chatod)
    elif chatod in administradores:
        if a == "Nueva reserva":
            bot.send_message(chatod, "Por favor, indique la fecha inicial para los clientes:")
            bot.send_message(chatod, "Ejemplo: 2019-06-25")
            paso1=True
        elif paso1 == True:
            if paso2 == True or paso1 == True or paso3 == True:
                paso1 = False
                paso2 = False
                paso3 = False
            comprobar=comprobarfechaintroducida(a)
            if comprobar == True:
                bot.send_message(chatod, "Ahora introduzca la fecha final:")
                bot.send_message(chatod, "Ejemplo: 2019-06-28")
                fechaentrada=a
                paso2=True
            else:
                markup=types.ReplyKeyboardMarkup()
                markup.row('Nueva reserva','Abrir puerta')
                markup.row('Dejar de ser administrador','Ver reservas activas')
                bot.send_message(chatod, "La fecha introducida no es correcta, por favor, vuelve a comenzar", None, None, markup)
                paso1=False
        elif paso2==True:
            if paso2 == True or paso1 == True or paso3 == True:
                paso1 = False
                paso2 = False
                paso3 = False
            comprobar=comprobarfechaintroducida(a)
            if comprobar == True:
                nuevapass=generapass()
                fechasalida=a
                bot.send_message(chatod, "Genial, se ha creado una nueva entrada. Los clientes podrán acceder a la vivienda desde la fecha "+fechaentrada+" hasta la fecha "+fechasalida+". \nPara acceder, sus clientes deberán introducir una única vez la contraseña que se muestra a continuación")
                bot.send_message(chatod, nuevapass)
                fechasiniciales.append(fechaentrada)
                fechasfinales.append(fechasalida)
                contraseñas.append(nuevapass)
                
            else:
                bot.send_message(chatod, "La fecha introducida no es correcta, por favor, vuelve a empezar")
                paso2=False
        
            
        elif a == "Abrir puerta":
            if paso2 == True or paso1 == True or paso3 == True:
                paso1 = False
                paso2 = False
                paso3 = False
            bot.send_message(chatod, "Abriendo puerta...")
            #blink()
        elif a == "Dejar de ser administrador":
            if paso2 == True or paso1 == True or paso3 == True:
                paso1 = False
                paso2 = False
                paso3 = False
            administradores.remove(chatod)
            bot.send_message(chatod, "Ya no tienes permisos de administrador")
        elif a == "Ver reservas activas":
            if paso2 == True or paso1 == True or paso3 == True:
                paso1 = False
                paso2 = False
                
            reservas = ""
            tam = int(len(contraseñas))
            paso3 = True
            if tam > 0:
                for i in range(tam):
                    j=i+1
                    reservas = reservas + (""+str(j)+". Reserva desde "+fechasiniciales[i]+" hasta "+fechasfinales[i]+" con la contraseña de acceso: "+contraseñas[i]+"\n")
                bot.send_message(chatod, reservas)
                bot.send_message(chatod, "Si quieres eliminar alguna reserva, simplemente escribe el número que deseas eliminar")

            else:
                bot.send_message(chatod, "No hay reservas activas")
        elif paso3 == True:
            paso3 == False
            comprueba = compruebaentero(a)
            cantidad = len(contraseñas)
            if comprueba == True:
                if cantidad >= int(a):
                    a = int(a)
                    a = a - 1
                    fechasiniciales.pop(a)
                    fechasfinales.pop(a)
                    contraseñas.pop(a)
                    a=a+1
                    bot.send_message(chatod, "Se ha borrado la reserva "+str(a))
                else:
                    bot.send_message(chatod, "El número no corresponde a ninguna reserva")
            else:
                bot.send_message(chatod, "Lo siento, pero no entiendo el mensaje")
        else:
            bot.send_message(chatod, "No entiendo el mensaje")
    else:
        if paso3 == True or paso2 == True or paso1 == True:
            paso3 = False
            paso2 = False
            paso1 = False
        if chatod in usuariosactivos:
            posicion = int(usuariosactivos.index(chatod))
            fechamax = fechafinalusuario[posicion]
            comprobar = comprobarfechamaxima(fechamax)
            if comprobar == False:
                usuariosactivos.remove(chatod)
            if chatod in usuariosactivos:
                
                if a == "Abrir" or a == "abrir" or a == "Abrir puerta":
        
                    bot.send_message(chatod, "Abriendo puerta...")
                    #blink()
                    
                else:
                    bot.send_message(chatod, "Recuerda que para abrir solo necesitas escribir la palabra Abrir o pulsar el botón")
        else:
            
            if a in contraseñas:#se va a coger el código random de la bbdd
                    posicion=contraseñas.index(a)
                    fechainic=fechasiniciales[posicion]
                    fechafin=fechasfinales[posicion]
                    verificafechainic=comprobarfecha(fechainic)
                    verificafechafin=comprobarfechamaxima(fechafin)
                    if verificafechainic==True and verificafechafin==True:
                        
                        mensajetipo="Enhorabuena! Ya puedes acceder a tu vivienda pulsando o escribiendo Abrir. Espero que tengas una gran estancia"
                        markup=types.ReplyKeyboardMarkup()
                        markup.add('Abrir puerta')
                        usuariosactivos.append(chatod)#Añadimos al usuario en la lista de usuarios que pueden acceder a la vivienda
                        fechafinalusuario.append(chatod)
                        bot.send_message(chatod, mensajetipo, None, None, markup)     
                    else:
                        bot.send_message(chatod, "Su reserva está fuera de fecha, recuerda que esta reserva corresponde al periodo del "+fechainic+"a las 12:00 hasta "+fechafin+" a las 15:00")
            else:
                
                bot.send_message(chatod, "El código que has introducido no es correcto, por favor, intentelo con otro código")
        
print("El bot se esta ejecutando")
try:
        bot.infinity_polling(True)
except Exception as err:
        logger.error(err)
        time.sleep(5)
        print("Error de internet")