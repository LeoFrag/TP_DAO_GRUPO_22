import datetime
from collections import defaultdict
from typing import List, Optional, Dict
import random
from db.insercion import insertar_habitacion, insertar_cliente  # Importar el método

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

    def __init__(self):
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
    def _validar_fecha_reserva(self, habitacion: Habitacion, fecha_entrada: datetime.date, fecha_salida: datetime.date) -> bool:

        
        for reserva in self.reservas: # Validar que la habitacion esta reservada para las fechas que quiero reservar
            if reserva.habitacion == habitacion and not (fecha_salida <= reserva.fecha_entrada or fecha_entrada >= reserva.fecha_salida):
                return False
        return True

    def registrar_reserva(self, reserva: Reserva):

        if self._validar_fecha_reserva(reserva.habitacion, reserva.fecha_entrada, reserva.fecha_salida):
            reserva.habitacion.estado = 'ocupada'
            self.reservas.append(reserva)
        else:
            raise ValueError("La habitación ya está reservada en esas fechas.")
        
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

    def asignar_empleado_a_habitacion(self, empleado: Empleado, habitacion: Habitacion, fecha: datetime.date):
        asignaciones_dia = [asig for asig in empleado.asignaciones if asig[1] == fecha]
        if len(asignaciones_dia) < 5:
            empleado.asignaciones.append((habitacion, fecha))
        else:
            raise ValueError("El empleado no puede tener más de 5 asignaciones diarias.")
    
    """"
    def consultar_disponibilidad(self, fecha: datetime.date) -> List[Habitacion]:
        return [h for h in self.habitaciones if h.estado == 'disponible']
    """

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
