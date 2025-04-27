import re
import ply.lex as lex


tokens = ( 
         "CORCHETE_I", "CORCHETE_D",
         "LLAVE_I", "LLAVE_D",
         "COMA", "COMILLA", "DOSPUNTOS",
         
        "EQUIPOS", "VERSION", "FIRMA_DIGITAL",
        "NOMBRE_EQ", "IDENTIDAD_EQ", "LINK", "ASIGNATURA", "CARRERA",
        "UNIVERSIDAD_REG", "DIRECCION","ALIANZA_EQ"
        
        "NOMBRE", "EDAD", "CARGO", "FOTO", "EMAIL", "HABILIDADES", "SALARIO", "ACTIVO"
        
        "PROYECTOS", "NOMBRE_PROY", "ESTADO_PROY", "RESUMEN_PROY", "TAREAS_PROY", "FECHA_INICIO",
        "FECHA_FIN", "VIDEO_PROY", "CONCLUSION_PROY"
        
        "FECHA", "NULL", "ENTERO", "FLOAT", "BOOLEANO", "URL", "STRING"
         )
t_COMILLA = r'\"'
t_CORCHETE_I = r'\['
t_CORCHETE_D = r'\]'
t_LLAVE_I = r'\{'
t_LLAVE_D = r'\}'
t_COMA = r','
t_DOSPUNTOS = r':'

