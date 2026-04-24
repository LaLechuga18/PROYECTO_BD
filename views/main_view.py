# views/main_view.py
from tkinter import *
from PIL import Image, ImageTk
from utils import set_icono

class MainView(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.geometry("500x400")
        self.title("Sistema Base de Datos")
        self.configure(bg="#133E87")
        set_icono(self)
        self.protocol("WM_DELETE_WINDOW", self._cerrar)
        self._build_ui()

    def _build_ui(self):
        from PROYECTO_BD.views.empleados_view import EmpleadosTableView
        from PROYECTO_BD.views.doctores_view import DoctoresTableView
        from PROYECTO_BD.views.pacientes_view import PacientesView
        from PROYECTO_BD.views.citas_view import CitasView
        from PROYECTO_BD.views.medicamentos_view import MedicamentosView

        frame = Frame(self)
        frame.pack(side="top", fill="x")

        botones = [
            ("Empleados",    "#0E2954", lambda: EmpleadosTableView(self)),
            ("Doctores",     "#1F6E8C", lambda: DoctoresTableView(self)),
            ("Pacientes",    "#2E8A99", lambda: PacientesView(self)),
            ("Citas",        "#84A7A1", lambda: CitasView(self)),
            ("Medicamentos", "#15B392", lambda: MedicamentosView(self)),
        ]
        for texto, color, cmd in botones:
            Button(frame, text=texto, command=cmd,
                   background=color, fg="White").pack(side="left", expand=True, fill="x")

        img = Image.open("database.png").resize((200, 200), Image.LANCZOS)
        self._img_tk = ImageTk.PhotoImage(img)
        Label(self, image=self._img_tk, bg="#133E87").pack(pady=20)

        Button(self, text="Cerrar", command=self._cerrar, bg="#FF004D").pack(pady=10)

    def _cerrar(self):
        self.destroy()
        self.parent.deiconify()