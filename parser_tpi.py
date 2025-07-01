import ply.yacc as yacc
from lexer_puro import tokens

start = 'JSON'

equipo_info = {}
integrantes = []
proyectos = []

def p_JSON(p):
    '''JSON : LLAVE_I EQUIPOS_DEF COMA VERSION_DEF COMA FIRMA_DEF LLAVE_D'''
    generar_html()

def p_EQUIPOS_DEF(p):
    '''EQUIPOS_DEF : EQUIPOS DOSPUNTOS CORCHETE_I EQUIPO CORCHETE_D'''

def p_EQUIPO(p):
    '''EQUIPO : LLAVE_I NOMBRE_EQ_DEF COMA IDENTIDAD_EQ_DEF COMA LINK_DEF COMA ASIGNATURA_DEF COMA CARRERA_DEF COMA UNIVERSIDAD_DEF COMA DIRECCION_DEF COMA ALIANZA_DEF COMA INTEGRANTES_DEF COMA PROYECTOS_DEF LLAVE_D'''

def p_NOMBRE_EQ_DEF(p):
    '''NOMBRE_EQ_DEF : NOMBRE_EQ DOSPUNTOS STRING'''
    equipo_info["nombre"] = p[3].strip('"')

def p_IDENTIDAD_EQ_DEF(p):
    '''IDENTIDAD_EQ_DEF : IDENTIDAD_EQ DOSPUNTOS URL'''
    equipo_info["logo"] = p[3].strip('"')

def p_LINK_DEF(p):
    '''LINK_DEF : LINK DOSPUNTOS URL'''
    equipo_info["link"] = p[3].strip('"')

def p_ASIGNATURA_DEF(p):
    '''ASIGNATURA_DEF : ASIGNATURA DOSPUNTOS STRING'''
    equipo_info["asignatura"] = p[3].strip('"')

def p_CARRERA_DEF(p):
    '''CARRERA_DEF : CARRERA DOSPUNTOS STRING'''
    equipo_info["carrera"] = p[3].strip('"')

def p_UNIVERSIDAD_DEF(p):
    '''UNIVERSIDAD_DEF : UNIVERSIDAD_REG DOSPUNTOS STRING'''
    equipo_info["universidad"] = p[3].strip('"')

def p_DIRECCION_DEF(p):
    '''DIRECCION_DEF : DIRECCION DOSPUNTOS LLAVE_I STRING DOSPUNTOS STRING COMA STRING DOSPUNTOS STRING COMA STRING DOSPUNTOS STRING LLAVE_D'''
    equipo_info["direccion"] = {
        "calle": p[6].strip('"'),
        "ciudad": p[10].strip('"'),
        "pais": p[14].strip('"')
    }

def p_ALIANZA_DEF(p):
    '''ALIANZA_DEF : ALIANZA_EQ DOSPUNTOS STRING'''
    equipo_info["alianza"] = p[3].strip('"')

def p_INTEGRANTES_DEF(p):
    '''INTEGRANTES_DEF : INTEGRANTES DOSPUNTOS CORCHETE_I INTEGRANTE_LISTA CORCHETE_D'''

def p_INTEGRANTE_LISTA(p):
    '''INTEGRANTE_LISTA : INTEGRANTE COMA INTEGRANTE_LISTA
                        | INTEGRANTE'''

def p_INTEGRANTE(p):
    '''INTEGRANTE : LLAVE_I \
NOMBRE DOSPUNTOS STRING COMA \
EDAD DOSPUNTOS valor_entero COMA \
CARGO DOSPUNTOS STRING COMA \
FOTO DOSPUNTOS URL COMA \
EMAIL DOSPUNTOS STRING COMA \
HABILIDADES DOSPUNTOS STRING COMA \
SALARIO DOSPUNTOS FLOAT COMA \
ACTIVO DOSPUNTOS BOOLEAN \
LLAVE_D'''
    integrante = {
        "nombre": p[4].strip('"'),
        "edad": p[8],
        "cargo": p[12].strip('"'),
        "foto": p[16].strip('"'),
        "email": p[20].strip('"'),
        "habilidades": p[24].strip('"'),
        "salario": p[28],
        "activo": p[32]
    }
    integrantes.append(integrante)

def p_valor_entero(p):
    '''valor_entero : INTEGER
                    | STRING'''
    if isinstance(p[1], int):
        p[0] = p[1]
    else:
        p[0] = int(p[1].strip('"'))

def p_PROYECTOS_DEF(p):
    '''PROYECTOS_DEF : PROYECTOS DOSPUNTOS CORCHETE_I PROYECTO_LISTA CORCHETE_D'''

def p_PROYECTO_LISTA(p):
    '''PROYECTO_LISTA : PROYECTO COMA PROYECTO_LISTA
                      | PROYECTO'''

def p_PROYECTO(p):
    '''PROYECTO : LLAVE_I NOMBRE_PROY DOSPUNTOS STRING COMA ESTADO_PROY DOSPUNTOS STRING COMA RESUMEN_PROY DOSPUNTOS STRING COMA TAREAS_PROY DOSPUNTOS CORCHETE_I TAREA_LISTA CORCHETE_D COMA FECHA_INICIO DOSPUNTOS FECHA_VALOR COMA FECHA_FIN DOSPUNTOS FECHA_VALOR COMA VIDEO_PROY DOSPUNTOS STRING COMA CONCLUSION_PROY DOSPUNTOS STRING LLAVE_D'''
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

def p_TAREA_LISTA(p):
    '''TAREA_LISTA : TAREA COMA TAREA_LISTA
                   | TAREA'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_TAREA(p):
    '''TAREA : LLAVE_I NOMBRE DOSPUNTOS STRING COMA ESTADO_PROY DOSPUNTOS STRING COMA RESUMEN_PROY DOSPUNTOS STRING COMA FECHA_INICIO DOSPUNTOS FECHA_VALOR COMA FECHA_FIN DOSPUNTOS FECHA_VALOR LLAVE_D'''
    tarea = {
        "nombre": p[4].strip('"'),
        "estado": p[8].strip('"'),
        "resumen": p[12].strip('"'),
        "fecha_inicio": p[16].strip('"'),
        "fecha_fin": p[20].strip('"')
    }
    p[0] = tarea

def p_VERSION_DEF(p):
    '''VERSION_DEF : VERSION DOSPUNTOS STRING'''
    equipo_info["version"] = p[3].strip('"')

def p_FIRMA_DEF(p):
    '''FIRMA_DEF : FIRMA_DIGITAL DOSPUNTOS STRING'''
    equipo_info["firma"] = p[3].strip('"')

def p_error(p):
    if p:
        print(f"❌ Error de sintaxis en token '{p.value}' (tipo: {p.type})")
    else:
        print("❌ Error de sintaxis: fin inesperado del archivo")

parser = yacc.yacc()

def generar_html():
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>{equipo_info.get("nombre", "Equipo")}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f7f7f7; }}
        h1 {{ color: #007acc; }}
        .integrante, .proyecto {{ border: 1px solid #ccc; padding: 10px; margin-bottom: 10px; background: #fff; }}
        .foto {{ width: 100px; }}
    </style>
</head>
<body>
    <h1>{equipo_info.get("nombre", "")}</h1>
    <p><strong>Asignatura:</strong> {equipo_info.get("asignatura", "")}</p>
    <p><strong>Carrera:</strong> {equipo_info.get("carrera", "")}</p>
    <p><strong>Universidad:</strong> {equipo_info.get("universidad", "")}</p>
    <p><strong>Dirección:</strong> {equipo_info.get("direccion", {}).get("calle", "")}, {equipo_info.get("direccion", {}).get("ciudad", "")}, {equipo_info.get("direccion", {}).get("pais", "")}</p>
    <p><strong>Link:</strong> <a href="{equipo_info.get("link", "")}">{equipo_info.get("link", "")}</a></p>
    <p><strong>Identidad visual:</strong></p>
    <img src="{equipo_info.get("logo", "")}" alt="Identidad visual" class="foto">
    <h2>Alianza del equipo</h2>
    <p>{equipo_info.get("alianza", "")}</p>
    <h2>Integrantes</h2>
"""
    for i in integrantes:
        html += f"""
    <div class="integrante">
        <img src="{i["foto"]}" class="foto">
        <p><strong>Nombre:</strong> {i["nombre"]}</p>
        <p><strong>Edad:</strong> {i["edad"]}</p>
        <p><strong>Cargo:</strong> {i["cargo"]}</p>
        <p><strong>Email:</strong> {i["email"]}</p>
        <p><strong>Habilidades:</strong> {i["habilidades"]}</p>
    </div>"""

    html += "<h2>Proyectos</h2>"
    for p in proyectos:
        html += f"""
        <div class="proyecto">
            <h3>{p["nombre"]}</h3>
            <p><strong>Estado:</strong> {p["estado"]}</p>
            <p>{p["resumen"]}</p>
            <p><strong>Tareas:</strong></p>
            <ul style="margin-left: 20px;">
        """
        for t in p["tareas"]:
            html += f"""
            <li>
                <strong> {t['nombre']} - {t['estado']}</strong><br>
                <span style="margin-left: 10px;">{t['resumen']}<br>
                Desde {t['fecha_inicio']} hasta {t['fecha_fin']}</span>
            </li>
        """
        html += f"""
            </ul>
            <p><strong>Inicio:</strong> {p["fecha_inicio"]}</p>
            <p><strong>Fin:</strong> {p["fecha_fin"]}</p>
            <p><strong>Video:</strong> {p["video"]}</p>
            <p><strong>Conclusión:</strong> {p["conclusion"]}</p>
        </div>
        """
        
        html += f"""
            <hr>
            <p><strong>Versión:</strong> {equipo_info.get("version", "")}</p>
            <p><strong>Firma digital:</strong> {equipo_info.get("firma", "")}</p>
        """

    with open("turing_version.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ HTML generado en 'salida.html'")

if __name__ == '__main__':
    with open('turing_version_base.json', 'r', encoding='utf-8') as f:
        contenido = f.read()
    parser.parse(contenido)
