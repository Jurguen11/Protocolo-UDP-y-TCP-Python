# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 16:17:27 2020

@author: Jurguen
"""

import os
import socket
from threading import Thread

#nombre_archivo, IP_address, puerto, parametro, nombre del archivo

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
HOST = socket.gethostbyname(socket.gethostname())
PORT = 1161
s.bind((HOST, PORT))
tamaño_b = 1024000

def main():

    while True:
        print("Connection to %s established")

        data = s.recvfrom(tamaño_b)
        address = data[1]
        mesage  = data[0]
        print(mesage)
        mesage = limpiar(str(mesage))
        mesage = mesage.split(",")
        print(mesage)
        if(mesage[0] == "-d"):
            descarga(mesage,address)
            break
        elif(mesage[0] == '-l'):
            print("Listado de archivos")
            listado(address)
            break
        elif(mesage[0] == "-u"):
            if (len(mesage)>1):    
                subir(mesage,address)  
            else:
                s.sendto(bytes("-1", "utf-8"),address)
            break
        else:
            s.sendto(bytes("-1","utf-8"),address)
            break
#Esto es para enviar el archivo que se desea descargar
def descarga(archivo,address):
    archivo_data = encontrar_archivo(str(archivo[1]))
    if( archivo_data != False):
        s.sendto(archivo_data,address)
    else:
        s.sendto(bytes("-1","utf-8"),address)

#Busca el archivo y regresa si lo encuentra y false si no
def encontrar_archivo(documento):
    direccion = os.getcwd()+"/Archivos/"+documento
    try:
        documento = open(direccion, "rb").read()
        return documento
    except:
        return False
    
#Para mostrar la lista de los archivos que contiene el servidor
def listado(address):
    direccion = os.getcwd() +  "/Archivos"
    listado_archivos = os.listdir(direccion)
    mensaje = ""
    for i in listado_archivos:
        mensaje+=i+','
    s.sendto(bytes(mensaje,"utf-8"),address)
#
def subir(archivo,address):
    contenido=s.recvfrom(tamaño_b)
    print(contenido)
    direccion = os.getcwd()+"/Archivos/"+archivo[1]
    archivo = open(direccion,"wb")
    archivo.write(contenido[0])
    archivo.close()
    s.sendto(bytes("El archivo se subio al servidor","utf-8"),address)

def limpiar(txt):
    txt = txt[2:len(txt)-1]
    return txt

def conexiones():
    while True:
        main()

if __name__ == "__main__":
    print("Waiting for connections...")
    ACCEPT_THREAD = Thread(target=conexiones)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    print("max connections reached!")
    s.close()
    
