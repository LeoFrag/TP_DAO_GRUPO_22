import sqlite3
from datetime import date

# Nombre de la base de datos
DB_NAME = "hotel.db"

# Función para insertar datos en la tabla 'habitaciones'
def insertar_habitacion(habitacion):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO habitaciones (numero, tipo, precio_por_noche)
            VALUES (?, ?, ?)
        ''', (habitacion.numero, habitacion.tipo, habitacion.precio_por_noche))
        conn.commit()
        print(f"Habitación {habitacion.numero} insertada exitosamente.")
    except sqlite3.IntegrityError as e:
        print("Error al insertar habitación:", e)
    finally:
        conn.close()

# Función para insertar datos en la tabla 'clientes'
def insertar_cliente(cliente):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO clientes (nombre, apellido, direccion, telefono, email)
            VALUES (?, ?, ?, ?, ?)
        ''', (cliente.nombre, cliente.apellido, cliente.direccion, cliente.telefono, cliente.email))
        conn.commit()
        print(f"Cliente {cliente.nombre} {cliente.apellido} insertado exitosamente.")
    except sqlite3.IntegrityError as e:
        print("Error al insertar cliente:", e)
    finally:
        conn.close()

# Función para insertar datos en la tabla 'empleados'
def insertar_empleado(nombre, apellido, cargo, sueldo):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO empleados (nombre, apellido, cargo, sueldo)
            VALUES (?, ?, ?, ?)
        ''', (nombre, apellido, cargo, sueldo))
        conn.commit()
        print(f"Empleado {nombre} {apellido} insertado exitosamente.")
    except sqlite3.IntegrityError as e:
        print("Error al insertar empleado:", e)
    finally:
        conn.close()

