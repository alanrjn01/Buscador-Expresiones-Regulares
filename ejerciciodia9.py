import os
from pathlib import Path
import re
import datetime
import time
import math

'''A esta función se le pasa por argumento un directorio y un patrón de expresión regular -> luego se crea una 
instancia de "Path" con la ubicación y se compila la expresión regular en una variable -> con el módulo "os" 
recorremos todo el árbol de carpetas almacenando la carpeta, subcarpetas y los archivos dentro -> en la iteracion
de archivos abrimos y leemos el contenido de cada "txt" para luego hacer una busqueda con el patrón indicado 
en el contenido del archivo -> si la búsqueda e scorre'''


def recorrer_archivos(ruta, patron):
    regular_expresion = re.compile(patron)
    ubicacion = Path(ruta)
    dic_archivo_serie = {}
    for carpeta, subcarpeta, archivo in os.walk(ubicacion):
        for arc in archivo:
            ruta_archivos = Path(carpeta, Path(arc))
            archivo_leido = ruta_archivos.open().readlines()
            busqueda = re.search(regular_expresion, str(archivo_leido))
            if busqueda is not None:
                dic_archivo_serie[arc] = busqueda.group()
    return dic_archivo_serie


'''
Esta función se encarga de recibir como parámetro el diccionario retornado de la función "recorrer_archivos" ->
por dentro se crea un objeto datetime con la fecha actual y se imprime por pantalla la clave y valor de cada elemento
del diccionario -> posteriormente se informa cuantos elementos posee el diccionario y el tiempo de búsqueda
'''


def imprimir_resultados(diccionario, tiempo_busqueda):
    fecha_actual = datetime.date.today()
    print(f'Fecha de búsqueda: [{fecha_actual}]')
    print("ARCHIVO\t        NRO.SERIE")
    print("-----------------------------")
    for key, value in diccionario.items():
        print(f'{key}\t{value}')
    pass
    print(f'\nCoincidencias encontradas: {len(diccionario)}')
    print(f'Duración de la búsqueda: {math.ceil(tiempo_busqueda)} segundo(s)')
    print("-----------------------------")


'''
Esta es la función del menú donde pide ingresar un número entre el 1 y el 2 capturando posibles errores
'''


def menu():
    print("Ingrese una opción:\n1-Comenzar aplicación\n2-Salir")
    check = False
    numero = 0
    while check == False:
        try:
            numero = int(input(">"))
            if numero < 1 or numero > 2:
                check = False
            else:
                check = True
        except:
            print("valor incorrecto")
    return numero


'''
Variables globales para la ejecución del código
'''


opcion = menu()
salir = False
ubicacion_correcta = False
directorio_ingresado = ''
patron = ''
patron_ingreso_directorio = r'\D:\w*'


'''
Ejecución del programa:
-case 1 : se pide el ingreso de un directorio, se realiza una comprobación sencilla con una expresión regular la cual
determina si empieza con "una letra y dos puntos" -> se pide ingresar una expresión regular para realizar la búsqueda
en los archivos encontrados -> se pasa a la función "recorrer_archivos" con el directorio y el patrón ingresados y 
el return de la función se almacena en una variable -> se realiza la búsqueda con un timer para calcular 
el tiempo de ejecución de la búsqueda -> luego se llama a la función "imprimir_resultados" indicando como argumento
el diccionario obtenido con el recorrido de archivos y el tiempo y dicha función se encarga de mostrar en consola
el resultado 
'''


while salir == False:

    match opcion:
        case 1:

            while ubicacion_correcta == False:
                directorio_ingresado = input("Ingrese la ruta donde desea buscar: ")
                # E:\Workspace-Python\Practica\EjercicioDia9\Carpeta_Descomprimida\Mi_Gran_Directorio
                directorio_ingresado_correctamente = re.search(patron_ingreso_directorio, directorio_ingresado)
                print("¡Formato de ruta incorrecta!")
                if directorio_ingresado_correctamente is not None:
                    ubicacion_correcta = True

            patron = input("Ingrese el patrón que desea buscar (Expresión regular): ")
            # N\D{3}-\d{5}

            inicio = time.time()
            diccionario_resultado = recorrer_archivos(directorio_ingresado, patron)
            final = time.time()

            tiempo_busqueda = final - inicio
            imprimir_resultados(diccionario_resultado, tiempo_busqueda)

        case 2:
            break

    ubicacion_correcta = False
    opcion = menu()
