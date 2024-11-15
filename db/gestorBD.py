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
                FOREIGN KEY (numero_habitacion) REFERENCES habitaciones(numero_habitacion)
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
                cargo TEXT CHECK(cargo IN ('recepcionista', 'limpieza', 'gerente')) NOT NULL,
                sueldo REAL NOT NULL
            );
        ''')

        # Crear tabla de asignaciones de empleados a habitaciones
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS asignaciones (
                id_asignacion INTEGER PRIMARY KEY AUTOINCREMENT,
                id_empleado INTEGER NOT NULL,
                numero_habitacion INTEGER NOT NULL,
                fecha DATE NOT NULL,
                FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado),
                FOREIGN KEY (numero_habitacion) REFERENCES habitaciones(numero),
                UNIQUE(fecha, numero_habitacion)
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


        # Validar si ya existen datos en la tabla de empleados antes de insertar
        self.cursor.execute('SELECT COUNT(*) FROM empleados')
        if self.cursor.fetchone()[0] == 0:  # Si no hay registros
            self.cursor.executemany('''
                INSERT INTO empleados (nombre, apellido, cargo, sueldo)
                VALUES (?, ?, ?, ?)
            ''', [
                ('Ana', 'Ramírez', 'recepcionista', 2000.0),
                ('Luis', 'Martínez', 'limpieza', 1800.0),
                ('Clara', 'Sánchez', 'gerente', 2500.0)
            ])

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
            return True
        else:
            return False

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
        
    def obtener_cliente_reserva(self, id_reserva):
        """Obtiene el cliente asociado a una reserva."""
        self.conectar()
        consulta = 'SELECT id_cliente FROM reservas WHERE id_reserva = ?'
        cursor = self.ejecutar_consulta(consulta, (id_reserva,))
        if cursor:
            id_cliente = cursor.fetchone()
            #self.desconectar()
            return id_cliente
        else:
            return None
        
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
    def obtener_reservas_detalladas(self):
        """Obtiene todas las reservas detalladas de la base de datos."""
        self.conectar()
        
        # Consulta para obtener reservas con detalles de cliente y habitación
        consulta = '''
            SELECT r.id_reserva, c.nombre, c.apellido, r.numero_habitacion, r.fecha_entrada, r.fecha_salida
            FROM reservas r
            JOIN clientes c ON r.id_cliente = c.id_cliente
            JOIN habitaciones h ON r.numero_habitacion = h.numero
        '''
        
        cursor = self.ejecutar_consulta(consulta)
        if cursor:
            reservas = cursor.fetchall()
            # self.desconectar()
            return reservas
        else:
            # self.desconectar()
            return []

    def obtener_tipo_habitacion(self, numero):
        """Obtiene el tipo de habitación asociado a una reserva."""
        self.conectar()
        consulta = 'SELECT tipo FROM habitaciones WHERE numero = ?'
        cursor = self.ejecutar_consulta(consulta, (numero,))
        if cursor:
            tipo = cursor.fetchone()
            #self.desconectar()
            return tipo
        else:
            #self.desconectar()
            return None
        
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

    def obtener_facturas_detalladas(self):
        consulta = '''
            SELECT f.id_reserva AS nro_reserva, c.nombre, c.apellido, r.numero_habitacion, f.fecha_emision, f.total
            FROM facturas f
            JOIN clientes c ON f.id_cliente = c.id_cliente
            JOIN reservas r ON f.id_reserva = r.id_reserva
        '''
        cursor = self.ejecutar_consulta(consulta)
        return cursor.fetchall() if cursor else []
    
    def obtener_reservas_por_periodo(self, fechainicio, fechafin):
        consulta = "SELECT * FROM reservas WHERE fecha_entrada >= ? AND fecha_salida <= ?"
        cursor = self.ejecutar_consulta(consulta, (fechainicio, fechafin))
        return cursor.fetchall() if cursor else []

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
        consulta = '''
            SELECT numero
            FROM habitaciones
            WHERE numero NOT IN (
                SELECT numero_habitacion
                FROM reservas
                WHERE (fecha_entrada <= ? AND fecha_salida >= ?) 
                   OR (fecha_entrada <= ? AND fecha_salida >= ?)
                   OR (fecha_entrada >= ? AND fecha_salida <= ?)
            );
        '''
        # Ejecutar la consulta con los parámetros
        cursor = self.ejecutar_consulta(consulta, (fecha_fin, fecha_inicio, fecha_fin, fecha_inicio, fecha_inicio, fecha_fin))
        return cursor.fetchall() if cursor else []
    
    def obtener_habitaciones_disponibles_por_fecha(self, fecha):
        consulta = '''
            SELECT numero, tipo, precio_por_noche
            FROM habitaciones
            WHERE numero NOT IN (
                SELECT numero_habitacion
                FROM reservas
                WHERE ? BETWEEN fecha_entrada AND fecha_salida
            );
        '''
        # Ejecutar la consulta con la fecha como parámetro
        cursor = self.ejecutar_consulta(consulta, (fecha,))
        return cursor.fetchall() if cursor else []
    
    def obtener_habitaciones_disponibles_por_asignar(self, fecha):
        consulta = '''
            SELECT numero, tipo 
            FROM habitaciones
            WHERE numero NOT IN (
                SELECT numero_habitacion
                FROM asignaciones
                WHERE fecha = ?  
            );
        '''

        # Ejecutar la consulta con la fecha como parámetro
        cursor = self.ejecutar_consulta(consulta, (fecha,))
        return cursor.fetchall() if cursor else []
    
    def obtener_precio_por_noche(self, numero_habitacion):
        consulta = 'SELECT precio_por_noche FROM habitaciones WHERE numero = ?'
        cursor = self.ejecutar_consulta(consulta, (numero_habitacion,))
        precio = cursor.fetchone()
        return precio[0] if precio else None
    
    def obtener_empleado_por_id(self, id_empleado):
        consulta = 'SELECT * FROM empleados WHERE id_empleado = ?'
        cursor = self.ejecutar_consulta(consulta, (id_empleado,))
        return cursor.fetchone() if cursor else None
    
    def verificar_disponibilidad_limpieza(self, numero_habitacion, fecha):
        """
        Verifica si una habitación está disponible para limpieza en una fecha específica.
        """
        consulta = '''
            SELECT COUNT(*) FROM asignaciones
            WHERE numero_habitacion = ? AND fecha = ?
        '''
        cursor = self.ejecutar_consulta(consulta, (numero_habitacion, fecha))
        resultado = cursor.fetchone()

        if resultado is None:
            # Si no hay resultados, asumimos que la habitación está disponible
            return True

        # `resultado[0]` contiene el número de registros encontrados
        count = resultado[0]
        return count == 0  # Disponible si no hay asignaciones
    
    def validar_email(self, email):
        consulta = 'SELECT 1 FROM clientes WHERE email = ?'
        cursor = self.ejecutar_consulta(consulta, (email,))
        # Si hay un resultado, devolver True; de lo contrario, False
        return cursor.fetchone() is not None
    
    def asignar_limpieza(self, numero_habitacion, id_empleado, fecha):
        consulta = """
        INSERT INTO asignaciones (numero_habitacion, id_empleado, fecha)
        VALUES (?, ?, ?)
        """
        cursor = self.ejecutar_consulta(consulta, (numero_habitacion, id_empleado, fecha))
        print(f"Ejecutando consulta: {consulta} con parámetros {numero_habitacion}, {id_empleado}, {fecha}")
 

# ---------------------------------------------------- ACTUALIZACIONES ---------------------------------------------------------
    
    def actualizar_estado_habitacion(self, numero, estado):
        """Actualiza el estado de una habitación por su número."""
        consulta = 'UPDATE habitaciones SET estado = ? WHERE numero = ?'
        resultado = self.ejecutar_consulta(consulta, (estado, numero))
        if resultado:
            print("Estado de la habitación actualizado correctamente.")

# ------------------------------------------------------ ELIMINAR --------------------------------------------------------

    def eliminar_reserva(self, id_reserva):
        """Elimina una reserva por su ID."""
        consulta = 'DELETE FROM reservas WHERE id_reserva = ?'
        self.ejecutar_consulta(consulta, (id_reserva,))
# ---------------------------------------------------- IDS ---------------------------------------------------------

    def obtener_proximo_id_cliente(self):
        """Obtiene el próximo ID de cliente disponible."""
        consulta = "SELECT MAX(id_cliente) FROM clientes"
        cursor = self.ejecutar_consulta(consulta)
        max_id = cursor.fetchone()[0]
        return (max_id + 1) if max_id else 1
    
    def obtener_proximo_id_reserva(self):
        """Obtiene el próximo ID de reserva disponible."""
        consulta = "SELECT MAX(id_reserva) FROM reservas"
        cursor = self.ejecutar_consulta(consulta)
        max_id = cursor.fetchone()[0]
        return (max_id + 1) if max_id else 1

    def obtener_proximo_id_factura(self):
        """Obtiene el próximo ID de factura disponible."""
        consulta = "SELECT MAX(id_factura) FROM facturas"
        cursor = self.ejecutar_consulta(consulta)
        max_id = cursor.fetchone()[0]
        return (max_id + 1) if max_id else 1