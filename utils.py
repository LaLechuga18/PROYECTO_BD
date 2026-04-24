# utils.py
from tkinter import ttk
from tkinter import PhotoImage

ICONO_PATH = "server-storage.png"

def set_icono(ventana):
    icono = PhotoImage(file=ICONO_PATH)
    ventana.iconphoto(True, icono)
    ventana._icono = icono  # evita que el GC lo elimine

def crear_treeview(parent, columnas):
    tabla = ttk.Treeview(parent, columns=columnas, show="headings")
    tabla.pack(expand=True, fill="both")
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=100)
    return tabla

def poblar_treeview(tabla, filas):
    tabla.delete(*tabla.get_children())
    for fila in filas:
        tabla.insert("", "end", values=fila)