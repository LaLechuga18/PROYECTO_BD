# views/doctores_view.py
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import models.doctor as model
from utils import set_icono, crear_treeview, poblar_treeview
from PROYECTO_BD.views.citas_view import CitasView
from PROYECTO_BD.views.medicamentos_view import MedicamentosView

class DoctoresTableView(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Doctores")
        self.configure(bg="#133E87")
        set_icono(self)
        self._build_ui()

    def _build_ui(self):
        Label(self, text="Tabla de Doctores", bg="#133E87", fg="White").pack(pady=10)
        filas, cols = model.get_all()
        self.tabla = crear_treeview(self, cols)
        poblar_treeview(self.tabla, filas)

        Button(self, text="Añadir Doctor",   command=self._añadir,   bg="#00FF9C").pack(pady=5)
        Button(self, text="Eliminar Doctor", command=self._eliminar, bg="#F9E400").pack(pady=5)
        Button(self, text="Cerrar",          command=self.destroy,   bg="#FF004D").pack(pady=5)

    def _añadir(self):
        AñadirDoctorDialog(self, on_guardado=lambda row: self.tabla.insert("", "end", values=row))

    def _eliminar(self):
        sel = self.tabla.selection()
        if not sel:
            return
        codigo = self.tabla.item(sel)["values"][0]
        model.eliminar(codigo)
        self.tabla.delete(sel)


class AñadirDoctorDialog(Toplevel):
    def __init__(self, parent, on_guardado):
        super().__init__(parent)
        self.title("Añadir Doctor")
        self.geometry("300x400")
        self.on_guardado = on_guardado
        set_icono(self)
        self._build_ui()

    def _build_ui(self):
        campos = ["Codigo", "Nombre", "Direccion", "Telefono",
                  "Fecha Nacimiento", "Sexo", "Especialidad", "Contraseña"]
        self.entries = {}
        for campo in campos:
            ttk.Label(self, text=campo).pack()
            e = ttk.Entry(self, show="*" if campo == "Contraseña" else "")
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


class DoctoresView(Toplevel):
    """Ventana personal del doctor tras hacer login."""
    def __init__(self, parent, nombre, codigo):
        super().__init__(parent)
        self.parent  = parent
        self.nombre  = nombre
        self.codigo  = codigo
        self.geometry("500x400")
        self.title("Doctores")
        self.configure(bg="#1D2D50")
        set_icono(self)
        self.protocol("WM_DELETE_WINDOW", self._cerrar)
        self._build_ui()

    def _build_ui(self):
        Label(self, text=f"Hola Dr. {self.nombre}!", bg="#1D2D50",
              font=("Arial", 12), fg="White", anchor="w").pack(fill="x")

        frame = Frame(self)
        frame.pack(side="top", fill="x")

        Button(frame, text="Citas",
               command=lambda: CitasView(self, codigo_doctor=self.codigo),
               bg="#590995", fg="White").pack(side="left", expand=True, fill="x")
        Button(frame, text="Medicamentos",
               command=lambda: MedicamentosView(self),
               bg="#117554", fg="White").pack(side="left", expand=True, fill="x")

        img = Image.open("caduceus.png").resize((200, 200), Image.LANCZOS)
        self._img_tk = ImageTk.PhotoImage(img)
        Label(self, image=self._img_tk, bg="#1D2D50").pack(pady=20)

        Button(self, text="Cerrar", command=self._cerrar, bg="#FF004D").pack(pady=10)

    def _cerrar(self):
        self.destroy()
        self.parent.deiconify()