import sqlite3

# Nombre de la base de datos
DB_NAME = "hotel.db"

# Conexión y creación de tablas
def create_tables():
    # Conectar a la base de datos
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Crear tabla de habitaciones
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS habitaciones (
            id_habitacion INTEGER PRIMARY KEY AUTOINCREMENT,
            numero INTEGER NOT NULL UNIQUE,
            tipo TEXT NOT NULL,
            estado TEXT DEFAULT 'disponible',
            precio_por_noche REAL NOT NULL
        );
    ''')

    # Crear tabla de clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            direccion TEXT,
            telefono TEXT,
            email TEXT UNIQUE
        );
    ''')

    # Crear tabla de reservas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservas (
            id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER NOT NULL,
            id_habitacion INTEGER NOT NULL,
            fecha_entrada DATE NOT NULL,
            fecha_salida DATE NOT NULL,
            cantidad_personas INTEGER NOT NULL,
            FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
            FOREIGN KEY (id_habitacion) REFERENCES habitaciones(id_habitacion),
            CHECK (fecha_salida > fecha_entrada)
        );
    ''')

    # Crear tabla de facturas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS facturas (
            id_factura INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER NOT NULL,
            id_reserva INTEGER NOT NULL,
            fecha_emision DATE NOT NULL,
            total REAL NOT NULL,
            FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
            FOREIGN KEY (id_reserva) REFERENCES reservas(id_reserva)
        );
    ''')

    # Crear tabla de empleados
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS empleados (
            id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            cargo TEXT CHECK(cargo IN ('recepcionista', 'servicio de limpieza', 'otros')) NOT NULL,
            sueldo REAL NOT NULL
        );
    ''')

    # Crear tabla de asignaciones de empleados a habitaciones
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS asignaciones (
            id_asignacion INTEGER PRIMARY KEY AUTOINCREMENT,
            id_empleado INTEGER NOT NULL,
            id_habitacion INTEGER NOT NULL,
            fecha DATE NOT NULL,
            FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado),
            FOREIGN KEY (id_habitacion) REFERENCES habitaciones(id_habitacion),
            UNIQUE(id_empleado, fecha, id_habitacion)
        );
    ''')

    # Confirmar cambios y cerrar conexión
    conn.commit()
    conn.close()

create_tables()
