# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 11:58:18 2020

@author: Aitor Martín
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
# Establecemos conexion con el servidor smtp de gmail
mailServer = smtplib.SMTP('smtp.gmail.com',587)
mailServer.ehlo()
mailServer.starttls()
mailServer.ehlo()
mailServer.login("tucorreo@correo","tucontraseña")
print (mailServer.ehlo())



#ENVIAR MENSAJES

# Construimos un mensaje Multipart, con un texto y una imagen adjunta
mensaje = MIMEMultipart()
mensaje['From']="correo_remitente"
mensaje['To']="correo_destinatario"
mensaje['Subject']="Asunto del correo"
# Adjuntamos el texto
mensaje.attach(MIMEText("Cuerpo del correo"))
# Adjuntamos la imagen
file = open("imagen.jpg", "rb")
contenido = MIMEImage(file.read())
contenido.add_header('Content-Disposition', 'attachment; filename = "imagen.jpg"')
mensaje.attach(contenido)
# Enviamos el correo, con los campos from y to.
mailServer.sendmail("correo_emisor",
                "correo_destinatario",
                mensaje.as_string())

# Cierre de la conexion
mailServer.close()