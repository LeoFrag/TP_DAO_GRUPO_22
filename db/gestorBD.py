import sqlite3
import os

DB_PATH = "db/hotel.db"

class GestorBD:
    _instance = None  # Variable de clase para almacenar la única instancia de GestorDB

    def __new__(cls, db_name=DB_PATH):
        # Verifica si _instance es None, lo que significa que aún no se ha creado una instancia
        
        if cls._instance is None:
            # Si no hay una instancia, se crea una usando __new__ del padre (super)
            cls._instance = super(GestorBD, cls).__new__(cls)
            # Asigna el nombre de la base de datos a la instancia única
            cls._instance.db_name = db_name
            # Inicializa la variable de conexión como None para más adelante establecer la conexión a la BD
            cls._instance.conn = None
            print("Creando la única instancia de GestorDB (Singleton).")
        # Devuelve la instancia única
        return cls._instance
    
    def __init__(self, db_name=DB_PATH):
        # Este método está intencionalmente vacío. La inicialización en el Singleton se maneja en __new__.
        # De esta forma, __init__ no sobreescribe la instancia existente.
        pass
        # self.db_name = db_name
        # self.conn = None
        # print("Constructor de GestorBD.")


    def borrar_base_de_datos(self):
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
            print("Base de datos borrada exitosamente.")
        else:
            print("No se encontró ninguna base de datos para borrar.")

    def crear_base_de_datos(self):
        """Crea una base de datos SQLite con tablas iniciales."""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print("Base de datos creada exitosamente.")
        except sqlite3.Error as e:
            print(f"Error al crear la base de datos: {e}")

    def conectar(self):
        """Establece la conexión con la base de datos."""
        try:
            if self.conn is None:
                self.conn = sqlite3.connect(self.db_name)
                self.cursor = self.conn.cursor()  # Asegúrate de que esta línea esté presente
            print("Conexión a la base de datos establecida..")
        except sqlite3.Error as e:
            print(f"Error al conectar con la base de datos: {e}")

    def desconectar(self):
        """Cierra la conexión con la base de datos."""
        if self.conn:
            self.conn.close()
            print("Conexión a la base de datos cerrada.")

    def mostrar_tablas(self):
        """Muestra las tablas de la base de datos."""
        self.conectar()
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = self.cursor.fetchall()
        print("Tablas en la base de datos:")
        for tabla in tablas:
            print(tabla[0])
        ##self.desconectar()()

    def ejecutar_consulta(self, consulta, parametros=()):
        """Ejecuta una consulta SQL con parámetros opcionales."""
        try:
            if self.conn is None:
                self.conectar()  # Asegúrate de que la conexión esté abierta
            cursor = self.conn.cursor()
            cursor.execute(consulta, parametros)
            self.conn.commit()
            return cursor
        except sqlite3.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return None

    def borrar_datos_de_tablas(self):
        """Borra los datos de todas las tablas de la base de datos."""
        self.conectar()
        tablas = ['habitaciones', 'clientes', 'empleados', 'reservas', 'facturas', 'servicio_limpieza']
        for tabla in tablas:
            self.cursor.execute(f"DELETE FROM {tabla}")
        self.conn.commit()
        print("Datos de las tablas eliminados correctamente.")
# ------------------------------------------------ CREAR E INSERTAR DATOS EN TABLA -----------------------------------------------------

    def crear_tablas(self):
        # Conectar a la base de datos
        
        self.conectar()

        # Crear tabla de habitaciones
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS habitaciones (
                id_habitacion INTEGER PRIMARY KEY AUTOINCREMENT,
                numero INTEGER NOT NULL UNIQUE,
                tipo TEXT NOT NULL,
                estado TEXT DEFAULT 'disponible',
                precio_por_noche REAL NOT NULL
            );
        ''')

        # Crear tabla de clientes
        self.cursor.execute('''
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
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS reservas (
                id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
                id_cliente INTEGER NOT NULL,
                numero_habitacion INTEGER NOT NULL,
                fecha_entrada DATE NOT NULL,
                fecha_salida DATE NOT NULL,
                cantidad_personas INTEGER NOT NULL,
                FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
                FOREIGN KEY (numero_habitacion) REFERENCES habitaciones(numero_habitacion),
                CHECK (fecha_salida > fecha_entrada)
            );
        ''')

        # Crear tabla de facturas
        self.cursor.execute('''
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
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS empleados (
                id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                cargo TEXT CHECK(cargo IN ('recepcionista', 'servicio de limpieza', 'otros')) NOT NULL,
                sueldo REAL NOT NULL
            );
        ''')

        # Crear tabla de asignaciones de empleados a habitaciones
        self.cursor.execute('''
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

        # Validar si ya existen datos en la tabla de habitaciones antes de insertar
        self.cursor.execute('SELECT COUNT(*) FROM habitaciones')
        if self.cursor.fetchone()[0] == 0:  # Si no hay registros
            self.cursor.executemany('''
                INSERT INTO habitaciones (numero, tipo, estado, precio_por_noche)
                VALUES (?, ?, ?, ?)
            ''', [
                (101, 'simple', 'disponible', 50.0),
                (102, 'doble', 'disponible', 80.0),
                (103, 'suite', 'disponible', 150.0)
            ])

        # Validar si ya existen datos en la tabla de clientes antes de insertar
        self.cursor.execute('SELECT COUNT(*) FROM clientes')
        if self.cursor.fetchone()[0] == 0:  # Si no hay registros
            self.cursor.executemany('''
                INSERT INTO clientes (nombre, apellido, direccion, telefono, email)
                VALUES (?, ?, ?, ?, ?)
            ''', [
                ('Juan', 'Pérez', 'Calle Falsa 123', '555-1234', 'juan.perez@example.com'),
                ('María', 'González', 'Av. Siempre Viva 742', '555-5678', 'maria.gonzalez@example.com'),
                ('Carlos', 'López', 'Av. Libertador 456', '555-8765', 'carlos.lopez@example.com')
            ])

        # Validar si ya existen datos en la tabla de reservas antes de insertar
        self.cursor.execute('SELECT COUNT(*) FROM reservas')
        if self.cursor.fetchone()[0] == 0:  # Si no hay registros
            self.cursor.executemany('''
                INSERT INTO reservas (id_cliente, numero_habitacion, fecha_entrada, fecha_salida, cantidad_personas)
                VALUES (?, ?, ?, ?, ?)
            ''', [
                (1, 101, '2024-11-15', '2024-11-20', 1),
                (2, 102, '2024-12-01', '2024-12-05', 2),
                (3, 103, '2024-12-10', '2024-12-15', 3)
            ])

        # Validar si ya existen datos en la tabla de facturas antes de insertar
        self.cursor.execute('SELECT COUNT(*) FROM facturas')
        if self.cursor.fetchone()[0] == 0:  # Si no hay registros
            self.cursor.executemany('''
                INSERT INTO facturas (id_cliente, id_reserva, fecha_emision, total)
                VALUES (?, ?, ?, ?)
            ''', [
                (1, 1, '2024-11-15', 250.0),
                (2, 2, '2024-12-01', 400.0),
                (3, 3, '2024-12-10', 750.0)
            ])

        # Validar si ya existen datos en la tabla de empleados antes de insertar
        self.cursor.execute('SELECT COUNT(*) FROM empleados')
        if self.cursor.fetchone()[0] == 0:  # Si no hay registros
            self.cursor.executemany('''
                INSERT INTO empleados (nombre, apellido, cargo, sueldo)
                VALUES (?, ?, ?, ?)
            ''', [
                ('Ana', 'Ramírez', 'recepcionista', 2000.0),
                ('Luis', 'Martínez', 'servicio de limpieza', 1800.0),
                ('Clara', 'Sánchez', 'otros', 2500.0)
            ])

        # Validar si ya existen datos en la tabla de asignaciones antes de insertar
        self.cursor.execute('SELECT COUNT(*) FROM asignaciones')
        if self.cursor.fetchone()[0] == 0:  # Si no hay registros
            self.cursor.executemany('''
                INSERT INTO asignaciones (id_empleado, id_habitacion, fecha)
                VALUES (?, ?, ?)
            ''', [
                (1, 101, '2024-11-15'),
                (2, 102, '2024-11-16'),
                (3, 103, '2024-11-17')
            ])

        print("Tablas y datos creados correctamente")

# ------------------------------------------------INSERTAR REGISTRO -----------------------------------------------------
    def insertar_habitacion(self, numero, tipo, precio_por_noche, estado="disponible"):
            """Inserta una nueva habitación en la base de datos."""
            consulta = '''
                INSERT INTO habitaciones (numero, tipo, precio_por_noche, estado)
                VALUES (?, ?, ?, ?)
            '''
            resultado = self.ejecutar_consulta(consulta, (numero, tipo, precio_por_noche, estado))
            if resultado:
                print("Habitación insertada correctamente.")
        
    def insertar_cliente(self, id_cliente, nombre, apellido, direccion, telefono, email):
        """Inserta un nuevo cliente en la base de datos."""
        consulta = '''
            INSERT INTO clientes (id_cliente, nombre, apellido, direccion, telefono, email)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        resultado = self.ejecutar_consulta(consulta, (id_cliente, nombre, apellido, direccion, telefono, email))
        if resultado:
            print("Cliente insertado correctamente.")

    def insertar_reserva(self, id_reserva, id_cliente, numero_habitacion, fecha_entrada, fecha_salida, cantidad_personas):
        """Inserta una nueva reserva en la base de datos como una transacción."""
        consulta = '''
            INSERT INTO reservas (id_reserva, id_cliente, numero_habitacion, fecha_entrada, fecha_salida, cantidad_personas)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        try:
            self.conectar()
            self.conn.execute('BEGIN TRANSACTION')
            resultado = self.ejecutar_consulta(consulta, (id_reserva, id_cliente, numero_habitacion, fecha_entrada, fecha_salida, cantidad_personas))
            if resultado:
                self.conn.commit()
                print("Reserva insertada correctamente.")
            else:
                self.conn.rollback()
                print("Error al insertar la reserva. Transacción revertida.")
        except sqlite3.Error as e:
            self.conn.rollback()
            print(f"Error al insertar la reserva: {e}. Transacción revertida.")
        finally:
            #self.desconectar()
            pass

    def insertar_factura(self, id_factura, id_cliente, id_reserva, fecha_emision, total):
        """Inserta una nueva factura en la base de datos como una transacción."""
        consulta = '''
            INSERT INTO facturas (id_factura, id_cliente, id_reserva, fecha_emision, total)
            VALUES (?, ?, ?, ?, ?)
        '''
        try:
            self.conectar()
            self.conn.execute('BEGIN TRANSACTION')
            resultado = self.ejecutar_consulta(consulta, (id_factura, id_cliente, id_reserva, fecha_emision, total))
            if resultado:
                self.conn.commit()
                print("Factura insertada correctamente.")
            else:
                self.conn.rollback()
                print("Error al insertar la factura. Transacción revertida.")
        except sqlite3.Error as e:
            self.conn.rollback()
            print(f"Error al insertar la factura: {e}. Transacción revertida.")
        finally:
            #self.desconectar()
            pass

    def insertar_empleado(self, id_empleado, nombre, apellido, cargo, sueldo):
        """Inserta un nuevo empleado en la base de datos."""
        consulta = '''
            INSERT INTO empleados (id_empleado, nombre, apellido, cargo, sueldo)
            VALUES (?, ?, ?, ?, ?)
        '''
        self.ejecutar_consulta(consulta, (id_empleado, nombre, apellido, cargo, sueldo))
        print("Empleado insertado correctamente.")
    
# -------------------------------------------------- CONSULTAS ---------------------------------------------------------------

    def obtener_habitaciones(self):
        """Obtiene todas las habitaciones de la base de datos."""
        self.conectar()
        consulta = 'SELECT * FROM habitaciones'
        cursor = self.ejecutar_consulta(consulta)
        if cursor:
            habitaciones = cursor.fetchall()
            #self.desconectar()
            return habitaciones
        else:
            print("No se pudieron obtener las habitaciones.")
            ##self.desconectar()
            return []
   
    def obtener_habitacion(self, numero):
        """Obtiene una habitación específica por su número."""
        self.conectar()
        consulta = 'SELECT * FROM habitaciones WHERE numero = ?'
        cursor = self.ejecutar_consulta(consulta, (numero,))
        if cursor:
            habitacion = cursor.fetchone()
            #self.desconectar()
            return habitacion
        else:
            print("No se pudo obtener la habitación.")
            #self.desconectar()
            return None
        
    def obtener_clientes(self):
        """Obtiene todos los clientes de la base de datos."""
        self.conectar()
        consulta = 'SELECT * FROM clientes'
        cursor = self.ejecutar_consulta(consulta)
        if cursor:
            clientes = cursor.fetchall()
            #self.desconectar()
            print("Clientes obtenidos correctamente.")
            return clientes
        else:
            print("No se pudieron obtener los clientes.")
            #self.desconectar()
            return []
        
    def obtener_reservas(self):
        
        """Obtiene todas las reservas de la base de datos."""
        self.conectar()
        consulta = 'SELECT * FROM reservas'
        cursor = self.ejecutar_consulta(consulta)
        if cursor:
            reservas = cursor.fetchall()
            #self.desconectar()
            return reservas
        else:
            #self.desconectar()
            return []
        
    def validar_disponibilidad_habitacion(self, numero_habitacion, fecha_entrada, fecha_salida):
        """Verifica si una habitación está disponible en las fechas seleccionadas."""
        consulta = """
            SELECT * FROM reservas 
            WHERE numero_habitacion = ? 
            AND (fecha_salida >= ? AND fecha_entrada <= ?)
        """
        parametros = (numero_habitacion, fecha_entrada, fecha_salida)
        cursor = self.ejecutar_consulta(consulta, parametros)
        return cursor.fetchone() is None
    
    def obtener_facturas(self):
        
        """Obtiene todas las facturas de la base de datos."""
        self.conectar()
        consulta = 'SELECT * FROM facturas'
        cursor = self.ejecutar_consulta(consulta)
        if cursor:
            facturas = cursor.fetchall()
            #self.desconectar()
            return facturas
        else:
            #self.desconectar()()
            return []
        

    def obtener_empleados(self):
        
        """Obtiene todos los empleados de la base de datos."""
        self.conectar()
        consulta = 'SELECT * FROM empleados'
        cursor = self.ejecutar_consulta(consulta)
        if cursor:
            empleados = cursor.fetchall()
            #self.desconectar()()
            return empleados
        else:
            #self.desconectar()()
            return []
        
    def obtener_habitaciones_disponibles(self, fecha_inicio, fecha_fin):
        consulta = """
            SELECT h.numero, h.tipo
            FROM habitaciones h
            LEFT JOIN reservas r ON h.numero = r.numero_habitacion
            WHERE h.estado = 'disponible'
            AND (
                r.numero_habitacion IS NULL
                OR (r.fecha_salida < ? OR r.fecha_entrada > ?)
            )
        """
        parametros = (fecha_inicio, fecha_fin)
        cursor = self.ejecutar_consulta(consulta, parametros)
        return {f"{habitacion[0]}-{habitacion[1]}": habitacion[0] for habitacion in cursor.fetchall()} if cursor else {}
    
# ---------------------------------------------------- ACTUALIZACIONES ---------------------------------------------------------
    
    def actualizar_estado_habitacion(self, numero, estado):
        """Actualiza el estado de una habitación por su número."""
        consulta = 'UPDATE habitaciones SET estado = ? WHERE numero = ?'
        resultado = self.ejecutar_consulta(consulta, (estado, numero))
        if resultado:
            print("Estado de la habitación actualizado correctamente.")

# ---------------------------------------------------- IDS ---------------------------------------------------------

    def obtener_proximo_id_cliente(self):
        """Obtiene el próximo ID de cliente disponible."""
        consulta = "SELECT MAX(id_cliente) FROM clientes"
        cursor = self.ejecutar_consulta(consulta)
        max_id = cursor.fetchone()[0]
        return (max_id + 1) if max_id else 1