import re
import ply.lex as lex
from tkinter import filedialog
import tkinter as tk
import time


tokens = ( 
         "CORCHETE_I", "CORCHETE_D",
         "LLAVE_I", "LLAVE_D",
         "COMA", "COMILLA", "DOSPUNTOS",
         
        "EQUIPOS", "VERSION", "FIRMA_DIGITAL",
        "NOMBRE_EQ", "IDENTIDAD_EQ", "LINK", "ASIGNATURA", "CARRERA",
        "UNIVERSIDAD_REG", "DIRECCION","ALIANZA_EQ",
        
        "NOMBRE", "EDAD", "CARGO", "FOTO", "EMAIL", "HABILIDADES", "SALARIO", "ACTIVO",
        
        "PROYECTOS", "NOMBRE_PROY", "ESTADO_PROY", "RESUMEN_PROY", "TAREAS_PROY", "FECHA_INICIO", "FECHA_FIN", "FECHA_VALOR",
        "VIDEO_PROY", "CONCLUSION_PROY",
        
        "FECHA", "NULL", "INTEGER", "FLOAT", "BOOLEAN", "URL", "STRING"
         )
t_COMILLA = r'\"'
t_CORCHETE_I = r'\['
t_CORCHETE_D = r'\]'
t_LLAVE_I = r'\{'
t_LLAVE_D = r'\}'
t_COMA = r','
t_DOSPUNTOS = r':'

t_ignore =  ' \t\n'

def t_FECHA_VALOR(t):
    r'"(19|20)\d{2}-\d{2}-\d{2}"'
    return t

def t_URL(t):
   r'"https?://[^\s"]+"'
   return t 

def t_STRING(t):
    r'"[^"]*"'
    palabras_reservadas = {
        '"equipos"': "EQUIPOS",
        '"version"': "VERSION",
        '"firma_digital"': "FIRMA_DIGITAL",
        '"nombre_equipo"': "NOMBRE_EQ",
        '"identidad_equipo"': "IDENTIDAD_EQ",
        '"link"': "LINK",
        '"asignatura"': "ASIGNATURA",
        '"carrera"': "CARRERA",
        '"universidad_regional"': "UNIVERSIDAD_REG",
        '"direccion"': "DIRECCION",
        '"alianza equipo"': "ALIANZA_EQ",
        '"nombre"': "NOMBRE",
        '"edad"': "EDAD",
        '"cargo"': "CARGO",
        '"foto"': "FOTO",
        '"email"': "EMAIL",
        '"habilidades"': "HABILIDADES",
        '"salario"': "SALARIO",
        '"activo"': "ACTIVO",
        '"proyectos"': "PROYECTOS",
        '"estado"': "ESTADO_PROY",
        '"resumen"': "RESUMEN_PROY",
        '"tareas"': "TAREAS_PROY",
        '"fecha_creacion"': "FECHA_INICIO",
        '"fecha_fin"': "FECHA_FIN",
        '"video"': "VIDEO_PROY",
        '"conclusion"': "CONCLUSION_PROY"
    }
    # Si el valor capturado está en palabras reservadas, cambia su tipo
    if t.value in palabras_reservadas:
        t.type = palabras_reservadas[t.value]
    return t

def t_INTEGER(t):
    r'-?\d+'
    t.value = int(t.value)
    return t 

def t_FLOAT(t):
    r'\d+\.\d{1,2}'
    t.value = float(t.value)
    return t 

def t_BOOLEAN(t):
    r'(true|flase)'
    t.value = True if t.value == 'true' else False
    return t 

def t_NULL(t):
    r'null'
    return t 

def t_error(t):
   print(f"Caracter ilegal '{t.value[0]}'")
   t.lexer.skip(1) 

lexer = lex.lex()

# PRUEBA
if __name__ == "__main__":
    data = '''
        {
        "nombre_equipo": "Los Pibes",
        "identidad_equipo": "https://pagina.com",
        "asignatura": "Sintaxis",
        "carrera": "Sistemas",
        "universidad_regional": "UTN FRRe",
        "direccion": null,
        "alianza equipo": "Unidos",
        "integrantes": [],
        "proyectos": [],
        "fecha_creacion": "2025-04-15"
        }
        '''

    lexer.input(data)
    for tok in lexer:
        print(tok)
  

