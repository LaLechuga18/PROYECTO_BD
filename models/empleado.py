# models/empleado.py
from db import conectar_db

def get_all():
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM empleado")
    filas = cur.fetchall()
    cols = [d[0] for d in cur.description]
    cur.close(); conn.close()
    return filas, cols

def insertar(datos: tuple):
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO empleado "
        "(codigo, nombre, direccion, telefono, fecha_nac, sexo, sueldo, turno, contraseña) "
        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        datos
    )
    conn.commit()
    cur.execute("SELECT * FROM empleado WHERE codigo = %s", (datos[0],))
    nuevo = cur.fetchone()
    cur.close(); conn.close()
    return nuevo

def eliminar(codigo):
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM empleado WHERE codigo = %s", (codigo,))
    conn.commit()
    cur.close(); conn.close()

def verificar_login(codigo, contrasena):
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT codigo, nombre FROM empleado WHERE codigo = %s AND contraseña = %s",
        (codigo, contrasena)
    )
    resultado = cur.fetchone()
    cur.close(); conn.close()
    return resultado