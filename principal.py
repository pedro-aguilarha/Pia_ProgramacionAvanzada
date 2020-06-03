import re   #modulo para usar las expresiones regulares
import csv   #modulo para usar los archivos csv y trabajar con ellos
import os    # modulo para trabajar con el sistema operativo
import datetime  #modulo para usar los datos datatime
import json      #modulo para trabajar archivos json
from operator import attrgetter # importamos operator que nos ofrece varias funciones para objetos iterables
from typing import List     # importamos List para trabajar con listas que contienen objetos iterables
from clasepia import CONTACTO  #importamos la clase CONTACTO para guardar objetos en esa clase
Contactos_List=[]   #definimos una lista global para guardar en ella los objetos de la clase CONTACTO


def Main():
    # se crea un bloque de codigo para abrir el archivo csv con whit open('archivo.csv')
    #OJO!! No agregue la ruta del arhcivo porque este mismo se encuentra en la carpeta del area de trabajo
    with open('contactos_mobil.csv') as archivo_csv:   #le damos un alias al archivo
        lector_csv = csv.reader(archivo_csv, delimiter = "|")  # se lee el archivo con un csv.reader
        contador_lineas = 0                                     # y se delimita cada columna por |
        # contador para las lineas del archivo
        # se lee secuencialmente el lector
        for linea_datos in lector_csv:
            if contador_lineas == 0:  #si contador es igual a 0 se imprimen las columnas
                # se concatenan por comas con un .join
                print(f'Los nombres de columna son {", ".join(linea_datos)}')
            else:  # de lo contrario se guarda cada contacto en un objeto temporal de la clase CONTACTO
                objeto_temporal = CONTACTO(linea_datos[0],linea_datos[1],linea_datos[2],linea_datos[3],
                                            linea_datos[4],linea_datos[5])
                Contactos_List.append(objeto_temporal)
                #se agrega a la lista de contactos con un append
        # Se incrementa el número de líneas
            contador_lineas += 1
    # se imprime cuantos contactos se procesaron y cargaron a la lista de contactos
    print(f'{len(Contactos_List)} CONTACTOS CARGADOS...')
    input("PRESIONA ENTER PARA CONTINUAR...")  #se pone una pausa

    # se llama a la funcion de menu que se mostrara al usuario
    Menu_Contactos()

# se define una funcion para mostrar el menu al usuario
def Menu_Contactos():
    #se cicla el menu en un while TRUE
    while True:
        # se borra la pantalla
        os.system ("cls")
        print("MENU CONTACTOS")
        print("[1] Agregar un contacto")
        print("[2] Buscar un contacto")
        print("[3] Eliminar un contacto")
        print("[4] Mostrar contactos")
        print("[5] Serializar datos")
        print("[0] Salir")
        _resp= input("Opcion: ") # se mantiene como string por si coloca cualquier cosa no truene el programa
        # si la opcion es igual a 1 se llama a la funcion agregar contacto
        if _resp == '1': # como _resp se dejo en string se coloca entre comillas sino no lo reconoceria
            Agregar_Contacto()
        elif _resp== '2':  #buscar contacto
            while True:
                #se valida que sea un formato valido
                _telefono= Validar("INSERTE EL TELEFONO CON EL SIGUIENTE FORMATO(99 9999-9999): ","TELEFONO")
                Concidencia= Busqueda_Contacto(_telefono)
                if Concidencia== True:  #si el resultado de la busqueda es verdadero se imprime el contacto
                    for i in Contactos_List:
                        print(i.NICKNAME,"|",i.NOMBRE,"|",i.CORREO,"|",i.TELEFONO,"|",i.FECHA_NACIMIENTO,"|",i.GASTO)
                        input("PRESIONA ENTER PARA CONTINUAR...")  #pausa
                        break
                    break
                else:
                    print("CONTACTO NO ENCONTRADO... INTENTE NUEVAMENTE")
                    input("PRESIONE ENTER PARA CONTINUAR...") #pausa
        elif _resp== '3':  #eliminar contacto
            while True:
                _telefono= Validar("INSERTE EL TELEFONO CON EL SIGUIENTE FORMATO(99 9999-9999): ","TELEFONO")
                Concidencia= Busqueda_Contacto(_telefono) #regresa un booleano
                if Concidencia== True: #si se encontro recorre secuencialmente la lista hasta que _telefono
                    for contacto in Contactos_List:       # sea igual al objeto.TELEFONO
                        if contacto.TELEFONO== _telefono:
                            Contactos_List.remove(contacto)  # elimina el objeto buscado
                            input("PRESIONA ENTER PARA CONTINUAR...")
                            break
                    break
                else:  # si no lo encuentra te refresa nuevamente al menu principal
                    print("CONTACTO NO ENCONTRADO... INTENTE NUEVAMENTE")
                    input("PRESIONE ENTER PARA CONTINUAR...")
                    break

        elif _resp== '4':
            Mostrar_Contactos()
        elif _resp == '5':
            Serializar_Contacto()
        elif _resp == '0':
            print("Se ordenaron los contactos por NickName")
            Ordenar()  #se llama a la funcion ordenar
            cambiar_archivo() # se llama a la funcion cambiar archivo
            escribir_archivo() # se llama a la funcion escribir en archivoz
            print("Se guardaron los contactos en: contactos_mobil.csv ")
            break
        else:   # si es diferente a las opciones disponible te muestra lo siguiente y te devuelve  al menu
            print("Opcion No Encontrada\nIntente con una opcion valida")
            input("PRESIONA ENTER PARA CONTINUAR....")   #pausa

def Validar(_message,_type):  # se reciben 2 parametros
    #procesamiento para nickname
    if _type=="NICKNAME":
        _check="^[A-Z|a-z]{1}[a-z|A-Z|0-9]{4,15}$" #formato que buscara el .search
        while True:
            _captura=input(_message)  # se le pide el dato nickname
            if re.search(_check,_captura):  # se busca en la captura el formato
                return (_captura)   # se retorna lo que capturo el usuario
                break   # se termina el ciclo
            else:
                print("El dato no tiene el tipo correcto")
    #procesamiento para telefono
    if _type=="TELEFONO":
        _check="^[0-9]{2}[ ]{1}[0-9]{4}[-]{1}[0-9]{4}$" #formato que buscara el .search
        while True:
            _captura=input(_message)
            if re.search(_check,_captura):
                return _captura
                break
            else:
                print("El dato no tiene el tipo correcto")
    #procesamiento para nombre
    if _type=="NOMBRE":
        _check="^[A-Z ]{10,35}$" #formato que buscara el .search
        while True:
            _captura=input(_message)
            captura_up= _captura.upper()
            if re.search(_check,captura_up):
                return captura_up
                break
            else:
                print("El dato no tiene el tipo correcto")
    # Procesamiento para float
    if _type=="FLOAT":
        _check="^[0-9]\d*\d.\d{1,2}$" #formato que buscara el .search
        while True:
            _captura=input(_message)
            if re.search(_check,_captura):
                return float(_captura)
                break
            else:
                print("El dato no tiene el tipo correcto")
    # Procesamiento para date
    if _type=="DATE":
        while True:
            _check="^[0-9]{4}/[0-9]{2}/[0-9]{2}$" #formato que buscara el .search
            _captura=input(_message)
            if re.search(_check,_captura):
                    try: #se crea en un bloque try por si ocurre un error
                        anio=int(_captura[0:4])  #usamos la notacion de slices para tomar ciertos caracteres
                        mes=int(_captura[5:7])
                        dia=int(_captura[-2:])
                        return datetime.date(anio,mes,dia)  # se retorna en tipo datetime
                    except ValueError: #si ocurre el error te imprime lo siguiente
                        print("El dato no es una fecha calendario correcta")
            else:
                print("El dato no tiene formato correcto AAAA/MM/DD")
    # Procesamiento para email
    if _type=="EMAIL":
        _check="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$" #formato que buscara el .search
        while True:
            _captura=input(_message)
            if re.search(_check,_captura): # se compara el texto con el formato
                return _captura
                break # se termina el ciclo
            else:
                print("El dato no tiene formato de correo")

def Agregar_Contacto():
    os.system ("cls")
    #llamas a la funcion validar(pregunta, el formato)
    # se valida todos los datos que pediremos llamando a la funcion validar
    nickname= Validar("INSERTE EL NICKNAME: ","NICKNAME")
    nombre= Validar("INSERTE EL NOMBRE: ","NOMBRE")
    correo= Validar("INSERTE EL CORREO: ","EMAIL")
    while True:  # en telefono antes de agregarlo lo busca y si ya existe te pide otro
        telefono= Validar("INSERTE EL TELEFONO CON EL SIGUIENTE FORMATO(99 9999-9999): ","TELEFONO")
        Concidencia = Busqueda_Contacto(telefono)
        if Concidencia== True: # se encontro el contacto
            print("TELEFONO GUARDADO EN OTRO CONTACTO...INTENTE CON OTRO")
            input("PRESIONA ENTER PARA CONTINUAR...")
        else:
            break
    fecha_nacimiento= Validar("INSERTE LA FECHA DE NACIMIENTO CON EL SIGUIENTE FORMATO(YYYY/MM/DD): ","DATE")
    gasto= Validar("INSERTE LOS GASTOS CON EL SIGUIENTE FORMATO(0.00):","FLOAT")
    #se instancia un onjeto con los atributos de la clase CONTACTO
    # se agrega a la lista como objeto de la clase CONTACTO
    objeto_temp= CONTACTO(nickname,nombre,correo,telefono,fecha_nacimiento,gasto)
    Contactos_List.append(objeto_temp)
    print(f"SE AGREGO {objeto_temp.NOMBRE} A LAS {objeto_temp.REGISTRO}") # se muestra la hora en que se registro
    input("PRESIONA ENTER PARA CONTINUAR...")


def Busqueda_Contacto(_telefono): #tiene como parametro el telefono
    os.system ("cls")
    Concidencia= False
    for i in Contactos_List: # se recorre la lista
        if i.TELEFONO == _telefono:
            Concidencia= True
    return Concidencia   # devuelve si encontro o no el telefono
                        # devuelve un booleano
    input("PRESIONA ENTER PARA CONTINUAR")


def Mostrar_Contactos():
    os.system("cls")
    Ordenar()  # se ordenar por nickname
    # se muestran secuencialmente por un for
    for contact in Contactos_List:
        print("NICKNAME: ",contact.NICKNAME)
        print("NOMBRE: ",contact.NOMBRE)
        print("CORREO: ",contact.CORREO)
        print("TELEFONO:",contact.TELEFONO)
        print("FECHA DE NACIMIENTO: ",contact.FECHA_NACIMIENTO)
        print("GASTO: ",contact.GASTO)
        print("-_-"*20)
    input("PRESIONA ENTER PARA CONTINUAR...")

def Serializar_Contacto():
    os.system("cls") #se borra la pantalla
    Ordenar() # se ordenar
    print("CONVERTIR A JSON")
    json_data = json.dumps(Contactos_List, default= lambda o: o.__dict__, indent=4)  #se convierten en json
    print(json_data) # y se imprime el archivo json
    input("PRESIONA ENTER PARA CONTINUAR")

def Ordenar():
    #se ordenan acendentemente
    Contactos_List.sort(key= attrgetter("NICKNAME"), reverse= False)
                            #attrgetter es una funcion importada del modulo operator


def cambiar_archivo():
    ruta_archivo=os.path.abspath(os.getcwd())  # se obtiene la ruta de la carpeta de trabajo actual
    archivo_respaldo=ruta_archivo+"\\contactos_mobil.bak" # se le agrega a la ruta el archivo.bak
    archivo_normal=ruta_archivo+"\\contactos_mobil.csv" # se le agrega a la ruta el archivo.scv

    print(archivo_respaldo)  # se imprime la ruta del arhcivo .bak
    print(archivo_normal)    # se imprime la ruta del archivo.csv

    # si la ruta del respaldo existe
    if os.path.exists(archivo_normal):
    # verifica si hay respaldo, y lo elimina
        if os.path.exists(archivo_respaldo):
            os.remove(archivo_respaldo) #se borra con un remove
        # renombra el archivo de respaldo al arhcivo normal que seria un csv
            os.rename(archivo_normal,archivo_respaldo)

# se genera el archivo csv
    f = open(archivo_normal,"w+")
# se escriben los encabezados del archivo
    f.write("NICKNAME|NOMBRE|CORREO|TELEFONO|FECHANACIMIENTO|GASTO")
# se cierra el archivo
    f.close()

def escribir_archivo():
    #obtiene la ruta de la carpeta de trabajo actual
    ruta = os.path.abspath(os.getcwd())
    archivo_trabajo=ruta+"\\contactos_mobil.csv"
    archivo_respaldo=ruta+"\\contactos_mobil.bak"
    if os.path.exists(archivo_trabajo):
        if os.path.exists(archivo_respaldo):
            os.remove(archivo_respaldo)
        os.rename(archivo_trabajo,archivo_respaldo)
    f = open(archivo_trabajo,"w+")
    #se escriben los encabezados
    f.write("NICKNAME|NOMBRE|CORREO|TELEFONO|FECHANACIMIENTO|GASTO\n")
    # se escribe en cada linea todos los contactos que existen en la lista de contactos
    for e in Contactos_List: # se separan por pipes cada columna
        f.write(f'{e.NICKNAME}|{e.NOMBRE}|{e.CORREO}|{e.TELEFONO}|{e.FECHA_NACIMIENTO}|{e.GASTO}\n')
    f.close()  # se cierra el archivo



# se llama a la  funcion main que es el bloque principal
Main()

#                               PRODUCTO INTEGRADOR DEL APRENDIZAJE
#ESTE PROGRAMA SE DESARROLLÓ POR FINES ACADEMICOS
# GRUPO 23 DE LTI FACPYA UANL
# el programa se desarrolló por:
# PEDRO AGUILAR HERRERA   # NALLELY FLORES HERNANDEZ         #DAYRA  GUZMAN LOPEZ
# DAMARIS  MARTINEZ NUÑEZ                # IVAN  YAKAB BENAVIDEZ


#                                    COLABORACIONES
# PEDRO AGUILAR DESARROLLÓ EL MAIN JUNTO CON LA FUNCION VALIDAR Y OPTIMIZÓ EL PROGRAMA
# NALLELY FLORES DESARROLLÓ LA FUNCION MENU PRINCIPAL JUNTO CON LA DEFINICION DE LAS CLASES
# DAMARIS MARTINEZ DESARROLLÓ  LAS FUNCIONES ESCRIBIR_ARCHIVO Y CAMBIAR ARCHIVO
#IVAN YAKAB DESARROLLÓ LA FUNCION ORDENAR, SERIALIZAR Y MOSTRAR
# DAYRA GUZMAN DESARROLLÓ LAS FUNCIONES  BUSQUEDA_CONTACTO Y AGREGAR_CONTACTO Y ELIMINAR DATOS



