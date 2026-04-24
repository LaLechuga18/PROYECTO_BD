# Núcleo Diagnóstico — Sistema de Gestión Hospitalaria

Sistema de escritorio para la gestión de un centro de diagnóstico médico, desarrollado con Python y Tkinter. Permite administrar empleados, doctores, pacientes, citas y medicamentos a través de una interfaz gráfica conectada a una base de datos PostgreSQL.

## Estructura del Proyecto

```
PROYECTO_BD/
├── app.py                  # Punto de entrada
├── db.py                   # Configuración y conexión a PostgreSQL
├── utils.py                # Funciones reutilizables de UI
├── models/
│   ├── empleado.py         # CRUD de empleados
│   ├── doctor.py           # CRUD de doctores
│   ├── paciente.py         # CRUD de pacientes
│   ├── cita.py             # CRUD de citas + validación de conflictos
│   └── medicamento.py      # CRUD de medicamentos
└── views/
    ├── login.py            # Ventana de inicio de sesión
    ├── main_view.py        # Panel de administrador
    ├── empleados_view.py   # Gestión de empleados
    ├── doctores_view.py    # Gestión de doctores + panel personal
    ├── pacientes_view.py   # Gestión de pacientes
    ├── citas_view.py       # Gestión de citas + calendario
    └── medicamentos_view.py
```

## Tecnologías

- **Python 3** — lenguaje principal
- **Tkinter** — interfaz gráfica de escritorio
- **PostgreSQL** — base de datos relacional
- **psycopg2** — conector Python ↔ PostgreSQL
- **Pillow** — manejo de imágenes en la UI
- **tkcalendar** — widget de calendario para citas

## Instalación

**1. Clonar el repositorio**
```bash
git clone https://github.com/LaLechuga18/nucleo-diagnostico.git
cd nucleo-diagnostico
```

**2. Crear entorno virtual e instalar dependencias**
```bash
python3 -m venv venv
source venv/bin/activate
pip install psycopg2-binary Pillow tkcalendar
```

En Linux, tkinter se instala desde el sistema:
```bash
# Fedora
sudo dnf install python3-tkinter

# Ubuntu/Debian
sudo apt install python3-tk
```

**3. Configurar la base de datos**

Editar `db.py` con tus credenciales de PostgreSQL:
```python
DB_CONFIG = {
    "dbname": "Nucleo Diagnostico",
    "user": "postgres",
    "password": "tu_contraseña",
    "host": "localhost",
}
```

**4. Ejecutar**
```bash
python app.py
```

## Roles de Usuario

El sistema maneja tres tipos de acceso desde la pantalla de login:

| Rol | Acceso |
|-----|--------|
| **Administrador** | Gestión completa de todas las entidades |
| **Doctor** | Vista de sus citas asignadas y medicamentos |
| **Empleado** | Registro de pacientes y citas |

## Arquitectura

El proyecto sigue una separación por capas inspirada en MVC:

- **`models/`** — toda la lógica de acceso a datos (SQL). Las vistas nunca hacen queries directamente.
- **`views/`** — ventanas Tkinter. Solo se comunican con los modelos, no con la BD.
- **`utils.py`** — funciones compartidas entre vistas para evitar duplicación de código.

## Notas

Proyecto universitario desarrollado para la materia de Bases de Datos en CUCEI, Universidad de Guadalajara. Refactorizado desde una arquitectura monolítica a una estructura modular por capas.
