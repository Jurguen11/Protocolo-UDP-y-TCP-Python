# -*- coding: utf-8 -*-


##C:\Users\Jurguen\.spyder-py3\servidorSocket
##python CLIENTE_UDP.py 192.168.0.14 1159 -l
##
"""
Created on Mon Jun 22 16:12:28 2020

@author: Jurguen
"""
import socket
import sys
import os


argumentos = len(sys.argv)
tamaño_buffer = 1024000
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
def encontrar_archivo(documento):
    direccion = os.getcwd()+"/Archivos Cliente/"+documento
    try:
        documento = open(direccion, "rb").read()
        return documento
    except:
        return False

def limpiar(txt):
    txt = txt[2:len(txt)-1]
    return txt

if ( (argumentos>5) or (argumentos<4)):
    print(sys.argv)
    print("El comando requiere minimo el formato: python nombre_archivo.py direccion_IP Puerto Argumento")
else:
    IP_address  = sys.argv[1]
    puerto      = int(sys.argv[2])
    argumento   = sys.argv[3]
    archivo     = ""
    addressPort = (IP_address,puerto)
    if (len(sys.argv)==5):
        archivo = sys.argv[4]
    
    mensaje = argumento +","+archivo
    print(mensaje)
    s.sendto(bytes(mensaje,"utf-8"),addressPort)
    if(argumento=="-l"):
        mensaje=s.recvfrom(tamaño_buffer)
        mensaje = limpiar(str(mensaje[0]))
        lista = mensaje.split(",")
        for i in lista:
            print(i)
    elif(argumento == "-d"):
        mensaje=s.recvfrom(tamaño_buffer)
        print(mensaje)
        print("Esperando respuesta del servidor")
        if(str(mensaje[0])=="b'-1'"):
            print("El nombre del archivo no existe")
        else:
            direccion = os.getcwd()+"/Archivos Cliente/"+archivo
            archivo = open(direccion,"wb")
            archivo.write(mensaje[0])
            archivo.close()
            print("Archivo guardado")
        
    elif(argumento == "-u"):
        arch_encontrado = encontrar_archivo(archivo)
        if(arch_encontrado != False):
            print("Subiendo...")
            s.sendto(arch_encontrado,addressPort)
            mensaje=s.recvfrom(tamaño_buffer)
            print(mensaje[0])
        else:
            print("Este archivo no existe")
    else:
        print("Puede que el parametro sea incorrecto")