"""
La función principal de este programa es leer los correos de booking que llegan para las reservas. Estos correos pueden ser tanto
reservas como cancelaciones, por lo que debe tener en cuenta las dos opciones. Este programa modifica el .txt externo
de manera que nuestro programa principal (keyhome.py) pueda estar actualizado en todo momento de las reservas que hay
"""

import time
from itertools import chain
import email
import imaplib
import string
imap_ssl_host = 'imap.gmail.com'  # imap.mail.yahoo.com
imap_ssl_port = 993
username = 'correo@correo'
password = 'contraseña'

# Restrict mail search. Be very specific.
# Machine should be very selective to receive messages.
criteria = {
    'FROM':    'aitormartin1992@gmail.com',#Aquí, en el programa real iría noreply@booking.com
    #'SUBJECT': 'Reserva cancelada',
    'BODY':    'PLAZA MAYOR',
}
uid_max = 0
anos = []
ano = 2020#Definimos el año actual y le damos hasta 200 más
for i in range(200):
    anos.append(ano)
    ano += 1
    
def convierteavector(texto):
    if len(texto) > 0:
        texto = string.replace(texto,"'","")
        texto = string.replace(texto,"[","")
        texto = string.replace(texto,"]","")
        texto = string.replace(texto," ","")
        vector = texto.split(',')
        return vector


def conviertefecha(fecha):
    vectordias = ["0","1","2","3","4","5","6","7","8","9"]
    vectormesnum = ["01","02","03","04","05","06","07","08","09","10","11","12"]
    vectormeslet = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]
    pos1 = fecha[0]
    if pos1 in vectordias:
        pos1 = "0"+pos1
    pos2 = fecha[1]
    buscames = vectormeslet.index(pos2)
    pos2 = vectormesnum[buscames]
    pos3 = fecha[2]
    fecha = [pos3,pos2,pos1]
    return fecha
    
def search_string(uid_max, criteria):
    c = list(map(lambda t: (t[0], '"'+str(t[1])+'"'), criteria.items())) + [('UID', '%d:*' % (uid_max+1))]
    return '(%s)' % ' '.join(chain(*c))
    # Produce search string in IMAP format:
    #   e.g. (FROM "me@gmail.com" SUBJECT "abcde" BODY "123456789" UID 9999:*)


def get_first_text_block(msg):
    type = msg.get_content_maintype()

    if type == 'multipart':
        for part in msg.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif type == 'text':
        return msg.get_payload()


server = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)
server.login(username, password)
server.select('INBOX')

result, data = server.uid('search', None, search_string(uid_max, criteria))

uids = [int(s) for s in data[0].split()]
if uids:
    uid_max = max(uids)
    # Initialize `uid_max`. Any UID less than or equal to `uid_max` will be ignored subsequently.

server.logout()


# Keep checking messages ...
# I don't like using IDLE because Yahoo does not support it.
while 1:
    # Have to login/logout each time because that's the only way to get fresh results.

    server = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)
    server.login(username, password)
    server.select('INBOX')

    result, data = server.uid('search', None, search_string(uid_max, criteria))

    uids = [int(s) for s in data[0].split()]
    for uid in uids:
        # Have to check again because Gmail sometimes does not obey UID criterion.
        if uid > uid_max:
            result, data = server.uid('fetch', uid, '(RFC822)')  # fetch entire message
            msg = email.message_from_string(data[0][1])
            
            uid_max = uid
        
            text = get_first_text_block(msg)
            print 'New message :::::::::::::::::::::'
            buscareserva = str(msg)
            if "t_new_reservation" in buscareserva:
                
                pos = buscareserva.index("t_new_reservation")
                pos = pos + 19
                posfinal = pos + 10
                numreserva = buscareserva[pos:posfinal]
                print ("El numero de reserva es el "+numreserva)
            if "Cancelaci" in buscareserva:
                pos = buscareserva.index("res_id=")
                pos = pos + 9
                posfinal = pos + 10
                numreserva = buscareserva[pos:posfinal]
                print ("El numero de cancelación es el "+numreserva)
            for i in range(200):
                ano = str(anos[i])
                if (" de "+ano+")") in buscareserva:
                    pos = buscareserva.index((" de "+ano+")"))
                    posfinal = pos + 8
                    bucleinf = True
                    while bucleinf == True:
                        pos = pos - 1
                        if buscareserva[pos] == ",":
                            bucleinf = False
                    pos = pos + 2
                    buscafecha = buscareserva[pos:posfinal]
                    buscafecha = buscafecha.split(' de ')
                    buscafecha = conviertefecha(buscafecha)
                    buscafecha.append(numreserva)

                    f = open ('reservas.txt','r')
                    texto = f.read()
                    f.close()
                    if len(texto) > 0:
                        vector = convierteavector(texto)
                    if "Cancelaci" in buscareserva:
                        if numreserva in vector:
                            pos = vector.index(numreserva)
                            pos = pos -3
                            for i in range(4):
                                vector.pop(pos)
                                print(vector)
                    else:
                        for i in range(4):
                            vector.append(buscafecha[i])
                    f = open ('reservas.txt','w')
                    f.write(str(vector))
                    f.close()
                        
                    
            
    server.logout()
    time.sleep(1)