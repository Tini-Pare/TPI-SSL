import ply.lex as lex
import os
import sys
import datetime

tokens = (
    "CORCHETE_I", "CORCHETE_D", "LLAVE_I", "LLAVE_D",
    "COMA", "COMILLA", "DOSPUNTOS", "INTEGRANTES",
    "EQUIPOS", "VERSION", "FIRMA_DIGITAL", "NOMBRE_EQ", "IDENTIDAD_EQ", "LINK",
    "ASIGNATURA", "CARRERA", "UNIVERSIDAD_REG", "DIRECCION", "ALIANZA_EQ",
    "NOMBRE", "EDAD", "CARGO", "FOTO", "EMAIL", "HABILIDADES", "SALARIO", "ACTIVO", "ESTADO",
    "TO_DO", "IN_PROGRESS", "ON_HOLD", "DONE", "CANCELLED",
    "PROYECTOS", "NOMBRE_PROY", "ESTADO_PROY", "RESUMEN_PROY", "TAREAS_PROY",
    "FECHA_INICIO", "FECHA_FIN", "FECHA_VALOR", "VIDEO_PROY", "CONCLUSION_PROY",
    "FECHA", "NULL", "INTEGER", "FLOAT", "BOOLEAN", "URL", "STRING"
)

t_COMILLA = r'\"'
t_CORCHETE_I = r'\['
t_CORCHETE_D = r'\]'
t_LLAVE_I = r'\{'
t_LLAVE_D = r'\}'
t_COMA = r','
t_DOSPUNTOS = r':'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_FECHA_VALOR(t):
    r'"(19|20)\d{2}-\d{2}-\d{2}"'
    date_str = t.value.strip('"')
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
        t.type = 'FECHA_VALOR'
        return t
    except ValueError:
        print(f"❌ Error léxico: Fecha en formato incorrecto o inválida '{t.value}' en la línea {t.lineno}")
        t.lexer.skip(len(t.value))
        return None

def t_URL(t):
    r'"https?://[^\s"]+"'
    return t

def t_EMAIL(t):
    r'"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"'
    return t

def t_STRING(t):
    r'"[^"]*"'
    palabras_reservadas = {
        '"integrantes"': "INTEGRANTES",
        '"equipos"': "EQUIPOS", '"version"': "VERSION", '"firma_digital"': "FIRMA_DIGITAL",
        '"nombre_equipo"': "NOMBRE_EQ", '"identidad_equipo"': "IDENTIDAD_EQ", '"link"': "LINK",
        '"asignatura"': "ASIGNATURA", '"carrera"': "CARRERA", '"universidad_regional"': "UNIVERSIDAD_REG",
        '"dirección"': "DIRECCION", '"alianza_equipo"': "ALIANZA_EQ",'"nombre"': "NOMBRE", '"nombre_proy"': "NOMBRE_PROY",
        '"edad"': "EDAD", '"cargo"': "CARGO", '"foto"': "FOTO", '"email"': "EMAIL",
        '"habilidades"': "HABILIDADES", '"salario"': "SALARIO", '"activo"': "ACTIVO",
        '"proyectos"': "PROYECTOS", '"estado_proy"': "ESTADO_PROY", '"resumen"': "RESUMEN_PROY",
        '"tareas"': "TAREAS_PROY", '"fecha_inicio"': "FECHA_INICIO", '"fecha_fin"': "FECHA_FIN",
        '"video"': "VIDEO_PROY", '"conclusion"': "CONCLUSION_PROY"
    }
    if t.value in palabras_reservadas:
        t.type = palabras_reservadas[t.value]
    return t

def t_FLOAT(t):
    r'\d+\.\d{1,2}'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'-?\d+'
    t.value = int(t.value)
    return t

def t_BOOLEAN(t):
    r'(true|false)'
    t.value = True if t.value == 'true' else False
    return t

def t_NULL(t):
    r'null'
    return t

def t_error(t):
    print(f"❌ Error léxico: símbolo no permitido '{t.value[0]}' en la línea {t.lineno}")
    t.lexer.skip(1)


lexer = lex.lex()
lexer.lineno = 1  # ← IMPORTANTE para que el parser tenga línea correcta

while True:
    try:
        opcion = input("Ingrese 1 para análisis interactivo, 2 para análisis de archivo:\n").strip()
        if opcion in ["1", "2"]:
            break
        print(f"❌ Opción inválida: '{opcion}'. Solo se acepta '1' o '2'.")
    except EOFError:
        print("\nSaliendo del programa.")
        sys.exit(0)

archivo = ""
if opcion == "2":
    try:
        archivo = input("Ingrese el nombre del archivo JSON (sin extensión):\n").strip()
    except EOFError:
        print("\nSaliendo del programa.")
        sys.exit(0)

    if not archivo.endswith(".json"):
        archivo += ".json"

# Guardar opción y archivo en modo.txt
with open("modo.txt", "w") as f:
    f.write(f"{opcion}\n{archivo}")

# Ejecutar según modo
if opcion == "2":
    if not os.path.isfile(archivo):
        print(f"[ERROR] El archivo '{archivo}' no existe.")
        sys.exit(1)

    with open(archivo, 'r', encoding='utf-8') as f:
        data = f.read()

    print("--- ANÁLISIS DEL ARCHIVO JSON ---")
    lexer.input(data)
    for tok in lexer:
        print(f"Se encontró el token '{tok.value}' de tipo {tok.type}")
    print("----------------------------------\n")
    print("Análisis del archivo JSON completado.")
    print("Presiona 'Ctrl + Z' (Windows) o 'Ctrl + D' (Linux/macOS) y luego Enter para salir.")
    try:
        while True:
            input()
    except EOFError:
        print("\nSaliendo del programa.")
else:
    print("Modo interactivo: Ingresa palabras para ver si son tokens.")
    print("------------------------------")
    print("Para salir, presiona 'Ctrl + Z' (Windows) o 'Ctrl + D' (Linux/macOS) y luego Enter.")
    try:
        while True:
            palabra = input(">> ").strip()
            if not palabra:
                continue
            lexer.input(palabra)
            tok = lexer.token()
            if tok and not lexer.token():
                print(f"'{palabra}' es un **TOKEN**: {tok.type} (Valor: {tok.value})")
            else:
                print(f"'{palabra}' **NO** es un token reconocido.")
    except EOFError:
        print("\nSaliendo del programa.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        input("\nPresiona Enter para salir...")

input("\nPresiona Enter para salir...")
