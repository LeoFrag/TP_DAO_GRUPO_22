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

def obtener_reservas():
     # Conectar a la base de datos
    conn = sqlite3.connect(DB_NAME)  
    cursor = conn.cursor()

    try:
        # Realizar la consulta para obtener todas los clientes
        cursor.execute("SELECT id_reserva, id_cliente, id_habitacion ,fecha_entrada, fecha_salida, cantidad_personas FROM reservas")
        # Devuelve los resultados como una lista de tuplas
        clientes = cursor.fetchall()
        return clientes

    except sqlite3.Error as e:
        print("Error al obtener los datos de la base de datos:", e)
        return None  # Retorna None si ocurre un error

    finally:
        # Cerrar la conexión (puedes decidir moverlo más tarde, si lo prefieres)
        conn.close()


def obtener_asignaciones():
    # Conectar a la base de datos
    conn = sqlite3.connect('hotel.db')
    cursor = conn.cursor()

    # Consulta para obtener las asignaciones de empleados a habitaciones
    consulta = """
        SELECT asignaciones.id, empleados.nombre AS nombre_empleado, empleados.apellido AS apellido_empleado, 
               habitaciones.numero AS numero_habitacion
        FROM asignaciones
        JOIN empleados ON asignaciones.empleado_id = empleados.id
        JOIN habitaciones ON asignaciones.habitacion_id = habitaciones.id
    """

    cursor.execute(consulta)
    asignaciones = cursor.fetchall()
    conn.close()

    # Formatear los datos para que puedan ser usados en la interfaz
    resultado = []
    for asignacion in asignaciones:
        id_asignacion, nombre_empleado, apellido_empleado, numero_habitacion = asignacion
        resultado.append({
            "id": id_asignacion,
            "empleado": f"{nombre_empleado} {apellido_empleado}",
            "habitacion": numero_habitacion
        })

    return resultado

def obtener_empleados():
    # Conectar a la base de datos
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        # Realizar la consulta para obtener todas los clientes
        cursor.execute("SELECT id_empleado, nombre, apellido, cargo, sueldo FROM empleados")
        # Devuelve los resultados como una lista de tuplas
        empleados = cursor.fetchall()
        return empleados

    except sqlite3.Error as e:
        print("Error al obtener los datos de la base de datos:", e)
        return None  # Retorna None si ocurre un error

    finally:
        # Cerrar la conexión (puedes decidir moverlo más tarde, si lo prefieres)
        conn.close()