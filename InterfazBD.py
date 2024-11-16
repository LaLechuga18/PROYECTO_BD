from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # LIBRERIA PARA IMPORTAR IMAGENES (pip install pillow)
import psycopg2  # Para la conexión a PostgreSQL
from psycopg2 import sql
from tkcalendar import Calendar #Descargar tkcalendar
from tkcalendar import DateEntry

#--------------------------------------BASE DE DATOS-----------------------------------------------
def conectar_db():
    # Conectar a la base de datos PostgreSQL
    conn = psycopg2.connect(
        dbname='Nucleo Diagnostico',  # Cambia por el nombre de tu base de datos
        user='postgres',  # Cambia por tu usuario
        password='SEBASTIAN18',  # Cambia por tu contraseña
        host='localhost',  # Cambia si tu servidor es diferente
    )
    return conn

#Funcion para limpiar los campos
def limpiar_campos():
    for widget in w.winfo_children():
        if isinstance(widget, Entry):
            widget.delete(0, 'end')
#---------------------------------------EMPLEADOS--------------------------------------------------
def mostrar_empleados():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM empleado")
    empleados = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()

    # Crear una nueva ventana para mostrar los empleados
    w_empleados = Toplevel()
    w_empleados.title("Empleados")
    w_empleados.configure(bg="#133E87")
    Label(w_empleados, text="Tabla de Empleados", bg="#133E87", fg="White").pack(pady=10)
    icono = PhotoImage(file="server-storage.png")
    w_empleados.iconphoto(True, icono)

    # Crear un Treeview para mostrar los datos
    tabla_empleados = ttk.Treeview(w_empleados, columns=column_names, show="headings")
    tabla_empleados.pack(expand=True, fill='both')

    # Configurar las columnas dinámicamente
    for col in column_names:
        tabla_empleados.heading(col, text=col)
        tabla_empleados.column(col, anchor='center', width=100)

    # Insertar los datos en el Treeview
    for empleado in empleados:
        tabla_empleados.insert("", "end", values=empleado)

    # Botón para añadir empleado
    añadir_btn = Button(w_empleados, text="Añadir Empleado", command=lambda: añadir_empleado(tabla_empleados),bg="#00FF9C")
    añadir_btn.pack(pady=5)

    # Función para eliminar el empleado seleccionado
    def eliminar_empleado():
        selected_item = tabla_empleados.selection()
        if selected_item:
            empleado_id = tabla_empleados.item(selected_item)['values'][0]  #  la primera columna es 'codigo'

            # Eliminar el empleado de la base de datos
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM empleado WHERE codigo = %s", (empleado_id,))
            conn.commit()
            cursor.close()
            conn.close()

            # Actualizar la tabla después de la eliminación
            tabla_empleados.delete(selected_item)  # Elimina el registro visualmente

    # Botón para eliminar empleado
    eliminar_btn = Button(w_empleados, text="Eliminar Empleado", command=eliminar_empleado, bg="#F9E400")
    eliminar_btn.pack(pady=5)

    Button(w_empleados, text="Cerrar", command=w_empleados.destroy, background="#FF004D").pack(pady=5)
def añadir_empleado(tabla_empleados):
    # Crear nueva ventana para agregar empleado
    w_agregar = Toplevel()
    w_agregar.title("Añadir Empleado")
    w_agregar.geometry("300x500")
    #w_agregar.configure(bg="#133E87")
    icono = PhotoImage(file="server-storage.png")
    w_agregar.iconphoto(True, icono)

    # Campos para ingresar datos
    ttk.Label(w_agregar, text="Codigo").pack()
    entry_codigo = ttk.Entry(w_agregar)
    entry_codigo.pack()

    ttk.Label(w_agregar, text="Nombre").pack()
    entry_nombre = ttk.Entry(w_agregar)
    entry_nombre.pack()

    ttk.Label(w_agregar, text="Direccion").pack()
    entry_direccion = ttk.Entry(w_agregar)
    entry_direccion.pack()

    ttk.Label(w_agregar, text="Telefono").pack()
    entry_telefono = ttk.Entry(w_agregar)
    entry_telefono.pack()

    ttk.Label(w_agregar, text="Fecha Nacimiento").pack()
    entry_fechanac = ttk.Entry(w_agregar)
    entry_fechanac.pack()

    ttk.Label(w_agregar, text="Sexo").pack()
    entry_sexo = ttk.Entry(w_agregar)
    entry_sexo.pack()

    ttk.Label(w_agregar, text="Sueldo").pack()
    entry_sueldo = ttk.Entry(w_agregar)
    entry_sueldo.pack()

    ttk.Label(w_agregar, text="Turno").pack()
    entry_turno = ttk.Entry(w_agregar)
    entry_turno.pack()

    ttk.Label(w_agregar, text="Contraseña").pack()
    entry_contra = ttk.Entry(w_agregar)
    entry_contra.pack()

    def guardar_empleado():
        codigo = entry_codigo.get()
        nombre = entry_nombre.get()
        direccion = entry_direccion.get()
        telefono = entry_telefono.get()
        fecha_nac = entry_fechanac.get()
        sexo = entry_sexo.get()
        sueldo = entry_sueldo.get()
        turno = entry_turno.get()
        contraseña = entry_contra.get()

        # Insertar el nuevo empleado en la base de datos
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO empleado (codigo, nombre, direccion, telefono, fecha_nac, sexo, sueldo, turno, contraseña) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (codigo, nombre, direccion, telefono, fecha_nac, sexo, sueldo, turno, contraseña))
        conn.commit()

        # Obtener el último registro añadido para mostrarlo en el Treeview
        cursor.execute("SELECT * FROM empleado WHERE codigo = %s", (codigo,))
        nuevo_empleado = cursor.fetchone()

        # Insertar el nuevo registro en el Treeview
        if nuevo_empleado:
            tabla_empleados.insert("", "end", values=nuevo_empleado)

        cursor.close()
        conn.close()

        w_agregar.destroy()  # Cerrar la ventana de añadir empleado

    # Botón para guardar empleado
    btn_guardar = Button(w_agregar, text="Guardar", command=guardar_empleado, bg="#008DDA")
    btn_guardar.pack(pady=20)

    Button(w_agregar, text="Cerrar", command=w_agregar.destroy, background="#FF004D").pack(pady=5)

#------------------------------------------DOCTORES--------------------------------------------------------
def mostrar_doctores():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM doctor")
    doctores = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()

    # Crear una nueva ventana para mostrar los doctores
    w_doctores = Toplevel()
    w_doctores.title("Doctores")
    w_doctores.configure(bg="#133E87")
    Label(w_doctores, text="Tabla de Doctores", bg="#133E87", fg="White").pack(pady=10)
    icono = PhotoImage(file="server-storage.png")
    w_doctores.iconphoto(True, icono)

    # Crear un Treeview para mostrar los datos
    tabla_doctores = ttk.Treeview(w_doctores, columns=column_names, show="headings")
    tabla_doctores.pack(expand=True, fill='both')

    # Configurar las columnas dinámicamente
    for col in column_names:
        tabla_doctores.heading(col, text=col)
        tabla_doctores.column(col, anchor='center', width=100)

    # Insertar los datos en el Treeview
    for doctor in doctores:
        tabla_doctores.insert("", "end", values=doctor)

    # Botón para añadir doctor
    añadir_btn = Button(w_doctores, text="Añadir Doctor", command=lambda: añadir_doctor(tabla_doctores), bg="#00FF9C")
    añadir_btn.pack(pady=5)

    # Función para eliminar el doctor seleccionado
    def eliminar_doctor():
        selected_item = tabla_doctores.selection()
        if selected_item:
            empleado_id = tabla_doctores.item(selected_item)['values'][0]

            # Eliminar el doctor de la base de datos
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM doctor WHERE codigo = %s", (empleado_id,))
            conn.commit()
            cursor.close()
            conn.close()

            # Actualizar la tabla después de la eliminación
            tabla_doctores.delete(selected_item)  # Elimina el registro visualmente

    # Botón para eliminar doctor
    eliminar_btn = Button(w_doctores, text="Eliminar Doctor", command=eliminar_doctor, bg="#F9E400")
    eliminar_btn.pack(pady=5)

    Button(w_doctores, text="Cerrar", command=w_doctores.destroy, bg="#FF004D").pack(pady=5)

def añadir_doctor(tabla_doctores):
    # Crear nueva ventana para agregar doctor
    w_agregar = Toplevel()
    w_agregar.title("Añadir Doctor")
    w_agregar.geometry("300x400")
    icono = PhotoImage(file="server-storage.png")
    w_agregar.iconphoto(True, icono)

    # Campos para ingresar datos
    ttk.Label(w_agregar, text="Codigo").pack()
    entry_codigo = ttk.Entry(w_agregar)
    entry_codigo.pack()

    ttk.Label(w_agregar, text="Nombre").pack()
    entry_nombre = ttk.Entry(w_agregar)
    entry_nombre.pack()

    ttk.Label(w_agregar, text="Direccion").pack()
    entry_direccion = ttk.Entry(w_agregar)
    entry_direccion.pack()

    ttk.Label(w_agregar, text="Telefono").pack()
    entry_telefono = ttk.Entry(w_agregar)
    entry_telefono.pack()

    ttk.Label(w_agregar, text="Fecha Nacimiento").pack()
    entry_fechanac = ttk.Entry(w_agregar)
    entry_fechanac.pack()

    ttk.Label(w_agregar, text="Sexo").pack()
    entry_sexo = ttk.Entry(w_agregar)
    entry_sexo.pack()

    ttk.Label(w_agregar, text="Especialidad").pack()
    entry_especialidad = ttk.Entry(w_agregar)
    entry_especialidad.pack()

    ttk.Label(w_agregar, text="Contraseña").pack()
    entry_contra = ttk.Entry(w_agregar)
    entry_contra.pack()

    def guardar_doctor():
        codigo = entry_codigo.get()
        nombre = entry_nombre.get()
        direccion = entry_direccion.get()
        telefono = entry_telefono.get()
        fecha_nac = entry_fechanac.get()
        sexo = entry_sexo.get()
        especialidad = entry_especialidad.get()
        contraseña = entry_contra.get()

        # Insertar el nuevo doctor en la base de datos
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO doctor (codigo, nombre, direccion, telefono, fecha_nac, sexo, especialidad, contraseña) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (codigo, nombre, direccion, telefono, fecha_nac, sexo, especialidad, contraseña))
        conn.commit()

        # Obtener el último registro añadido para mostrarlo en el Treeview
        cursor.execute("SELECT * FROM doctor WHERE codigo = %s", (codigo,))
        nuevo_empleado = cursor.fetchone()

        # Insertar el nuevo registro en el Treeview
        if nuevo_empleado:
            tabla_doctores.insert("", "end", values=nuevo_empleado)

        cursor.close()
        conn.close()

        w_agregar.destroy()  # Cerrar la ventana de añadir doctor

    # Botón para guardar doctor
    btn_guardar = Button(w_agregar, text="Guardar", command=guardar_doctor, bg="#008DDA")
    btn_guardar.pack(pady=10)

    Button(w_agregar, text="Cerrar", command=w_agregar.destroy, background="#FF004D").pack(pady=5)


#-----------------------------------PACIENTES---------------------------------------------------------

def mostrar_pacientes():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM paciente")
    pacientes = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()

    # Crear una nueva ventana para mostrar los pacientes
    w_pacientes = Toplevel()
    w_pacientes.title("Pacientes")
    w_pacientes.configure(bg="#433878")
    Label(w_pacientes, text="Tabla de Pacientes", bg="#433878", fg="White").pack(pady=10)
    icono = PhotoImage(file="server-storage.png")
    w_pacientes.iconphoto(True, icono)

    # Crear un Treeview para mostrar los datos
    tabla_pacientes = ttk.Treeview(w_pacientes, columns=column_names, show="headings")
    tabla_pacientes.pack(expand=True, fill='both')

    # Configurar las columnas dinámicamente
    for col in column_names:
        tabla_pacientes.heading(col, text=col)
        tabla_pacientes.column(col, anchor='center', width=100)

    # Insertar los datos en el Treeview
    for paciente in pacientes:
        tabla_pacientes.insert("", "end", values=paciente)

    # Botón para añadir paciente
    añadir_btn = Button(w_pacientes, text="Añadir Paciente", command=lambda: añadir_citas(tabla_pacientes), bg="#00FF9C")
    añadir_btn.pack(pady=5)

    # Función para eliminar el paciente seleccionado
    def eliminar_paciente():
        selected_item1 = tabla_pacientes.selection()
        if selected_item1:
            empleado_id1 = tabla_pacientes.item(selected_item1)['values'][0]

            # Eliminar el paciente de la base de datos
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM paciente WHERE codigo = %s", (empleado_id1,))
            conn.commit()
            cursor.close()
            conn.close()

            # Actualizar la tabla después de la eliminación
            tabla_pacientes.delete(selected_item1)  # Elimina el registro visualmente

    # Botón para eliminar paciente
    eliminar_btn = Button(w_pacientes, text="Eliminar Paciente", command=eliminar_paciente, bg="#F9E400")
    eliminar_btn.pack(pady=5)

    Button(w_pacientes, text="Cerrar", command=w_pacientes.destroy, bg="#FF004D").pack(pady=5)

def añadir_paciente(tabla_pacientes):
    # Crear nueva ventana para agregar doctor
    w_agregar = Toplevel()
    w_agregar.title("Añadir Paciente")
    w_agregar.geometry("300x400")
    icono = PhotoImage(file="server-storage.png")
    w_agregar.iconphoto(True, icono)

    # Campos para ingresar datos
    ttk.Label(w_agregar, text="Codigo").pack()
    entry_codigo = ttk.Entry(w_agregar)
    entry_codigo.pack()

    ttk.Label(w_agregar, text="Nombre").pack()
    entry_nombre = ttk.Entry(w_agregar)
    entry_nombre.pack()

    ttk.Label(w_agregar, text="Direccion").pack()
    entry_direccion = ttk.Entry(w_agregar)
    entry_direccion.pack()

    ttk.Label(w_agregar, text="Telefono").pack()
    entry_telefono = ttk.Entry(w_agregar)
    entry_telefono.pack()

    ttk.Label(w_agregar, text="Fecha Nacimiento").pack()
    entry_fechanac = ttk.Entry(w_agregar)
    entry_fechanac.pack()

    ttk.Label(w_agregar, text="Sexo").pack()
    entry_sexo = ttk.Entry(w_agregar)
    entry_sexo.pack()

    ttk.Label(w_agregar, text="Edad").pack()
    entry_edad = ttk.Entry(w_agregar)
    entry_edad.pack()

    ttk.Label(w_agregar, text="Estatura").pack()
    entry_estatura = ttk.Entry(w_agregar)
    entry_estatura.pack()

    def guardar_paciente():
        codigo = entry_codigo.get()
        nombre = entry_nombre.get()
        direccion = entry_direccion.get()
        telefono = entry_telefono.get()
        fecha_nac = entry_fechanac.get()
        sexo = entry_sexo.get()
        edad = entry_edad.get()
        estatura = entry_estatura.get()

        # Insertar el nuevo paciente en la base de datos
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO paciente (codigo, nombre, direccion, telefono, fecha_nac, sexo, edad, estatura) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (codigo, nombre, direccion, telefono, fecha_nac, sexo, edad, estatura))
        conn.commit()

        # Obtener el último registro añadido para mostrarlo en el Treeview
        cursor.execute("SELECT * FROM paciente WHERE codigo = %s", (codigo,))
        nuevo_empleado = cursor.fetchone()

        # Insertar el nuevo registro en el Treeview
        if nuevo_empleado:
            tabla_pacientes.insert("", "end", values=nuevo_empleado)

        cursor.close()
        conn.close()

        w_agregar.destroy()  # Cerrar la ventana de añadir paciente

    # Botón para guardar doctor
    btn_guardar = Button(w_agregar, text="Guardar", command=guardar_paciente, bg="#008DDA")
    btn_guardar.pack(pady=10)

    Button(w_agregar, text="Cerrar", command=w_agregar.destroy, background="#FF004D").pack(pady=5)

#-------------------------------------CITAS--------------------------------------------------

def mostrar_citas():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cita")
    citas = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()

    # Crear una nueva ventana para mostrar las citas y el calendario
    w_citas = Toplevel()
    w_citas.title("Citas")
    w_citas.configure(bg="#433878")
    Label(w_citas, text="Tabla de Citas", bg="#433878", fg="White").pack(pady=10)
    icono = PhotoImage(file="server-storage.png")
    w_citas.iconphoto(True, icono)

    # Crear un Treeview para mostrar los datos
    tabla_citas = ttk.Treeview(w_citas, columns=column_names, show="headings")
    tabla_citas.pack(expand=True, fill='both')

    # Configurar las columnas dinámicamente
    for col in column_names:
        tabla_citas.heading(col, text=col)
        tabla_citas.column(col, anchor='center', width=100)

    # Insertar los datos en el Treeview
    for cita in citas:
        tabla_citas.insert("", "end", values=cita)

    # Crear un widget de calendario
    calendar_frame = Frame(w_citas)
    calendar_frame.pack(pady=20)

     #AQUI SE PERSONALIZA EL CALENDARIO
    cal = Calendar(calendar_frame,
                   selectmode="day",
                   year=2024, month=11,
                   showweeknumbers=False,  # Oculta los números de semana
                   locale="es",  # Cambia el idioma a español
                   date_pattern="dd/mm/yyyy",  # Formato de fecha en español
                   background="#B1D690",
                   foreground="black",
                   selectbackground="blue",
                   selectforeground="white",
                   weekendbackground="lightgrey",
                   weekendforeground="white",
                   othermonthforeground="grey",
                   othermonthbackground="white",
                   bordercolor="grey",
                   normalbackground="white",
                   normalforeground="black",
                   font=("Arial", 12),
                   headerfont=("Arial", 14, "bold"),
                   headersbackground="#88C273",
                   headersforeground="black")
    cal.pack()

    # Definir el color de los eventos de citas
    cal.tag_config("cita", background="#008DDA", foreground="black")

    def modificar_datos():
        selected_item = tabla_citas.selection()
        if selected_item:
            # Obtener los datos de la fila seleccionada
            datos = tabla_citas.item(selected_item)['values']
            id_empleado = datos[0]  # Suponiendo que el ID está en la primera columna

            # Crear una ventana para modificar los datos
            modificar_citas(id_empleado, datos, tabla_citas)

    # Crear un botón "Modificar"
    btn_modificar = Button(w_citas, text="Modificar Cita", command=modificar_datos, bg="#008DDA")
    btn_modificar.pack(pady=5)


    # Resaltar las fechas de citas en el calendario
    for cita in citas:
        fecha = cita[3]  # Suponiendo que la fecha está en la cuarta columna
        cal.calevent_create(fecha, "Cita", "cita")

    # Agregar botón para añadir una nueva cita
    añadir_btn = Button(w_citas, text="Añadir Cita", command=lambda: añadir_citas(tabla_citas), bg="#00FF9C")
    añadir_btn.pack(pady=5)
    limpiar_campos()

    # Función para eliminar la cita seleccionada
    def eliminar_citas():
        selected_item = tabla_citas.selection()
        if selected_item:
            cita_id = tabla_citas.item(selected_item)['values'][0]

            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM cita WHERE id_cita = %s", (cita_id,))
            conn.commit()
            cursor.close()
            conn.close()

            # Actualizar la tabla y el calendario
            tabla_citas.delete(selected_item)

    eliminar_btn = Button(w_citas, text="Eliminar Cita", command=eliminar_citas, bg="#F9E400")
    eliminar_btn.pack(pady=5)

    Button(w_citas, text="Cerrar", command=w_citas.destroy, bg="#FF004D").pack(pady=5)

    def modificar_citas(id_cita, datos_actuales, tabla_citas):
        # Ventana para modificar los datos
        w_modificar = Toplevel()
        w_modificar.geometry("300x400")
        w_modificar.title("Modificar Cita")

        # Conectar a la base de datos para obtener los doctores y pacientes disponibles
        conn = conectar_db()
        cursor = conn.cursor()

        # Obtener lista de pacientes con su código y nombre
        cursor.execute("SELECT codigo, nombre FROM paciente")
        pacientes = cursor.fetchall()  # Lista de tuplas (codigo, nombre)

        # Obtener lista de doctores con su código y nombre
        cursor.execute("SELECT codigo, nombre FROM doctor")
        doctores = cursor.fetchall()  # Lista de tuplas (codigo, nombre)

        cursor.close()
        conn.close()

        # Campos de entrada para modificar
        # Combobox para seleccionar el doctor, muestra el nombre pero guarda el código
        ttk.Label(w_modificar, text="Doctor").pack()
        combo_codigo_doctor = ttk.Combobox(w_modificar, values=[f"{codigo} - {nombre}" for codigo, nombre in doctores])
        combo_codigo_doctor.pack()
        # Configurar el valor inicial usando el código actual del doctor
        combo_codigo_doctor.set(f"{datos_actuales[1]}")

        # Combobox para seleccionar el paciente, muestra el nombre pero guarda el código
        ttk.Label(w_modificar, text="Paciente").pack()
        combo_codigo_paciente = ttk.Combobox(w_modificar,
                                             values=[f"{codigo} - {nombre}" for codigo, nombre in pacientes])
        combo_codigo_paciente.pack()
        # Configurar el valor inicial usando el código actual del paciente
        combo_codigo_paciente.set(f"{datos_actuales[2]}")

        # Campo de entrada para la fecha
        ttk.Label(w_modificar, text="Fecha ").pack()
        entry_fechan = ttk.Entry(w_modificar)
        entry_fechan.pack()
        entry_fechan.insert(0, datos_actuales[3])

        # Campo de entrada para la hora
        ttk.Label(w_modificar, text="Hora").pack()
        entry_horan = ttk.Entry(w_modificar)
        entry_horan.pack()
        entry_horan.insert(0, datos_actuales[4])

        # Función para guardar los cambios en la base de datos
        def guardar_cambios():
            # Obtener valores de los Combobox
            nuevo_doc = combo_codigo_doctor.get().split(" - ")[0]  # Extraer solo el código del doctor
            nuevo_pac = combo_codigo_paciente.get().split(" - ")[0]  # Extraer solo el código del paciente
            nuevo_fecha = entry_fechan.get()
            nuevo_hora = entry_horan.get()

            # Verificar si todos los campos tienen valores
            if not nuevo_doc or not nuevo_pac or not nuevo_fecha or not nuevo_hora:
                messagebox.showerror("Error", "Todos los campos deben ser llenados")
                return

            try:
                conn = conectar_db()
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE cita
                    SET codigo_doctor = %s, codigo_paciente = %s, fecha = %s, hora = %s
                    WHERE id_cita = %s
                """, (nuevo_doc, nuevo_pac, nuevo_fecha, nuevo_hora, id_cita))  # Pasar valores a la consulta
                conn.commit()

                # Actualizar la tabla en la interfaz
                for item in tabla_citas.get_children():
                    if tabla_citas.item(item)["values"][0] == id_cita:  # Buscar la fila correspondiente
                        tabla_citas.item(item, values=(
                        id_cita, nuevo_doc, nuevo_pac, nuevo_fecha, nuevo_hora))  # Actualizar la fila

                cursor.close()
                conn.close()

                messagebox.showinfo("Éxito", "Datos actualizados correctamente.")
                w_modificar.destroy()  # Cerrar la ventana de modificación

            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar los cambios: {e}")

        # Botón para guardar los cambios
        btn_guardar = Button(w_modificar, text="Guardar", command=guardar_cambios, bg="#008DDA")
        btn_guardar.pack(pady=10)

        # Botón para cerrar la ventana de modificación
        Button(w_modificar, text="Cerrar", command=w_modificar.destroy, bg="#FF004D").pack(pady=5)

def añadir_citas(tabla_citas):
    # Crear nueva ventana para agregar cita
    w_agregar = Toplevel()
    w_agregar.title("Añadir Cita")
    w_agregar.geometry("300x400")
    icono = PhotoImage(file="server-storage.png")
    w_agregar.iconphoto(True, icono)

    # Conectar a la base de datos para obtener los doctores y pacientes disponibles
    conn = conectar_db()
    cursor = conn.cursor()

    # Obtener lista de pacientes con su código y nombre
    cursor.execute("SELECT codigo, nombre FROM paciente")
    pacientes = cursor.fetchall()  # Esto será una lista de tuplas (codigo, nombre)

    # Obtener lista de doctores con su código y nombre
    cursor.execute("SELECT codigo, nombre FROM doctor")
    doctores = cursor.fetchall()  # Esto será una lista de tuplas (codigo, nombre)

    cursor.close()
    conn.close()

    # Campos para ingresar datos
    ttk.Label(w_agregar, text="ID de Cita").pack()
    entry_id_cita = ttk.Entry(w_agregar)
    entry_id_cita.pack()

    # Combobox para seleccionar el paciente, muestra el nombre pero guarda el código
    ttk.Label(w_agregar, text="Paciente").pack()
    combo_codigo_paciente = ttk.Combobox(w_agregar, values=[f"{codigo} - {nombre}" for codigo, nombre in pacientes])
    combo_codigo_paciente.pack()

    # Combobox para seleccionar el doctor, muestra el nombre pero guarda el código
    ttk.Label(w_agregar, text="Doctor").pack()
    combo_codigo_doctor = ttk.Combobox(w_agregar, values=[f"{codigo} - {nombre}" for codigo, nombre in doctores])
    combo_codigo_doctor.pack()

    # Campo de entrada de texto para la fecha
    ttk.Label(w_agregar, text="Fecha").pack()
    entry_fecha = ttk.Entry(w_agregar)
    entry_fecha.pack()

    # Campo de entrada de texto para la hora
    ttk.Label(w_agregar, text="Hora").pack()
    entry_hora = ttk.Entry(w_agregar)
    entry_hora.pack()

    def guardar_cita(tabla_citas):
        codigo_cita = entry_id_cita.get()

        # Obtener el código de paciente y doctor de la selección del Combobox
        codigo_paciente = combo_codigo_paciente.get().split(" - ")[0]  # Obtener el código antes del "-"
        codigo_doctor = combo_codigo_doctor.get().split(" - ")[0]  # Obtener el código antes del "-"

        fecha = entry_fecha.get()
        hora = entry_hora.get()

        # Verificar si todos los campos tienen valores
        if not (codigo_cita and codigo_paciente and codigo_doctor and fecha and hora):
            messagebox.showerror("Error", "Todos los campos deben ser llenados")
            return

        conn = conectar_db()
        cursor = conn.cursor()

        # Consulta para verificar si el doctor ya tiene una cita a la misma hora y fecha
        cursor.execute(
            "SELECT * FROM cita WHERE codigo_doctor = %s AND fecha = %s AND hora = %s",
            (codigo_doctor, fecha, hora)
        )
        cita_existente = cursor.fetchone()

        if cita_existente:
            messagebox.showerror("Error", "El doctor ya tiene una cita en esa fecha y hora.")
            cursor.close()
            conn.close()
            return  # Salir de la función si hay conflicto

        # Insertar la nueva cita en la base de datos
        cursor.execute(
            "INSERT INTO cita (id_cita, codigo_paciente, codigo_doctor, fecha, hora) VALUES (%s, %s, %s, %s, %s)",
            (codigo_cita, codigo_paciente, codigo_doctor, fecha, hora)
        )
        conn.commit()

        # Obtener el último registro añadido para mostrarlo en el Treeview
        cursor.execute("SELECT * FROM cita WHERE id_cita = %s", (codigo_cita,))
        nueva_cita = cursor.fetchone()

        # Insertar el nuevo registro en el Treeview
        if nueva_cita:
            tabla_citas.insert("", "end", values=nueva_cita)

        cursor.close()
        conn.close()
        w_agregar.destroy()  # Cerrar la ventana de añadir cita

    # Botón para guardar cita
    btn_guardar = Button(w_agregar, text="Guardar", command=lambda: guardar_cita(tabla_citas), bg="#008DDA")
    btn_guardar.pack(pady=10)

    Button(w_agregar, text="Cerrar", command=w_agregar.destroy, background="#FF004D").pack(pady=5)

#----------------------------------------MEDICAMENTOS-------------------------------------------------------------

def mostrar_medicamentos():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medicamento")
    medicamentos = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()

    # Crear una nueva ventana para mostrar los pacientes
    w_medicamentos = Toplevel()
    w_medicamentos.title("Medicamentos")
    w_medicamentos.configure(bg="#257180")
    Label(w_medicamentos, text="Tabla de Medicamentos", bg="#433878", fg="White").pack(pady=10)
    icono = PhotoImage(file="server-storage.png")
    w_medicamentos.iconphoto(True, icono)

    # Crear un Treeview para mostrar los datos
    tabla_medicamentos = ttk.Treeview(w_medicamentos, columns=column_names, show="headings")
    tabla_medicamentos.pack(expand=True, fill='both')

    # Configurar las columnas dinámicamente
    for col in column_names:
        tabla_medicamentos.heading(col, text=col)
        tabla_medicamentos.column(col, anchor='center', width=100)

    # Insertar los datos en el Treeview
    for medicamento in medicamentos:
        tabla_medicamentos.insert("", "end", values=medicamento)

    # Botón para añadir paciente
    añadir_btn = Button(w_medicamentos, text="Añadir Medicamento", command=lambda: añadir_medicamento(tabla_medicamentos), bg="#00FF9C")
    añadir_btn.pack(pady=5)

    # Función para eliminar el paciente seleccionado
    def eliminar_medicamento():
        selected_item1 = tabla_medicamentos.selection()
        if selected_item1:
            empleado_id1 = tabla_medicamentos.item(selected_item1)['values'][0]

            # Eliminar el paciente de la base de datos
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM medicamento WHERE codigo = %s", (empleado_id1,))
            conn.commit()
            cursor.close()
            conn.close()

            # Actualizar la tabla después de la eliminación
            tabla_medicamentos.delete(selected_item1)  # Elimina el registro visualmente

    # Botón para eliminar paciente
    eliminar_btn = Button(w_medicamentos, text="Eliminar Medicamento", command=eliminar_medicamento, bg="#F9E400")
    eliminar_btn.pack(pady=5)

    Button(w_medicamentos, text="Cerrar", command=w_medicamentos.destroy, bg="#FF004D").pack(pady=5)

def añadir_medicamento(tabla_medicamentos):
    # Crear nueva ventana para agregar medicamento
    w_agregar = Toplevel()
    w_agregar.title("Añadir Medicamento")
    w_agregar.geometry("300x400")
    icono = PhotoImage(file="server-storage.png")
    w_agregar.iconphoto(True, icono)

    # Campos para ingresar datos
    ttk.Label(w_agregar, text="Codigo").pack()
    entry_codigo = ttk.Entry(w_agregar)
    entry_codigo.pack()

    ttk.Label(w_agregar, text="Nombre del Medicamento").pack()
    entry_nombre_med = ttk.Entry(w_agregar)
    entry_nombre_med.pack()

    ttk.Label(w_agregar, text="Via de Administracion").pack()
    entry_via = ttk.Entry(w_agregar)
    entry_via.pack()

    ttk.Label(w_agregar, text="Presentacion").pack()
    entry_pres = ttk.Entry(w_agregar)
    entry_pres.pack()

    ttk.Label(w_agregar, text="Fecha de Caducidad").pack()
    entry_fechacad = ttk.Entry(w_agregar)
    entry_fechacad.pack()


    def guardar_medicamento():
        codigo = entry_codigo.get()
        nombre = entry_nombre_med.get()
        via_admin = entry_via.get()
        presentacion = entry_pres.get()
        fecha_cad = entry_fechacad.get()

        # Insertar el nuevo medicamento en la base de datos
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO medicamento (codigo, nombre, via_adm, presentacion, fecha_cad) VALUES (%s, %s, %s, %s, %s)",
            (codigo, nombre, via_admin, presentacion, fecha_cad))
        conn.commit()

        # Obtener el último registro añadido para mostrarlo en el Treeview
        cursor.execute("SELECT * FROM medicamento WHERE codigo = %s", (codigo,))
        nuevo_medicamento = cursor.fetchone()

        # Insertar el nuevo registro en el Treeview
        if nuevo_medicamento:
            tabla_medicamentos.insert("", "end", values=nuevo_medicamento)

        cursor.close()
        conn.close()

        w_agregar.destroy()  # Cerrar la ventana de añadir medicamento

    # Botón para guardar medicamento
    btn_guardar = Button(w_agregar, text="Guardar", command=guardar_medicamento, bg="#008DDA")
    btn_guardar.pack(pady=10)

    Button(w_agregar, text="Cerrar", command=w_agregar.destroy, background="#FF004D").pack(pady=5)

def ventana_principal():
    w.withdraw()
    w2 = Toplevel()  # Toplevel para crear una nueva ventana
    w2.geometry("500x400")
    w2.title("Sistema Base de Datos")
    icono = PhotoImage(file="server-storage.png")
    w2.iconphoto(True, icono)
    w2.configure(background="#133E87")

    # Frame superior para los botones
    frame_botones = Frame(w2)
    frame_botones.pack(side="top", fill="x")  # Llenar horizontalmente

    # Crear botones
    btn_empleados = Button(frame_botones, text="Empleados", command=mostrar_empleados,background="#0E2954", fg="White")
    btn_empleados.pack(side="left", expand=True, fill="x")

    btn_doctores = Button(frame_botones, text="Doctores", command=mostrar_doctores, background="#1F6E8C", fg="White")
    btn_doctores.pack(side="left", expand=True, fill="x")

    btn_pacientes = Button(frame_botones, text="Pacientes", command=mostrar_pacientes, background="#2E8A99", fg="White")
    btn_pacientes.pack(side="left", expand=True, fill="x")

    btn_citas = Button(frame_botones, text="Citas", command=mostrar_citas, background="#84A7A1", fg="White")
    btn_citas.pack(side="left", expand=True, fill="x")

    btn_medicamentos = Button(frame_botones, text="Medicamentos", command=mostrar_medicamentos, background="#15B392", fg="White")
    btn_medicamentos.pack(side="left", expand=True, fill="x")

    # Poner la imagen usando pillow
    image = Image.open("database.png")  # Aquí va la ruta de tu imagen
    image = image.resize((200, 200), Image.LANCZOS)  # Cambiar el tamaño de la imagen
    image_tk = ImageTk.PhotoImage(image)

    # Crear etiqueta para la imagen y centrarla
    label_imagen = Label(w2, image=image_tk, background="#133E87")
    label_imagen.pack(pady=20)  # Espacio superior para la imagen

    label_imagen.image = image_tk  # Para no borrar la imagen de la memoria

    # Botón de cerrar fuera del frame de botones
    btn_cerrar = Button(w2, text="Cerrar", command=lambda: cerrar_ventanas(w2), background="#FF004D")
    btn_cerrar.pack(pady=10)  # Espacio superior para el botón

def mostrar_citas_doctor(codigo_doctor):
    # Conectar a la base de datos
    conn = conectar_db()
    cursor = conn.cursor()

    # Filtrar las citas asignadas al doctor según su código
    query = """
            SELECT id_cita, codigo_paciente, fecha, hora
            FROM cita
            WHERE codigo_doctor = %s
            ORDER BY fecha, hora
        """
    cursor.execute(query, (codigo_doctor,))
    citas = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()

    # Crear una nueva ventana para mostrar las citas y el calendario
    w_citas = Toplevel()
    w_citas.title("Citas")
    w_citas.configure(bg="#433878")
    Label(w_citas, text="Tabla de Citas", bg="#433878", fg="White").pack(pady=10)
    icono = PhotoImage(file="server-storage.png")
    w_citas.iconphoto(True, icono)

    # Crear un Treeview para mostrar los datos
    tabla_citas = ttk.Treeview(w_citas, columns=column_names, show="headings")
    tabla_citas.pack(expand=True, fill='both')

    # Configurar las columnas dinámicamente
    for col in column_names:
        tabla_citas.heading(col, text=col)
        tabla_citas.column(col, anchor='center', width=100)

    # Insertar los datos filtrados en el Treeview
    for cita in citas:
        tabla_citas.insert("", "end", values=cita)

    # Crear un widget de calendario
    calendar_frame = Frame(w_citas)
    calendar_frame.pack(pady=20)

    # Personalizar el calendario
    cal = Calendar(calendar_frame,
                   selectmode="day",
                   year=2024, month=11,
                   showweeknumbers=False,  # Oculta los números de semana
                   locale="es",  # Cambia el idioma a español
                   date_pattern="dd/mm/yyyy",  # Formato de fecha en español
                   background="#B1D690",
                   foreground="black",
                   selectbackground="blue",
                   selectforeground="white",
                   weekendbackground="lightgrey",
                   weekendforeground="white",
                   othermonthforeground="grey",
                   othermonthbackground="white",
                   bordercolor="grey",
                   normalbackground="white",
                   normalforeground="black",
                   font=("Arial", 12),
                   headerfont=("Arial", 14, "bold"),
                   headersbackground="#88C273",
                   headersforeground="black")
    cal.pack()

    # Configurar un color para eventos de citas
    cal.tag_config("cita", background="#008DDA", foreground="black")

def cerrar_ventanas(window):
    window.destroy()  # Cierra la ventana secundaria
    limpiar_campos()
    w.deiconify()  # Muestra la ventana principal de nuevo

def login():
    user = usuario.get()  # Obtiene el nombre de usuario ingresado
    password = contra.get()  # Obtiene la contraseña ingresada

    # Verificar si es administrador
    if user == 'admin' and password == '1234':
        ventana_principal()  # Abre la ventana principal para el administrador
        return

    # Conectar a la base de datos y verificar las credenciales
    conexion = conectar_db()
    if conexion is None:
        return

    try:
        cursor = conexion.cursor()

        # Verificar si las credenciales pertenecen a un doctor
        query_doctor = "SELECT codigo, nombre FROM doctor WHERE codigo = %s AND contraseña = %s"
        cursor.execute(query_doctor, (user, password))
        resultado_doctor = cursor.fetchone()

        if resultado_doctor:
            codigo_doctor, nombre_doctor = resultado_doctor  # Recupera el código y nombre del doctor
            mensaje_bienvenida = f"Hola, Dr. {nombre_doctor.capitalize()}"
            messagebox.showinfo("Inicio de sesión exitoso", mensaje_bienvenida)
            ventana_doctores(nombre_doctor, codigo_doctor)  # Abre la ventana de doctores
            return

        # Verificar si las credenciales pertenecen a un empleado
        query_empleado = "SELECT codigo, nombre FROM empleado WHERE codigo = %s AND contraseña = %s"
        cursor.execute(query_empleado, (user, password))
        resultado_empleado = cursor.fetchone()

        if resultado_empleado:
            codigo_empleado, nombre_empleado = resultado_empleado  # Recupera el código y nombre del empleado
            mensaje_bienvenida = f"Hola, {nombre_empleado.capitalize()}"
            messagebox.showinfo("Inicio de sesión exitoso", mensaje_bienvenida)
            ventana_empleados(nombre_empleado)  # Abre la ventana de empleados
            return

        # Si no se encuentra ninguna coincidencia
        messagebox.showerror("Error", "Código o contraseña inválidos...")

    except Exception as e:
        messagebox.showerror("Error de consulta", f"Ocurrió un error al verificar las credenciales: {e}")

    finally:
        cursor.close()
        conexion.close()




#-----------------------------------VENTANA DE EMPLEADOS--------------------------------------------
def ventana_empleados(nombre_empleado):
    w.withdraw()
    w2 = Toplevel()  # Toplevel para crear una nueva ventana
    w2.geometry("500x400")
    w2.title("Empleados")
    icono = PhotoImage(file="server-storage.png")
    w2.iconphoto(True, icono)
    w2.configure(background="#433878")

    Label(w2, text=f"Hola {nombre_empleado}!", bg="#433878", font=("Arial", 12),fg="White", anchor='w').pack(fill='x')

    # Frame superior para los botones
    frame_botones = Frame(w2)
    frame_botones.pack(side="top", fill="x")  # Llenar horizontalmente

    # Crear botones
    btn_pacientes1 = Button(frame_botones, text="Dar de alta", command=mostrar_pacientes, background="#6196A6", fg="White")
    btn_pacientes1.pack(side="left", expand=True, fill="x")

    btn_pacientes1 = Button(frame_botones, text="Registrar Cita", command=mostrar_citas ,background="#133E87", fg="White")
    btn_pacientes1.pack(side="left", expand=True, fill="x")

    # Poner la imagen usando pillow
    image = Image.open("staff.png")  # Aquí va la ruta de tu imagen
    image = image.resize((200, 200), Image.LANCZOS)  # Cambiar el tamaño de la imagen
    image_tk = ImageTk.PhotoImage(image)

    # Crear etiqueta para la imagen y centrarla
    label_imagen = Label(w2, image=image_tk, background="#433878")
    label_imagen.pack(pady=20)  # Espacio superior para la imagen

    label_imagen.image = image_tk  # Para no borrar la imagen de la memoria

    # Botón de cerrar fuera del frame de botones
    btn_cerrar = Button(w2, text="Cerrar", command=lambda: cerrar_ventanas(w2), background="#FF004D")
    btn_cerrar.pack(pady=10)  # Espacio superior para el botón

#--------------------VENTANA DE DOCTORES---------------------------------

def ventana_doctores(nombre_doctor, codigo_doctor):
    w.withdraw()
    w2 = Toplevel()  # Toplevel para crear una nueva ventana
    w2.geometry("500x400")
    w2.title("Doctores")
    icono = PhotoImage(file="server-storage.png")
    w2.iconphoto(True, icono)
    w2.configure(background="#1D2D50")

    # Saludo al doctor
    Label(w2, text=f"Hola Dr. {nombre_doctor}!", bg="#1D2D50", font=("Arial", 12), fg="White", anchor='w').pack(fill='x')

    # Frame superior para los botones
    frame_botones = Frame(w2)
    frame_botones.pack(side="top", fill="x")  # Llenar horizontalmente

    # Crear botones
    btn_citas = Button(frame_botones, text="Citas", command=lambda: mostrar_citas_doctor(codigo_doctor),
                       background="#590995", fg="White")
    btn_citas.pack(side="left", expand=True, fill="x")

    btn_medicamentos = Button(frame_botones, text="Medicamentos", command=mostrar_medicamentos,
                              background="#117554", fg="White")
    btn_medicamentos.pack(side="left", expand=True, fill="x")

    # Poner la imagen usando Pillow
    image = Image.open("caduceus.png")  # Aquí va la ruta de tu imagen
    image = image.resize((200, 200), Image.LANCZOS)  # Cambiar el tamaño de la imagen
    image_tk = ImageTk.PhotoImage(image)

    # Crear etiqueta para la imagen y centrarla
    label_imagen = Label(w2, image=image_tk, background="#1D2D50")
    label_imagen.pack(pady=20)  # Espacio superior para la imagen

    label_imagen.image = image_tk  # Para no borrar la imagen de la memoria

    # Botón de cerrar fuera del frame de botones
    btn_cerrar = Button(w2, text="Cerrar", command=lambda: cerrar_ventanas(w2), background="#FF004D")
    btn_cerrar.pack(pady=10)  # Espacio superior para el botón



# ------------------------VENTANA DE LOGIN-----------------------------
w = Tk()
w.geometry("400x400")
w.title("Iniciar sesión")
w.configure(bg="#133E87")
icono = PhotoImage(file="server-storage.png")
w.iconphoto(True,icono)
# Poner la imagen usando pillow
image = Image.open("unlocked.png")  # Aquí va la ruta de tu imagen
image = image.resize((150, 150), Image.LANCZOS)  # Cambiar el tamaño de la imagen
image_tk = ImageTk.PhotoImage(image)

# Crear etiqueta para la imagen y centrarla
label_imagen = Label(w, image=image_tk, bg="#133E87")
label_imagen.pack(pady=20)  # Espacio superior para la imagen

label_imagen.image = image_tk  # Para no borrar la imagen de la memoria

# ----------------------------CAMPOS---------------------------------------------
t1 = Label(w, text="USUARIO", background="#133E87", fg="White")
t1.pack(pady=5)
usuario = ttk.Entry(w)
usuario.pack()

t2 = Label(w, text="CONTRASEÑA", background="#133E87", fg="White")
t2.pack(pady=5)
contra = ttk.Entry(w, show="*")
contra.pack()

# --------------------------------BOTONES------------------------------------
btn_aceptar = Button(w, text="Aceptar", command=login, bg="#00FF9C")
btn_aceptar.pack(pady=10)

btn_cancelar = Button(w, text="Cancelar", command=w.destroy, bg="#FF004D")
btn_cancelar.pack(pady=10)

w.mainloop()
