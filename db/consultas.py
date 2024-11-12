import sqlite3

# Nombre de la base de datos
DB_NAME = "hotel.db"

def obtener_habitaciones():
    # Conectar a la base de datos
    conn = sqlite3.connect(DB_NAME)  
    cursor = conn.cursor()

    try:
        # Realizar la consulta para obtener todas las habitaciones
        cursor.execute("SELECT numero, tipo, precio_por_noche, estado FROM habitaciones")
        # Devuelve los resultados como una lista de tuplas
        habitaciones = cursor.fetchall()
        return habitaciones

    except sqlite3.Error as e:
        print("Error al obtener los datos de la base de datos:", e)
        return None  # Retorna None si ocurre un error

    finally:
        # Cerrar la conexión (puedes decidir moverlo más tarde, si lo prefieres)
        conn.close()

def obtener_clientes():
    # Conectar a la base de datos
    conn = sqlite3.connect(DB_NAME)  
    cursor = conn.cursor()

    try:
        # Realizar la consulta para obtener todas los clientes
        cursor.execute("SELECT id_cliente, nombre, apellido, direccion, telefono, email FROM clientes")
        # Devuelve los resultados como una lista de tuplas
        clientes = cursor.fetchall()
        return clientes

    except sqlite3.Error as e:
        print("Error al obtener los datos de la base de datos:", e)
        return None  # Retorna None si ocurre un error

    finally:
        # Cerrar la conexión (puedes decidir moverlo más tarde, si lo prefieres)
        conn.close()


