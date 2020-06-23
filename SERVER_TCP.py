# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 16:13:03 2020

@author: Jurguen
"""


import os
import socket
from threading import Thread


#nombre_archivo, IP_address, puerto, parametro, nombre del archivo


#python SERVER.py DESKTOP-2RLFBAM 8000 -l

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = socket.gethostbyname(socket.gethostname())
PORT = 10000
s.bind((HOST, PORT))
s.listen(20)
tamaño_b = 1024000
def main():
    while True:
        connection, client_address = s.accept()
        
        print("Connection to %s established", client_address)
        try:
            while True:
                data = connection.recv(tamaño_b)
                data = data.decode()
                data = data.split(",")
                argumento = data[0]
                
                if(argumento == "-d"):
                    descarga(connection,data[1])
                    break
                elif(argumento == '-l'):
                    listado(connection)
                    break
                elif(argumento == "-u"):
                    if (len(data)>1):    
                        subir(connection,data[1])  
                    else:
                        connection.send(bytes("El parametro requiere el nombre del un archivo", "utf-8"))
                    break
                else:
                    connection.send(bytes("Puede que el parametro sea incorrecto","utf-8"))
                    break
        finally:
            connection.close()
#Esto es para enviar el archivo que se desea descargar
def descarga(conn, archivo):
    archivo = encontrar_archivo(archivo)
    if( archivo != False):
        conn.send(archivo)
    else:
        conn.send(bytes("Es posible que el archivo no exista","utf-8"))

#Busca el archivo y regresa si lo encuentra y false si no
def encontrar_archivo(documento):
    direccion = os.getcwd()+"/Archivos/"+documento
    try:
        documento = open(direccion, "rb").read()
        return documento
    except:
        return False
    
#Para mostrar la lista de los archivos que contiene el servidor
def listado(conn):
    direccion = os.getcwd() +  "/Archivos"
    listado_archivos = os.listdir(direccion)
    mensaje = ""
    for i in listado_archivos:
        mensaje+=i+'\n'
    conn.send(bytes(mensaje,"utf-8"))
#
def subir(conn,archivo):
    contenido=conn.recv(tamaño_b)
    contenido.decode()
    direccion = os.getcwd()+"/Archivos/"+archivo
    archivo = open(direccion,"wb")
    archivo.write(contenido)
    archivo.close()
    conn.send(bytes("El archivo se subio al servidor","utf-8"))

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
    