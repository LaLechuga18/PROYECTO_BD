# views/pacientes_view.py
from tkinter import *
from tkinter import ttk
import models.paciente as model
from utils import set_icono, crear_treeview, poblar_treeview

class PacientesView(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Pacientes")
        self.configure(bg="#433878")
        set_icono(self)
        self._build_ui()

    def _build_ui(self):
        Label(self, text="Tabla de Pacientes", bg="#433878", fg="White").pack(pady=10)
        filas, cols = model.get_all()
        self.tabla = crear_treeview(self, cols)
        poblar_treeview(self.tabla, filas)

        Button(self, text="Añadir Paciente",   command=self._añadir,   bg="#00FF9C").pack(pady=5)
        Button(self, text="Eliminar Paciente", command=self._eliminar, bg="#F9E400").pack(pady=5)
        Button(self, text="Cerrar",            command=self.destroy,   bg="#FF004D").pack(pady=5)

    def _añadir(self):
        AñadirPacienteDialog(self, on_guardado=lambda row: self.tabla.insert("", "end", values=row))

    def _eliminar(self):
        sel = self.tabla.selection()
        if not sel:
            return
        codigo = self.tabla.item(sel)["values"][0]
        model.eliminar(codigo)
        self.tabla.delete(sel)


class AñadirPacienteDialog(Toplevel):
    def __init__(self, parent, on_guardado):
        super().__init__(parent)
        self.title("Añadir Paciente")
        self.geometry("300x400")
        self.on_guardado = on_guardado
        set_icono(self)
        self._build_ui()

    def _build_ui(self):
        campos = ["Codigo", "Nombre", "Direccion", "Telefono",
                  "Fecha Nacimiento", "Sexo", "Edad", "Estatura"]
        self.entries = {}
        for campo in campos:
            ttk.Label(self, text=campo).pack()
            e = ttk.Entry(self)
            e.pack()
            self.entries[campo] = e

        Button(self, text="Guardar", command=self._guardar, bg="#008DDA").pack(pady=10)
        Button(self, text="Cerrar",  command=self.destroy,  bg="#FF004D").pack(pady=5)

    def _guardar(self):
        datos = tuple(e.get() for e in self.entries.values())
        nuevo = model.insertar(datos)
        if nuevo:
            self.on_guardado(nuevo)
        self.destroy()