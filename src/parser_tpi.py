import ply.yacc as yacc
from lexer_puro import tokens
import lexer_puro
import sys
import os

start = 'JSON'

equipo_info = {}
integrantes = []
proyectos = []

try:
    with open("modo.txt", "r") as f:
        lineas = f.read().strip().splitlines()
        opcion = lineas[0].strip()
        nombre_json = lineas[1].strip() if len(lineas) > 1 else ""
except FileNotFoundError:
    print("\u26a0 No se encontr\u00f3 'modo.txt'. Asumiendo modo interactivo.")
    opcion = "1"
    nombre_json = ""

if opcion not in ["1", "2"]:
    print(f"❌ Valor inválido en 'modo.txt': '{opcion}'. Solo se acepta '1' (interactivo) o '2' (archivo).")
    sys.exit(1)

crear_html = opcion == "2"

nombre_html = os.path.splitext(nombre_json)[0] + ".html" if crear_html else ""

if crear_html:
    try:
        salida_html = open(nombre_html, "w", encoding="utf-8")
    except Exception as e:
        print(f"❌ No se pudo crear el archivo HTML: {e}")
        sys.exit(1)

    salida_html.write("""<!DOCTYPE html>
<html lang=\"es\">
<head>
    <meta charset=\"UTF-8\">
    <title>Turing's Version</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f7f7f7; }
        h1 { color: #007acc; }
        .integrante, .proyecto { border: 1px solid #ccc; padding: 10px; margin-bottom: 10px; background: #fff; }
        .foto { width: 100px; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; background: #fff; }
        th { background-color: #007acc; color: white; }
        td, th { border: 1px solid #ccc; padding: 8px; text-align: left; }
    </style>
</head>
<body>
""")

def escribir_html(texto):
    if crear_html:
        salida_html.write(texto + "\n")

def p_JSON(p):
    '''JSON : LLAVE_I EQUIPOS_DEF COMA VERSION_OPT FIRMA_OPT LLAVE_D'''
    escribir_html('</div>')
    escribir_html("<hr>")
    if equipo_info.get("version"):
        escribir_html(f"<p><strong>Versi\u00f3n:</strong> {equipo_info['version']}</p>")
    if equipo_info.get("firma"):
        escribir_html(f"<p><strong>Firma digital:</strong> {equipo_info['firma']}</p>")
    escribir_html("</body>\n</html>")
    if crear_html:
        salida_html.close()

def p_EQUIPOS_DEF(p):
    '''EQUIPOS_DEF : EQUIPOS DOSPUNTOS CORCHETE_I EQUIPO CORCHETE_D'''

def p_EQUIPO(p):
    '''EQUIPO : LLAVE_I NOMBRE_EQ_DEF COMA IDENTIDAD_EQ_DEF COMA LINK_OPT ASIGNATURA_DEF COMA CARRERA_DEF COMA UNIVERSIDAD_DEF COMA DIRECCION_OPT ALIANZA_DEF COMA INTEGRANTES_DEF COMA PROYECTOS_DEF LLAVE_D'''

def p_LINK_OPT(p):
    '''LINK_OPT : LINK_DEF COMA
                | empty'''

def p_LINK_DEF(p):
    '''LINK_DEF : LINK DOSPUNTOS URL'''
    equipo_info["link"] = p[3].strip('"')
    escribir_html(f'<p><strong>Link:</strong> <a href="{equipo_info["link"]}">{equipo_info["link"]}</a></p>')

def p_empty(p):
    'empty :'
    pass

def p_ASIGNATURA_DEF(p):
    '''ASIGNATURA_DEF : ASIGNATURA DOSPUNTOS STRING'''
    equipo_info["asignatura"] = p[3].strip('"')
    escribir_html(f"<p><strong>Asignatura:</strong> {equipo_info['asignatura']}</p>")

def p_NOMBRE_EQ_DEF(p):
    '''NOMBRE_EQ_DEF : NOMBRE_EQ DOSPUNTOS STRING'''
    equipo_info["nombre"] = p[3].strip('"')
    escribir_html(f"<h1>{equipo_info['nombre']}</h1>")

def p_IDENTIDAD_EQ_DEF(p):
    '''IDENTIDAD_EQ_DEF : IDENTIDAD_EQ DOSPUNTOS URL'''
    equipo_info["logo"] = p[3].strip('"')

def p_CARRERA_DEF(p):
    '''CARRERA_DEF : CARRERA DOSPUNTOS STRING'''
    equipo_info["carrera"] = p[3].strip('"')
    escribir_html(f"<p><strong>Carrera:</strong> {equipo_info['carrera']}</p>")

def p_UNIVERSIDAD_DEF(p):
    '''UNIVERSIDAD_DEF : UNIVERSIDAD_REG DOSPUNTOS STRING'''
    equipo_info["universidad"] = p[3].strip('"')
    escribir_html(f"<p><strong>Universidad:</strong> {equipo_info['universidad']}</p>")

def p_DIRECCION_OPT(p):
    '''DIRECCION_OPT : DIRECCION_DEF COMA
                     | empty'''
    pass

def p_DIRECCION_DEF(p):
    '''DIRECCION_DEF : DIRECCION DOSPUNTOS LLAVE_I CAMPOS_DIRECCION LLAVE_D'''
    direccion = {}
    for key, val in p[4]:
        direccion[key] = val
    equipo_info["direccion"] = direccion
    partes = [direccion.get("calle"), direccion.get("ciudad"), direccion.get("pais")]

    direccion_str = ", ".join([p for p in partes if p])
    escribir_html(f"<p><strong>Direcci\u00f3n:</strong> {direccion_str}</p>")

def p_CAMPOS_DIRECCION(p):
    '''CAMPOS_DIRECCION : CAMPO_DIRECCION COMA CAMPOS_DIRECCION
                        | CAMPO_DIRECCION'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_CAMPO_DIRECCION(p):
    '''CAMPO_DIRECCION : STRING DOSPUNTOS STRING'''
    p[0] = (p[1].strip('"'), p[3].strip('"'))

def p_CAMPO_DIRECCION_error(p):
    '''CAMPO_DIRECCION : error DOSPUNTOS STRING
                       | STRING DOSPUNTOS error'''
    print(f"❌ Error sintáctico en dirección en línea {p.lineno(1)}: campo mal escrito o valor inválido.")
    escribir_html(f"<p><strong>⚠ Error en dirección: campo mal escrito o valor inválido.</strong></p>")


def p_ALIANZA_DEF(p):
    '''ALIANZA_DEF : ALIANZA_EQ DOSPUNTOS STRING'''
    equipo_info["alianza"] = p[3].strip('"')
    escribir_html('<p><strong>Identidad visual:</strong></p>')
    escribir_html(f'<img src="{equipo_info.get("logo", "")}" alt="Identidad visual" class="foto">')
    escribir_html("<h2>Alianza del equipo</h2>")
    escribir_html(f"<p>{equipo_info['alianza']}</p>")
    escribir_html('<h2>Integrantes</h2>')
    escribir_html('<div class="integrantes">')


def p_INTEGRANTES_DEF(p):
    '''INTEGRANTES_DEF : INTEGRANTES DOSPUNTOS CORCHETE_I INTEGRANTE_LISTA CORCHETE_D'''
    escribir_html('</div>')
    escribir_html('<h2>Proyectos</h2>')

def p_INTEGRANTE_LISTA(p):
    '''INTEGRANTE_LISTA : INTEGRANTE COMA INTEGRANTE_LISTA
                        | INTEGRANTE'''
    pass

def p_EDAD_OPT(p):
    '''EDAD_OPT : EDAD DOSPUNTOS valor_entero COMA
                | empty
                | EDAD DOSPUNTOS empty COMA'''
    if len(p) == 5:
        p[0] = p[3]
    else:
        p[0] = None
        
def p_INTEGRANTE(p):
    '''INTEGRANTE : LLAVE_I \
NOMBRE DOSPUNTOS STRING COMA \
EDAD_OPT \
CARGO DOSPUNTOS STRING COMA \
FOTO DOSPUNTOS URL COMA \
EMAIL DOSPUNTOS EMAIL COMA \
HABILIDADES DOSPUNTOS STRING COMA \
SALARIO DOSPUNTOS FLOAT COMA \
ACTIVO DOSPUNTOS BOOLEAN \
LLAVE_D'''

    nombre = p[4].strip('"')
    edad = p[6] 
    cargo     = p[9].strip('"')
    foto      = p[13].strip('"')
    email     = p[17].strip('"')
    habilidades = p[21].strip('"')
    salario   = p[25]
    activo    = p[29]

    integrante = {
        "nombre": nombre,
        "edad": edad,
        "cargo": cargo,
        "foto": foto,
        "email": email,
        "habilidades": habilidades,
        "salario": salario,
        "activo": activo
    }
    
    integrantes.append(integrante)

    escribir_html(f"""
    <div class="integrante">
        <img src="{foto}" class="foto">
        <p><strong>Nombre:</strong> {nombre}</p>""")
    if edad is not None:
        escribir_html(f"<p><strong>Edad:</strong> {edad}</p>")
    escribir_html(f"""<p><strong>Cargo:</strong> {cargo}</p>
        <p><strong>Email:</strong> {email}</p>
        <p><strong>Habilidades:</strong> {habilidades}</p>
        <p><strong>Salario:</strong> {salario}</p>
        <p><strong>Activo:</strong> {activo}</p>
    </div>""")

def p_valor_entero(p):
    '''valor_entero : INTEGER
                    | STRING
                    | empty'''
    if isinstance(p[1], int):
        p[0] = p[1]
    else:
        p[0] = int(p[1].strip('"'))

def p_PROYECTOS_DEF(p):
    '''PROYECTOS_DEF : PROYECTOS DOSPUNTOS CORCHETE_I PROYECTO_LISTA CORCHETE_D'''
    pass

def p_PROYECTO_LISTA(p):
    '''PROYECTO_LISTA : PROYECTO COMA PROYECTO_LISTA
                      | PROYECTO'''

def p_FECHA_INICIO_OPT(p):
    '''FECHA_INICIO_OPT : COMA FECHA_INICIO DOSPUNTOS FECHA_VALOR
                        | empty'''
    if len(p) == 5:
        p[0] = p[4].strip('"')
    else:
        p[0] = None

def p_FECHA_FIN_OPT(p):
    '''FECHA_FIN_OPT : COMA FECHA_FIN DOSPUNTOS FECHA_VALOR
                     | empty'''
    if len(p) == 5:
        p[0] = p[4].strip('"')
    else:
        p[0] = None

def p_PROYECTO(p):
    '''PROYECTO : LLAVE_I NOMBRE_PROY DOSPUNTOS STRING COMA ESTADO_PROY DOSPUNTOS STRING COMA RESUMEN_PROY DOSPUNTOS STRING COMA TAREAS_PROY DOSPUNTOS CORCHETE_I TAREA_LISTA CORCHETE_D COMA FECHA_INICIO DOSPUNTOS FECHA_VALOR COMA FECHA_FIN DOSPUNTOS FECHA_VALOR COMA VIDEO_PROY DOSPUNTOS URL COMA CONCLUSION_PROY DOSPUNTOS STRING LLAVE_D'''
    proyecto = {
        "nombre": p[4].strip('"'),
        "estado": p[8].strip('"'),
        "resumen": p[12].strip('"'),
        "tareas": p[17],
        "fecha_inicio": p[22].strip('"'),
        "fecha_fin": p[26].strip('"'),
        "video": p[30].strip('"'),
        "conclusion": p[34].strip('"')
    }
    proyectos.append(proyecto)

    escribir_html(f"""
    <div class="proyecto">
        <h3>{proyecto["nombre"]}</h3>
        <p><strong>Estado:</strong> {proyecto["estado"]}</p>
        <p>{proyecto["resumen"]}</p>
        <p><strong>Tareas:</strong></p>
        <table>
            <thead>
                <tr><th>Nombre</th><th>Estado</th><th>Resumen</th><th>Desde</th><th>Hasta</th></tr>
            </thead>
            <tbody>
    """)
    for t in proyecto["tareas"]:
        escribir_html(f"""
            <tr>
                <td>{t['nombre']}</td>
                <td>{t['estado']}</td>
                <td>{t['resumen']}</td>
                <td>{t['fecha_inicio'] if t['fecha_inicio'] else "-"}</td>
                <td>{t['fecha_fin'] if t['fecha_fin'] else "-"}</td>

            </tr>
        """)
    escribir_html(f"""
            </tbody>
        </table>
        <p><strong>Inicio:</strong> {proyecto["fecha_inicio"]}</p>
        <p><strong>Fin:</strong> {proyecto["fecha_fin"]}</p>
        <p><strong>Video:</strong> {proyecto["video"]}</p>
        <p><strong>Conclusión:</strong> {proyecto["conclusion"]}</p>
    </div>
    """)

def p_TAREA_LISTA(p):
    '''TAREA_LISTA : TAREA COMA TAREA_LISTA
                   | TAREA'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_TAREA(p):
    '''TAREA : LLAVE_I CAMPOS_TAREA LLAVE_D'''
    tarea = {
        "nombre": "",
        "estado": "",
        "resumen": "",
        "fecha_inicio": None,
        "fecha_fin": None
    }
    for key, val in p[2]:
        if key == "nombre":
            tarea["nombre"] = val
        elif key == "estado":
            tarea["estado"] = val
        elif key == "resumen":
            tarea["resumen"] = val
        elif key == "fecha_inicio":
            tarea["fecha_inicio"] = val
        elif key == "fecha_fin":
            tarea["fecha_fin"] = val
    p[0] = tarea
    
def p_CAMPOS_TAREA(p):
    '''CAMPOS_TAREA : CAMPO_TAREA COMA CAMPOS_TAREA
                    | CAMPO_TAREA'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]
    
def p_CAMPO_TAREA(p):
    '''CAMPO_TAREA : NOMBRE DOSPUNTOS STRING
                   | ESTADO_PROY DOSPUNTOS STRING
                   | RESUMEN_PROY DOSPUNTOS STRING
                   | FECHA_INICIO DOSPUNTOS FECHA_VALOR
                   | FECHA_FIN DOSPUNTOS FECHA_VALOR'''

    token_type = p.slice[1].type

    if token_type == "NOMBRE":
        clave = "nombre"
    elif token_type == "ESTADO_PROY":
        clave = "estado"
    elif token_type == "RESUMEN_PROY":
        clave = "resumen"
    elif token_type == "FECHA_INICIO":
        clave = "fecha_inicio"
    elif token_type == "FECHA_FIN":
        clave = "fecha_fin"
    else:
        clave = "?"

    valor = p[3].strip('"')
    p[0] = (clave, valor)
    
def p_VERSION_OPT(p):
    '''VERSION_OPT : VERSION_DEF COMA
                   | empty'''

def p_VERSION_DEF(p):
    '''VERSION_DEF : VERSION DOSPUNTOS STRING'''
    equipo_info["version"] = p[3].strip('"')

def p_FIRMA_OPT(p):
    '''FIRMA_OPT : FIRMA_DEF  
                 | empty'''

def p_FIRMA_DEF(p):
    '''FIRMA_DEF : FIRMA_DIGITAL DOSPUNTOS STRING'''
    equipo_info["firma"] = p[3].strip('"')

def p_error(p):
    if p:
        print(f"❌ Error sintáctico en línea {p.lineno}: token inválido '{p.value}' (tipo: {p.type})")
        escribir_html(f"<p><strong>⚠ Error de sintaxis en línea {p.lineno}: token '{p.value}'</strong></p>")
        input("\nPresiona Enter para salir...")
        input("\n")
    else:
        print("❌ Error sintáctico: fin inesperado del archivo.")
        escribir_html("<p><strong>⚠ Error de sintaxis: fin inesperado del archivo.</strong></p>")
        input("\nPresiona Enter para salir...")

    escribir_html("</body>\n</html>")
    if crear_html:
        salida_html.close()
    sys.exit(1)

parser = yacc.yacc()

if __name__ == '__main__':
    if crear_html:
        if not os.path.isfile(nombre_json):
            print(f"❌ Error de ejecución: el archivo '{nombre_json}' no existe.")
            sys.exit(1)

        if not nombre_json.endswith(".json"):
            print(f"❌ Error de ejecución: el archivo debe tener extensión .json (actual: '{nombre_json}').")
            sys.exit(1)

        try:
            with open(nombre_json, 'r', encoding='utf-8') as f:
                contenido = f.read()

            lexer_puro.lexer.lineno = 1  # Reiniciar contador de líneas
            parser.parse(contenido, lexer=lexer_puro.lexer)

            print(f"✅ Análisis completado. HTML generado en '{nombre_html}'.")
        except Exception as e:
            print(f"❌ Error al procesar el archivo: {e}")
            sys.exit(1)

    else:
        print("🛠 Modo interactivo activado. No se generará HTML.")
