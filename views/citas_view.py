# views/citas_view.py
from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import models.cita as model
import models.doctor as doctor_model
import models.paciente as paciente_model
from utils import set_icono, crear_treeview, poblar_treeview

CALENDAR_OPTS = dict(
    selectmode="day", year=2024, month=11,
    showweeknumbers=False, locale="es", date_pattern="dd/mm/yyyy",
    background="#B1D690", foreground="black",
    selectbackground="blue", selectforeground="white",
    weekendbackground="lightgrey", weekendforeground="white",
    normalbackground="white", normalforeground="black",
    font=("Arial", 12), headerfont=("Arial", 14, "bold"),
    headersbackground="#88C273", headersforeground="black",
)

class CitasView(Toplevel):
    def __init__(self, parent, codigo_doctor=None):
        super().__init__(parent)
        self.codigo_doctor = codigo_doctor
        self.title("Citas")
        self.configure(bg="#433878")
        set_icono(self)
        self._build_ui()

    def _build_ui(self):
        Label(self, text="Tabla de Citas", bg="#433878", fg="White").pack(pady=10)

        if self.codigo_doctor:
            filas, cols = model.get_by_doctor(self.codigo_doctor)
        else:
            filas, cols = model.get_all()

        self.tabla = crear_treeview(self, cols)
        poblar_treeview(self.tabla, filas)

        self._build_calendario(filas)

        if not self.codigo_doctor:
            Button(self, text="Modificar Cita", command=self._modificar, bg="#008DDA").pack(pady=5)
            Button(self, text="Añadir Cita",    command=self._añadir,    bg="#00FF9C").pack(pady=5)
            Button(self, text="Eliminar Cita",  command=self._eliminar,  bg="#F9E400").pack(pady=5)

        Button(self, text="Cerrar", command=self.destroy, bg="#FF004D").pack(pady=5)

    def _build_calendario(self, filas):
        frame = Frame(self)
        frame.pack(pady=20)
        self.cal = Calendar(frame, **CALENDAR_OPTS)
        self.cal.pack()
        self.cal.tag_config("cita", background="#008DDA", foreground="black")
        for fila in filas:
            self.cal.calevent_create(fila[3], "Cita", "cita")

    def _añadir(self):
        AñadirCitaDialog(self, on_guardado=lambda row: self.tabla.insert("", "end", values=row))

    def _eliminar(self):
        sel = self.tabla.selection()
        if not sel:
            return
        cita_id = self.tabla.item(sel)["values"][0]
        model.eliminar(cita_id)
        self.tabla.delete(sel)

    def _modificar(self):
        sel = self.tabla.selection()
        if not sel:
            return
        datos = self.tabla.item(sel)["values"]
        ModificarCitaDialog(self, datos, self.tabla)


class AñadirCitaDialog(Toplevel):
    def __init__(self, parent, on_guardado):
        super().__init__(parent)
        self.title("Añadir Cita")
        self.geometry("300x400")
        self.on_guardado = on_guardado
        set_icono(self)
        self._build_ui()

    def _build_ui(self):
        pacientes = paciente_model.get_lista()
        doctores  = doctor_model.get_lista()

        ttk.Label(self, text="ID de Cita").pack()
        self.entry_id = ttk.Entry(self)
        self.entry_id.pack()

        ttk.Label(self, text="Paciente").pack()
        self.combo_pac = ttk.Combobox(self, values=[f"{c} - {n}" for c, n in pacientes])
        self.combo_pac.pack()

        ttk.Label(self, text="Doctor").pack()
        self.combo_doc = ttk.Combobox(self, values=[f"{c} - {n}" for c, n in doctores])
        self.combo_doc.pack()

        ttk.Label(self, text="Fecha").pack()
        self.entry_fecha = ttk.Entry(self)
        self.entry_fecha.pack()

        ttk.Label(self, text="Hora").pack()
        self.entry_hora = ttk.Entry(self)
        self.entry_hora.pack()

        Button(self, text="Guardar", command=self._guardar, bg="#008DDA").pack(pady=10)
        Button(self, text="Cerrar",  command=self.destroy,  bg="#FF004D").pack(pady=5)

    def _guardar(self):
        id_cita = self.entry_id.get()
        pac     = self.combo_pac.get().split(" - ")[0]
        doc     = self.combo_doc.get().split(" - ")[0]
        fecha   = self.entry_fecha.get()
        hora    = self.entry_hora.get()

        if not all([id_cita, pac, doc, fecha, hora]):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        try:
            nueva = model.insertar((id_cita, pac, doc, fecha, hora))
            if nueva:
                self.on_guardado(nueva)
            self.destroy()
        except ValueError as e:
            messagebox.showerror("Conflicto", str(e))


class ModificarCitaDialog(Toplevel):
    def __init__(self, parent, datos, tabla):
        super().__init__(parent)
        self.title("Modificar Cita")
        self.geometry("300x400")
        self.datos  = datos
        self.tabla  = tabla
        self._build_ui()

    def _build_ui(self):
        doctores  = doctor_model.get_lista()
        pacientes = paciente_model.get_lista()

        ttk.Label(self, text="Doctor").pack()
        self.combo_doc = ttk.Combobox(self, values=[f"{c} - {n}" for c, n in doctores])
        self.combo_doc.set(str(self.datos[1]))
        self.combo_doc.pack()

        ttk.Label(self, text="Paciente").pack()
        self.combo_pac = ttk.Combobox(self, values=[f"{c} - {n}" for c, n in pacientes])
        self.combo_pac.set(str(self.datos[2]))
        self.combo_pac.pack()

        ttk.Label(self, text="Fecha").pack()
        self.entry_fecha = ttk.Entry(self)
        self.entry_fecha.insert(0, self.datos[3])
        self.entry_fecha.pack()

        ttk.Label(self, text="Hora").pack()
        self.entry_hora = ttk.Entry(self)
        self.entry_hora.insert(0, self.datos[4])
        self.entry_hora.pack()

        Button(self, text="Guardar", command=self._guardar, bg="#008DDA").pack(pady=10)
        Button(self, text="Cerrar",  command=self.destroy,  bg="#FF004D").pack(pady=5)

    def _guardar(self):
        doc   = self.combo_doc.get().split(" - ")[0]
        pac   = self.combo_pac.get().split(" - ")[0]
        fecha = self.entry_fecha.get()
        hora  = self.entry_hora.get()

        if not all([doc, pac, fecha, hora]):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        try:
            id_cita = self.datos[0]
            model.actualizar(id_cita, doc, pac, fecha, hora)
            for item in self.tabla.get_children():
                if self.tabla.item(item)["values"][0] == id_cita:
                    self.tabla.item(item, values=(id_cita, doc, pac, fecha, hora))
            messagebox.showinfo("Éxito", "Cita actualizada.")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))