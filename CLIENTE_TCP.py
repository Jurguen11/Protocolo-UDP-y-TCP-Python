# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 16:13:39 2020

@author: Jurguen
"""


import socket
import sys
import os


argumentos = len(sys.argv)
tamaño_buffer = 1024000


def encontrar_archivo(documento):
    direccion = os.getcwd()+"/Archivos Cliente/"+documento
    try:
        documento = open(direccion, "rb").read()
        return documento
    except:
        return False

if ( (argumentos>5) or (argumentos<4)):
    print("El comando requiere minimo el formato: python nombre_archivo.py direccion_IP Puerto Argumento")
else:
    IP_address  = sys.argv[1]
    puerto      = int(sys.argv[2])
    argumento   = sys.argv[3]
    archivo     = ""

    if (len(sys.argv)==5):
        archivo = sys.argv[4]
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP_address,puerto))
    
    try:
        mensaje = argumento +","+archivo
        s.send(bytes(mensaje,"utf-8"))
        if(argumento=="-l"):
            mensaje=s.recv(tamaño_buffer)
            print(mensaje.decode())
        elif(argumento == "-d"):
            mensaje=s.recv(tamaño_buffer)
            print("Esperando respuesta del servidor")
            mensaje.decode()
            direccion = os.getcwd()+"/Archivos Cliente/"+archivo
            print("Descargando archivo")
            archivo = open(direccion,"wb")
            archivo.write(mensaje)
            archivo.close()
            print("Puedes ver el archivo en la carpeta Archivos Cliente")
        elif(argumento == "-u"):
            arch_encontrado = encontrar_archivo(archivo)
            if(arch_encontrado != False):
                print("Subiendo...")
                s.send(arch_encontrado)
                mensaje=s.recv(tamaño_buffer)
                print(mensaje.decode())
            else:
                print("Este archivo no existe")
            
    finally:
        s.close()
