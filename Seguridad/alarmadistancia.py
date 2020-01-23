"""
El objeto de este programa es el de avisar al propietario de la vivienda en el caso de que algún intruso abra la caja en la que se encuentra
la Raspberry Pi Zero W
"""
#trigger gpio 17
#echo gpio 4

import RPi.GPIO as GPIO    #Importamos la libreria GPIO
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
#Importamos time (time.sleep)
GPIO.setmode(GPIO.BCM)     #Ponemos la placa en modo BCM
GPIO_TRIGGER = 17          #Usamos el pin GPIO 17 como TRIGGER
GPIO_ECHO    = 4           #Usamos el pin GPIO 4 como ECHO
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  #Configuramos Trigger como salida
GPIO.setup(GPIO_ECHO,GPIO.IN)      #Configuramos Echo como entrada
GPIO.output(GPIO_TRIGGER,False)    #Ponemos el pin 17 como LOW

destinatario = "aitormartin1992@gmail.com"#En este campo se debe introducir el correo electrónico al que queremos que se de el aviso de alarma

def alarma(destinatario):
    # Establecemos conexion con el servidor smtp de gmail
    mailServer = smtplib.SMTP('smtp.gmail.com',587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login("keyhomeproject@gmail.com","*R6pN!RpC*5e")
    print (mailServer.ehlo())



    #ENVIAR MENSAJES

    # Construimos un mensaje Multipart, con un texto y una imagen adjunta
    mensaje = MIMEMultipart()
    mensaje['From']="keyhomeproject@gmail.com"
    mensaje['To']=destinatario
    mensaje['Subject']="Alarma en tu vivienda de uso turístico"
    # Adjuntamos el texto
    mensaje.attach(MIMEText("La caja de tu raspberry pi ha sido abierta. Por favor, cuando acudas a la vivienda de nuevo reinicia el sistema introduciendo una copia de la tarjeta microSD"))
    """
    # Adjuntamos la imagen
    file = open("imagen.jpg", "rb")
    contenido = MIMEImage(file.read())
    #contenido.add_header('Content-Disposition', 'attachment; filename = "imagen.jpg"')
    mensaje.attach(contenido)
    """
    # Enviamos el correo, con los campos from y to.
    mailServer.sendmail("keyhomeproject@gmail.com",
                    destinatario,
                    mensaje.as_string())

    # Cierre de la conexion
    mailServer.close()
try:
    while True:     #Iniciamos un loop infinito
        GPIO.output(GPIO_TRIGGER,True)   #Enviamos un pulso de ultrasonidos
        time.sleep(0.001)                #Una pequenna pausa
        GPIO.output(GPIO_TRIGGER,False)  #Apagamos el pulso
        start = time.time()              #Guarda el tiempo actual mediante time.time()
        while GPIO.input(GPIO_ECHO)==0:  #Mientras el sensor no reciba senal...
            start = time.time()          #Mantenemos el tiempo actual mediante time.time()
        while GPIO.input(GPIO_ECHO)==1:  #Si el sensor recibe senal...
            stop = time.time()           #Guarda el tiempo actual mediante time.time() en otra variable
        elapsed = stop-start             #Obtenemos el tiempo transcurrido entre envio y recepcion
        distance = (elapsed * 34300)/2   #Distancia es igual a tiempo por velocidad partido por 2   D = (T x V)/2
        print (distance)                   #Devolvemos la distancia (en centimetros) por pantalla
        if distance > 10:
            #Esto querría decir que han abierto la caja, por lo que avisamos al propietario
            alarma(destinatario)
            break#Salimos del bucle para no enviar más avisos
        time.sleep(1)                    #Pequena pausa para no saturar el procesador de la Raspberry
except KeyboardInterrupt:                #Si el usuario pulsa CONTROL+C...
    print ("sesion finalizada")                         #Avisamos del cierre al usuario
    GPIO.cleanup()                       #Limpiamos los pines GPIO y salimos