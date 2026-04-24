# models/cita.py
from db import conectar_db

def get_all():
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM cita")
    filas = cur.fetchall()
    cols = [d[0] for d in cur.description]
    cur.close(); conn.close()
    return filas, cols

def get_by_doctor(codigo_doctor):
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT id_cita, codigo_paciente, fecha, hora FROM cita "
        "WHERE codigo_doctor = %s ORDER BY fecha, hora",
        (codigo_doctor,)
    )
    filas = cur.fetchall()
    cols = [d[0] for d in cur.description]
    cur.close(); conn.close()
    return filas, cols

def insertar(datos: tuple):
    """datos = (id_cita, codigo_paciente, codigo_doctor, fecha, hora)"""
    conn = conectar_db()
    cur = conn.cursor()
    # Verificar conflicto de horario
    cur.execute(
        "SELECT 1 FROM cita WHERE codigo_doctor = %s AND fecha = %s AND hora = %s",
        (datos[2], datos[3], datos[4])
    )
    if cur.fetchone():
        cur.close(); conn.close()
        raise ValueError("El doctor ya tiene una cita en esa fecha y hora.")
    cur.execute(
        "INSERT INTO cita (id_cita, codigo_paciente, codigo_doctor, fecha, hora) "
        "VALUES (%s,%s,%s,%s,%s)",
        datos
    )
    conn.commit()
    cur.execute("SELECT * FROM cita WHERE id_cita = %s", (datos[0],))
    nueva = cur.fetchone()
    cur.close(); conn.close()
    return nueva

def actualizar(id_cita, codigo_doctor, codigo_paciente, fecha, hora):
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE cita SET codigo_doctor=%s, codigo_paciente=%s, fecha=%s, hora=%s "
        "WHERE id_cita = %s",
        (codigo_doctor, codigo_paciente, fecha, hora, id_cita)
    )
    conn.commit()
    cur.close(); conn.close()

def eliminar(id_cita):
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM cita WHERE id_cita = %s", (id_cita,))
    conn.commit()
    cur.close(); conn.close()