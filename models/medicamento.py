# models/medicamento.py
from db import conectar_db

def get_all():
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM medicamento")
    filas = cur.fetchall()
    cols = [d[0] for d in cur.description]
    cur.close(); conn.close()
    return filas, cols

def insertar(datos: tuple):
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO medicamento "
        "(codigo, nombre, via_adm, presentacion, fecha_cad) "
        "VALUES (%s,%s,%s,%s,%s)",
        datos
    )
    conn.commit()
    cur.execute("SELECT * FROM medicamento WHERE codigo = %s", (datos[0],))
    nuevo = cur.fetchone()
    cur.close(); conn.close()
    return nuevo

def eliminar(codigo):
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM medicamento WHERE codigo = %s", (codigo,))
    conn.commit()
    cur.close(); conn.close()