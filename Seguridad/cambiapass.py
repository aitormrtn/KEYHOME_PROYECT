# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 13:37:15 2019

@author: Aitor Martín

Este programa tiene por objeto actualizar, de forma periodica, una contraseña de 6 digitos para cada usuario, de manera que 
la seguridad del sistema KeyHome aumente.
"""

import sqlite3
import random


#Esta función genera una contraseña numérica de n digitos
def generapass():
    caracteres = "0123456789"
    n = 6;
    password=""
    for i in range(n):#Creamos una pass de 12 digitos
        digito = random.randrange(10)
        password=password+caracteres[digito]
    return password

#Conectamos con la base de datos y creamos un cursor
miConexion = sqlite3.connect("Seguridad")
miCursor = miConexion.cursor()

#Contamos el número de registros que tenemos
miCursor.execute("SELECT * FROM SEGURIDAD")
obtieneregistros = miCursor.fetchall()
contador = 0
for id_usuario in obtieneregistros:
   contador += 1
   
#Creamos una nueva contraseña para cada usuario

for i in range(contador):
    i+=1
    num = str(i)
    print(num)
    password = generapass()
    miCursor.execute("UPDATE SEGURIDAD SET CONTRASEÑA="+password+" WHERE ID_USUARIO="+num+"")
    print(password)

miConexion.commit()
miConexion.close()