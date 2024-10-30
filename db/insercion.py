import sqlite3
from datetime import date

# Nombre de la base de datos
DB_NAME = "hotel.db"

# Función para insertar datos en la tabla 'habitaciones'
def insertar_habitacion(numero, tipo, precio_por_noche):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO habitaciones (numero, tipo, precio_por_noche)
            VALUES (?, ?, ?)
        ''', (numero, tipo, precio_por_noche))
        conn.commit()
        print(f"Habitación {numero} insertada exitosamente.")
    except sqlite3.IntegrityError as e:
        print("Error al insertar habitación:", e)
    finally:
        conn.close()

# Función para insertar datos en la tabla 'clientes'
def insertar_cliente(nombre, apellido, direccion, telefono, email):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO clientes (nombre, apellido, direccion, telefono, email)
            VALUES (?, ?, ?, ?, ?)
        ''', (nombre, apellido, direccion, telefono, email))
        conn.commit()
        print(f"Cliente {nombre} {apellido} insertado exitosamente.")
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

# Agregar tres registros de ejemplo en cada tabla
def main():
    # Insertar habitaciones
    insertar_habitacion(101, 'doble', 120.0)
    insertar_habitacion(102, 'simple', 80.0)
    insertar_habitacion(103, 'suite', 200.0)

    # Insertar clientes
    insertar_cliente("Ana", "Martínez", "Calle 123", "555-1234", "ana@example.com")
    insertar_cliente("Juan", "Pérez", "Avenida 456", "555-5678", "juan@example.com")
    insertar_cliente("Luisa", "Gómez", "Plaza 789", "555-8765", "luisa@example.com")

    # Insertar empleados
    insertar_empleado("Carlos", "Sánchez", "recepcionista", 1500.0)
    insertar_empleado("Marta", "Lopez", "servicio de limpieza", 1200.0)
    insertar_empleado("Pedro", "Ramírez", "recepcionista", 1500.0)

if __name__ == "__main__":
    main()
