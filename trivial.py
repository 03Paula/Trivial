from multiprocessing import connection
import sqlite3
from random import randrange
import datetime 
from sqlite3 import Error
import csv

def preguntasTrivial():
    ## Extraemos las posibles respuestas de cada pregunta y las almacenamos en un diccionario.
    try:
        file = open('preguntas.txt') ## Abrimos el archivo que contiene las preguntas
    except FileNotFoundError:
        print("El archivo preguntas.txt no existe.")
        exit()
    else:
        c = 0 ## Creamos una variable que funcione como contador para que cada 5,empiece la pregunta.
        diccionario_preg : dict = {}
        lista = []
        for line in file:
            if c!=5:
                if c==0: ## La primera línea es la pregunta
                    diccionario_preg["pregunta"] = line.rstrip('\n')
                    c+=1
                elif c==1: ## La segunda línea es la respuesta.
                    diccionario_preg["respuesta"] = line.rstrip('\n')
                    c+=1
                elif c==2: ## La tercera línea es la primera opción.
                    diccionario_preg["opcion1"] = line.rstrip('\n')
                    c+=1
                elif c==3: ## La cuarta línea es la segunda opción.
                    diccionario_preg["opcion2"] = line.rstrip('\n')
                    c+=1
                elif c==4: ## La quinta línea es la tercera opción
                    diccionario_preg["opcion3"] = line.rstrip('\n')
                    c+=1
                else:
                    c+=1
            else: ## La sexta línea es la última opción 
                diccionario_preg["opcion4"] =line.rstrip('\n')
                lista.append(diccionario_preg)
                c=0
                diccionario_preg = {} ## Volvemos a dejar el diccionario vacio
        return lista


def connection(db_file):
    ## Conectamos con la base de datos
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e: ## Si hay un error imprimirá el error.
        print(e)

    return conn


def crear_insertar(cursor):
    ## Se crea una tabla si no existe, con los siguientes campos
    cursor.execute("CREATE TABLE IF NOT EXISTS resultados_trivial(fecha_finalizacion TIMESTAMP, jugador TEXT,puntuacion INTEGER)")
    db.commit
    fecha = datetime.datetime.now()
    ## Insertamos los valores en la tabla
    cursor.execute('''INSERT INTO resultados_trivial(fecha_finalizacion,jugador,puntuacion)
                  VALUES(:fecha_finalizacion,:jugador,:puntuacion)''', 
                {'fecha_finalizacion':fecha,'jugador':jugador,'puntuacion':puntuacion})
    db.commit()


## Imprime los resultados guardados en la base de datos
def resultados():
    for row in cursor.execute("select * from resultados_trivial"):
        print(row)


## Crea un fichero .csv con datos de la tabla resultados_trivial.
def ficheroCSV():
    cursor.execute("select * from resultados_trivial")
    rows = cursor.fetchall()
    csv_path = 'Datos.csv'
    with open(csv_path,'w',newline="") as csv_file:
        csv_writer = csv.writer(csv_file,delimiter=",")
        ## Escribe los campos de la tabla.
        csv_writer.writerow([i[0] for i in cursor.description])
        ## Escribe los datos de la tabla.
        csv_writer.writerows(rows)


if __name__ == "__main__":
    
    #Introducción
    print("************************************************************************************")
    print("*                                     TRIVIAL                                      *")
    print("************************************************************************************")

    print("Bienvenido al trivial, a continuación le explicaré las instrucciones.\n")
    print("-Instrucciones")
    print("El juego es muy sencillo, se le pasaran unas preguntas, en concreto 10, las cuales tendrán sus opciones."+
    "\nPara responder a las preguntas simplemente tendrás que elegir una letra de la a a la d.")
    print("Suerte!!\n")

    jugador = input("Escriba su nombre: ")
    print("Comencemos con las preguntas\n")
    puntuacion = 0
    preguntas = 0
    rep: list  = []## Variable para evitar repetidos
    while preguntas!=10:
        indice = randrange(0,len(preguntasTrivial()))
        if indice not in rep:
            rep.append(indice)
            preguntas+=1
            pregunta = preguntasTrivial()[indice]
            print(pregunta["pregunta"])
            print("A) " + pregunta["opcion1"])
            print("B) " + pregunta["opcion2"])
            print("C) " + pregunta["opcion3"])
            print("D) " + pregunta["opcion4"])

            respuesta = input("Escriba su respuesta: ")
            if respuesta.upper() == pregunta["respuesta"]:
                print("Has elegido la respuesta correcta.\n")
                puntuacion+=1
            else:
                print("No has elegido la opción correcta.La opción correcta era " + pregunta["respuesta"] + "\n")
        else:
            continue
    
    print("Número de preguntas acertadas " + str(puntuacion) + "\n")

    db = connection("Trivial.db")
    cursor = db.cursor()
    crear_insertar(cursor)

    print("----------------Resultados----------------")
    resultados()

    ficheroCSV()
    db.close() ## Cerramos la conexion con la base de datos.
    print("Sqlite conexión cerrada")
  
    


