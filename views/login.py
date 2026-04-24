# views/login.py
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import models.empleado as empleado_model
import models.doctor as doctor_model
from utils import set_icono

class LoginView(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("400x400")
        self.title("Iniciar sesión")
        self.configure(bg="#133E87")
        set_icono(self)
        self._build_ui()

    def _build_ui(self):
        img = Image.open("unlocked.png").resize((150, 150), Image.LANCZOS)
        self._img_tk = ImageTk.PhotoImage(img)
        Label(self, image=self._img_tk, bg="#133E87").pack(pady=20)

        Label(self, text="USUARIO", bg="#133E87", fg="White").pack(pady=5)
        self.entry_usuario = ttk.Entry(self)
        self.entry_usuario.pack()

        Label(self, text="CONTRASEÑA", bg="#133E87", fg="White").pack(pady=5)
        self.entry_contra = ttk.Entry(self, show="*")
        self.entry_contra.pack()

        Button(self, text="Aceptar", command=self._login, bg="#00FF9C").pack(pady=10)
        Button(self, text="Cancelar", command=self.destroy, bg="#FF004D").pack(pady=5)

    def _login(self):
        user = self.entry_usuario.get()
        password = self.entry_contra.get()

        if user == "admin" and password == "1234":
            self._abrir(lambda: self._abrir_admin())
            return

        resultado_doctor = doctor_model.verificar_login(user, password)
        if resultado_doctor:
            codigo, nombre = resultado_doctor
            messagebox.showinfo("Bienvenido", f"Hola, Dr. {nombre.capitalize()}")
            self._abrir(lambda: self._abrir_doctor(nombre, codigo))
            return

        resultado_empleado = empleado_model.verificar_login(user, password)
        if resultado_empleado:
            codigo, nombre = resultado_empleado
            messagebox.showinfo("Bienvenido", f"Hola, {nombre.capitalize()}")
            self._abrir(lambda: self._abrir_empleado(nombre))
            return

        messagebox.showerror("Error", "Código o contraseña inválidos.")

    def _abrir(self, callback):
        self.withdraw()
        callback()

    def _abrir_admin(self):
        from PROYECTO_BD.views.main_view import MainView
        MainView(self)

    def _abrir_doctor(self, nombre, codigo):
        from PROYECTO_BD.views.doctores_view import DoctoresView
        DoctoresView(self, nombre, codigo)

    def _abrir_empleado(self, nombre):
        from PROYECTO_BD.views.empleados_view import EmpleadosView
        EmpleadosView(self, nombre)