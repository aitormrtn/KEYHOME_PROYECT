# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 02:56:28 2020

@author: Usuario

http://www.tuxrincon.com/blog/python-multihilo-ejemplos/
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from datetime import date
from datetime import datetime
import telebot
from telebot import types
import time
bot = telebot.TeleBot('1051111158:AAFvK-O_b3OYY_9yG90i3etabjl_-xBGOVE')
pagina = ["Cafetera","B00791D5AK","Pulsera de plata","B01JYAMSTW","Pulsera deportiva","B07B49316G","Colgador de cinturones de madera","B004BL1TBI"]
stock = []
ventas = []
busqueda = []
urls = []
for i in range(int(len(pagina)/2)):
    ventas.append(0)
    busqueda.append(0)
    urls.append(0)
while True:
    for i in range(int(len(pagina)/2)):
        pos = 2*i+1
        busqueda[i] = webdriver.Firefox()
        urls[i] = ("https://www.amazon.es/dp/"+pagina[pos]+"")
        busqueda[i].get(urls[i])
    time.sleep(2)
    for i in range(int(len(pagina)/2)):
        busqueda[i].find_element_by_id("add-to-cart-button").click()
    time.sleep(2)
    for i in range(int(len(pagina)/2)):
        busqueda[i].find_element_by_id("nav-cart").click()
    time.sleep(2)
    for i in range(int(len(pagina)/2)):
        busqueda[i].find_element_by_id("a-autoid-0-announce").click()
    time.sleep(2)
    for i in range(int(len(pagina)/2)):
        busqueda[i].find_element_by_id("dropdown1_10").click()
    time.sleep(2)
    for i in range(int(len(pagina)/2)):
        busqueda[i].find_element_by_name("quantityBox").send_keys("999")
    time.sleep(0.2)
    for i in range(int(len(pagina)/2)):
        busqueda[i].find_element_by_id("a-autoid-1-announce").click()
    time.sleep(2)
    for i in range(int(len(pagina)/2)):
        texto = busqueda[i].find_element_by_xpath("/html/body")
        texto = str(texto.text)
        pos = texto.index("Subtotal (")
        pos = pos + 10
        if texto[pos+1] == " ":
            posfinal = pos+1
        if texto[pos+2] == " ":
            posfinal = pos+2
        if texto[pos+3] == " ":
            posfinal = pos+3
        cantidad = texto[pos:posfinal]
        if len(stock) < (len(pagina)/2):
            stock.append(cantidad)
        else:
            ventas[i] = int(ventas[i]) + int(stock[i]) - int(cantidad)
            stock[i] = cantidad
        stock[i] = cantidad
        print("Hay "+cantidad+" unidades en Stock disponibles")
    for i in range(int(len(pagina)/2)):
        busqueda[i].find_element_by_class_name("sc-action-delete").click()
        busqueda[i].close()
    print(datetime.now())
    new_date = datetime(2020, 4, 20, 19, 42, 00, 00000)
    if datetime.now() > new_date:        
        mensaje = ""
        bot.send_message(250187565, "Hola Aitor, te informo del seguimiento de tus productos.")
        for i in range(int(len(pagina)/2)):
            mensaje = "Se han vendido "+str(ventas[i])+" unidades del artículo "+str(pagina[i*2])+"."
            bot.send_message(250187565, mensaje)
        break
    print("El stock es "+str(stock)+"")
    print("Las ventas son "+str(ventas)+"")
    time.sleep(600)

"""
print(browser.find_element_by_name("quantityBox"))
print(browser.context)
browser.close()
"""