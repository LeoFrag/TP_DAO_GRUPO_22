import datetime
from collections import defaultdict
from typing import List, Optional, Dict
import random
from db.insercion import insertar_habitacion, insertar_cliente, insertar_reserva, insertar_asignacion, insertar_empleado  # Importar el método

# Clase Habitación
class Habitacion:

    def __init__(self, numero: int, tipo: str, precio_por_noche: float, estado="Disponible"):
        self.numero = numero
        self.tipo = tipo  # Simple, Doble, Suite
        self.estado = estado  # Disponible, Ocupada
        self.precio_por_noche = precio_por_noche

    def cambiar_estado(self, nuevo_estado):
        self.estado = nuevo_estado

    def __repr__(self):
        return f"Habitación {self.numero} ({self.tipo}) - Precio: {self.precio_por_noche}, Estado: {self.estado}"

# Clase Cliente
class Cliente:

    def __init__(self, id_cliente: int, nombre: str, apellido: str, direccion: str, telefono: str, email: str):

        self.id_cliente = id_cliente
        self.nombre = nombre
        self.apellido = apellido
        self.direccion = direccion
        self.telefono = telefono
        self.email = email

    def __repr__(self):
        return f"{self.apellido}, {self.nombre} (ID: {self.id_cliente})"

# Clase Reserva
class Reserva:

    def __init__(self, id_reserva: int, cliente: Cliente, habitacion: Habitacion, fecha_entrada: datetime.date,
                 fecha_salida: datetime.date, cantidad_personas: int):
        self.id_reserva = id_reserva
        self.cliente = cliente
        self.habitacion = habitacion
        self.fecha_entrada = fecha_entrada
        self.fecha_salida = fecha_salida
        self.cantidad_personas = cantidad_personas

    def __repr__(self):
        return f"Reserva {self.id_reserva} - Cliente: {self.cliente}, Habitación: {self.habitacion.numero}, Fecha entrada: {self.fecha_entrada}, Fecha salida: {self.fecha_salida}"

# Clase Factura
class Factura:

    def __init__(self, id_factura: int, cliente: Cliente, reserva: Reserva, fecha_emision: datetime.date, total: float):
        self.id_factura = id_factura
        self.cliente = cliente
        self.reserva = reserva
        self.fecha_emision = fecha_emision
        self.total = total

    def calcular_total(self):
        dias_estadia = (self.reserva.fecha_salida - self.reserva.fecha_entrada).days
        self.total = dias_estadia * self.reserva.habitacion.precio_por_noche

    def __repr__(self):
        return f"Factura {self.id_factura} - Cliente: {self.cliente}, Total: {self.total}, Fecha de emisión: {self.fecha_emision}"

# Clase Empleado
class Empleado:

    def __init__(self, id_empleado: int, nombre: str, apellido: str, cargo: str, sueldo: float):
        self.id_empleado = id_empleado
        self.nombre = nombre
        self.apellido = apellido
        self.cargo = cargo # Recepcionista, servicio de limpieza, etc
        self.sueldo = sueldo
        self.asignaciones_diarias = 0

    def asignar_habitacion(self):
        if self.asignaciones_diarias < 5:
            self.asignaciones_diarias += 1
        else:
            raise ValueError("Este empleado ya tiene 5 asignaciones diarias.")
        
    def __repr__(self):
        return f"Empleado {self.id_empleado} - {self.nombre} {self.apellido} ({self.cargo})"

# Clase Hotel
class Hotel:

    def __init__(self, conexion_db):
        self.conexion_db = conexion_db
        self.habitaciones = []
        self.clientes =  [] 
        self.reservas =  []
        self.facturas =  []
        self.empleados =  []

    # Registrar habitacion al sistema del hotel - Punto 1 

    def registrar_habitacion(self, numero, tipo, precio):

        habitacion = Habitacion(numero=numero, tipo=tipo, precio_por_noche=precio)

        insertar_habitacion(habitacion)

        print(f"Habitación registrada: {habitacion}")

    # Registrar clientes al sistema - Punto 2

    def registrar_cliente(self, nombre, apellido, telefono, email, direccion):
            
        cliente = Cliente(id_cliente=len(self.clientes)+1, nombre=nombre, apellido=apellido, direccion=direccion, telefono=telefono, email=email)

        insertar_cliente(cliente)

        print(f"Cliente registrado: {cliente}")

    # Registrar reserva - Punto 3


    def registrar_reserva(self, id_cliente: int, numero_habitacion: int, fecha_entrada: datetime.date, fecha_salida: datetime.date, cantidad_personas: int):
        with self.conexion_db as conexion:
            cursor = conexion.cursor()

            # Buscar el cliente en la base de datos
            cursor.execute("SELECT * FROM clientes WHERE id_cliente = ?", (id_cliente,))
            cliente_data = cursor.fetchone()
            if cliente_data is None:
                raise ValueError("El cliente no existe en el sistema.")
            cliente = Cliente(*cliente_data)  # Convierte los datos en una instancia de Cliente
            
            # Buscar la habitación en la base de datos
            cursor.execute("SELECT * FROM habitaciones WHERE numero = ?", (numero_habitacion,))
            habitacion_data = cursor.fetchone()
            if habitacion_data is None:
                raise ValueError("La habitación no existe en el sistema.")
            # Modifica el código para que `habitacion_data` solo pase los primeros 4 o 5 valores necesarios
            habitacion = Habitacion(*habitacion_data[:4])
            
            # Verificar disponibilidad de la habitación en las fechas solicitadas
            if not self._validar_fecha_reserva(cursor, numero_habitacion, fecha_entrada, fecha_salida):
                raise ValueError("La habitación ya está reservada en esas fechas.")
            
            # Crear instancia de reserva y guardar en la base de datos
            reserva = Reserva(
                id_reserva=len(self.reservas) + 1,
                cliente=cliente,
                habitacion=habitacion,
                fecha_entrada=fecha_entrada,
                fecha_salida=fecha_salida,
                cantidad_personas=cantidad_personas
            )
            habitacion.cambiar_estado("Ocupada")

            insertar_reserva(cliente.id_cliente, habitacion.numero, fecha_entrada, fecha_salida, cantidad_personas)
            print(f"Reserva registrada: {reserva}")

    # Método para validar disponibilidad de la habitación en las fechas solicitadas
    def _validar_fecha_reserva(self, cursor, id_habitacion: int, fecha_entrada: datetime.date, fecha_salida: datetime.date) -> bool:
        cursor.execute("""
            SELECT * FROM reservas 
            WHERE id_habitacion = ? 
            AND (fecha_entrada <= ? AND fecha_salida >= ?)
        """, (id_habitacion, fecha_salida, fecha_entrada))
        
        # Retorna True si no hay reservas en esas fechas, False en caso contrario
        return cursor.fetchone() is None
        
        
    def revisar_salidas_diarias(self):

        hoy = datetime.date.today()
        for reserva in self.reservas:
            if reserva.fecha_salida == hoy:
                self.generar_factura(reserva)

    def generar_factura(self, reserva: Reserva):

        total = (reserva.fecha_salida - reserva.fecha_entrada).days * reserva.habitacion.precio_por_noche
        factura = Factura(id_factura=len(self.facturas) + 1, cliente=reserva.cliente, reserva=reserva,
                          fecha_emision=datetime.date.today(), total=total)
        self.facturas.append(factura)
        reserva.habitacion.estado = 'disponible'

    def asignar_empleado_a_habitacion(self, id_empleado, id_habitacion, fecha=None):
        # Si no se proporciona una fecha, usar la fecha actual
        if fecha is None:
            fecha = datetime.date.today()

        # Verificar si el empleado es de limpieza
        empleado = next(
            (e for e in self.empleados if e.id_empleado == id_empleado and e.cargo == 'servicio de limpieza'), None)

        if not empleado:
            print("Empleado no encontrado o no es de limpieza.")
            return

        # Limitar las asignaciones diarias
        if empleado.asignaciones_diarias >= 5:
            print(f"Empleado {empleado.nombre} {empleado.apellido} ya tiene 5 asignaciones hoy.")
            return

        # Realizar la asignación en la base de datos
        try:
            insertar_asignacion(id_empleado, id_habitacion, fecha)
            empleado.asignar_habitacion()  # Actualizar el contador de asignaciones del empleado
            print(
                f"Empleado {empleado.nombre} {empleado.apellido} asignado a la habitación {id_habitacion} en la fecha {fecha}.")
        except Exception as e:
            print(f"Error al asignar empleado: {e}")

    # Verificar si las fechas de entrada y salida de las reservas no se superponen con la fecha dada.
    
    def consultar_disponibilidad(self, fecha: datetime.date) -> List[Habitacion]:
        disponibles = []
        for habitacion in self.habitaciones:
            if all(not (reserva.fecha_entrada <= fecha < reserva.fecha_salida) for reserva in self.reservas if reserva.habitacion == habitacion):
                disponibles.append(habitacion)
        return disponibles
    
    # Reportes

    def listar_reservas(self, fecha_inicio: datetime.date, fecha_fin: datetime.date) -> List[Reserva]:
        return [r for r in self.reservas if fecha_inicio <= r.fecha_entrada <= fecha_fin]

    def reporte_ingresos(self) -> float:
        return sum(factura.total for factura in self.facturas)

    def reporte_ocupacion_promedio(self) -> Dict[str, float]:
        total_ocupacion = defaultdict(int)
        contador = defaultdict(int)

        for reserva in self.reservas:
            total_ocupacion[reserva.habitacion.tipo] += (reserva.fecha_salida - reserva.fecha_entrada).days
            contador[reserva.habitacion.tipo] += 1

        return {tipo: total / (contador[tipo] or 1) for tipo, total in total_ocupacion.items()}

    def registrar_empleado(self, nombre, apellido, cargo, sueldo):

        empleado = Empleado(id_empleado=len(self.empleados) + 1, nombre=nombre, apellido=apellido, cargo=cargo, sueldo=sueldo)

        insertar_empleado(nombre, apellido, cargo, sueldo)

        print(f"Cliente registrado: {empleado}")