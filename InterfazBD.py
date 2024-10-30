from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # LIBRERIA PARA IMPORTAR IMAGENES (pip install pillow)
import psycopg2  # Para la conexión a PostgreSQL


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
            empleado_id = tabla_empleados.item(selected_item)['values'][0]  # Asumiendo que la primera columna es 'codigo'

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

    # Botón para añadir empleado
    añadir_btn = Button(w_doctores, text="Añadir Doctor", command=lambda: añadir_doctor(tabla_doctores), bg="#00FF9C")
    añadir_btn.pack(pady=5)

    # Función para eliminar el doctor seleccionado
    def eliminar_dcotor():
        selected_item = tabla_doctores.selection()
        if selected_item:
            empleado_id = tabla_doctores.item(selected_item)['values'][0]  # Asumiendo que la primera columna es 'codigo'

            # Eliminar el empleado de la base de datos
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM doctor WHERE codigo = %s", (empleado_id,))
            conn.commit()
            cursor.close()
            conn.close()

            # Actualizar la tabla después de la eliminación
            tabla_doctores.delete(selected_item)  # Elimina el registro visualmente

    # Botón para eliminar empleado
    eliminar_btn = Button(w_doctores, text="Eliminar Doctor", command=eliminar_dcotor, bg="#F9E400")
    eliminar_btn.pack(pady=5)

    Button(w_doctores, text="Cerrar", command=w_doctores.destroy, bg="#FF004D").pack(pady=5)

def añadir_doctor(tabla_doctores):
    # Crear nueva ventana para agregar doctor
    w_agregar = Toplevel()
    w_agregar.title("Añadir Doctor")
    w_agregar.geometry("300x400")
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

        # Insertar el nuevo empleado en la base de datos
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

        w_agregar.destroy()  # Cerrar la ventana de añadir empleado

    # Botón para guardar doctor
    btn_guardar = Button(w_agregar, text="Guardar", command=guardar_doctor, bg="#008DDA")
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

    btn_doctores = Button(frame_botones, text="Doctores", command=mostrar_doctores,background="#1F6E8C", fg="White")
    btn_doctores.pack(side="left", expand=True, fill="x")

    btn_pacientes = Button(frame_botones, text="Pacientes", background="#2E8A99", fg="White")
    btn_pacientes.pack(side="left", expand=True, fill="x")

    btn_citas = Button(frame_botones, text="Citas",background="#84A7A1", fg="White")
    btn_citas.pack(side="left", expand=True, fill="x")

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

def cerrar_ventanas(window):
    window.destroy()  # Cierra la ventana secundaria
    limpiar_campos()
    w.deiconify()  # Muestra la ventana principal de nuevo

def login():
    user = usuario.get()
    contraseña = contra.get()
    if user == 'admin' and contraseña == '1234': #VALIDACION DE CADENAS
        ventana_principal()
    else:
        messagebox.showerror("Error","Usuario o contraseña invalido...")


# ------------------------VENTANA PRINCIPAL-----------------------------
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

# ---------------CAMPOS----------------
t1 = Label(w, text="USUARIO", background="#133E87", fg="White")
t1.pack(pady=5)
usuario = ttk.Entry(w)
usuario.pack()

t2 = Label(w, text="CONTRASEÑA", background="#133E87", fg="White")
t2.pack(pady=5)
contra = ttk.Entry(w, show="*")
contra.pack()

# ----------------BOTONES-----------------
btn_aceptar = Button(w, text="Aceptar", command=login, bg="#00FF9C")
btn_aceptar.pack(pady=10)

btn_cancelar = Button(w, text="Cancelar", command=w.destroy, bg="#FF004D")
btn_cancelar.pack(pady=10)

w.mainloop()
