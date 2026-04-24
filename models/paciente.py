# models/paciente.py
from db import conectar_db

def get_all():
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM paciente")
    filas = cur.fetchall()
    cols = [d[0] for d in cur.description]
    cur.close(); conn.close()
    return filas, cols

def insertar(datos: tuple):
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO paciente "
        "(codigo, nombre, direccion, telefono, fecha_nac, sexo, edad, estatura) "
        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
        datos
    )
    conn.commit()
    cur.execute("SELECT * FROM paciente WHERE codigo = %s", (datos[0],))
    nuevo = cur.fetchone()
    cur.close(); conn.close()
    return nuevo

def eliminar(codigo):
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM paciente WHERE codigo = %s", (codigo,))
    conn.commit()
    cur.close(); conn.close()

def get_lista():
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("SELECT codigo, nombre FROM paciente")
    lista = cur.fetchall()
    cur.close(); conn.close()
    return lista