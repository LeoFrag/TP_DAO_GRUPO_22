import datetime
from collections import defaultdict
from typing import List, Optional, Dict


class Habitacion:
    def __init__(self, numero: int, tipo: str, precio_por_noche: float):
        self.numero = numero
        self.tipo = tipo  # simple, doble, suite
        self.estado = 'disponible'  # disponible, ocupada
        self.precio_por_noche = precio_por_noche

    def __repr__(self):
        return f"Habitación {self.numero} ({self.tipo}) - Precio: {self.precio_por_noche}, Estado: {self.estado}"


class Cliente:
    def __init__(self, id_cliente: int, nombre: str, apellido: str, direccion: str, telefono: str, email: str):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.apellido = apellido
        self.direccion = direccion
        self.telefono = telefono
        self.email = email

    def __repr__(self):
        return f"{self.nombre} {self.apellido} (ID: {self.id_cliente})"


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


class Factura:
    def __init__(self, id_factura: int, cliente: Cliente, reserva: Reserva, fecha_emision: datetime.date, total: float):
        self.id_factura = id_factura
        self.cliente = cliente
        self.reserva = reserva
        self.fecha_emision = fecha_emision
        self.total = total

    def __repr__(self):
        return f"Factura {self.id_factura} - Cliente: {self.cliente}, Total: {self.total}, Fecha de emisión: {self.fecha_emision}"


class Empleado:
    def __init__(self, id_empleado: int, nombre: str, apellido: str, cargo: str, sueldo: float):
        self.id_empleado = id_empleado
        self.nombre = nombre
        self.apellido = apellido
        self.cargo = cargo
        self.sueldo = sueldo
        self.asignaciones = []  # List of assignments for cleaning

    def __repr__(self):
        return f"Empleado {self.id_empleado} - {self.nombre} {self.apellido} ({self.cargo})"


class Hotel:
    def __init__(self):
        self.habitaciones: List[Habitacion] = []
        self.clientes: List[Cliente] = []
        self.reservas: List[Reserva] = []
        self.facturas: List[Factura] = []
        self.empleados: List[Empleado] = []

    def registrar_habitacion(self, habitacion: Habitacion):
        self.habitaciones.append(habitacion)

    def registrar_cliente(self, cliente: Cliente):
        self.clientes.append(cliente)

    def _validar_fecha_reserva(self, habitacion: Habitacion, fecha_entrada: datetime.date, fecha_salida: datetime.date) -> bool:
        for reserva in self.reservas:
            if reserva.habitacion == habitacion and not (fecha_salida <= reserva.fecha_entrada or fecha_entrada >= reserva.fecha_salida):
                return False
        return True

    def registrar_reserva(self, reserva: Reserva):
        if self._validar_fecha_reserva(reserva.habitacion, reserva.fecha_entrada, reserva.fecha_salida):
            reserva.habitacion.estado = 'ocupada'
            self.reservas.append(reserva)
        else:
            raise ValueError("La habitación ya está reservada en esas fechas.")

    def generar_factura(self, reserva: Reserva):
        total = (reserva.fecha_salida - reserva.fecha_entrada).days * reserva.habitacion.precio_por_noche
        factura = Factura(id_factura=len(self.facturas) + 1, cliente=reserva.cliente, reserva=reserva,
                          fecha_emision=datetime.date.today(), total=total)
        self.facturas.append(factura)
        reserva.habitacion.estado = 'disponible'  # Free the room after billing

    def asignar_empleado_a_habitacion(self, empleado: Empleado, habitacion: Habitacion):
        if len(empleado.asignaciones) < 5:
            empleado.asignaciones.append(habitacion)
        else:
            raise ValueError("El empleado no puede tener más de 5 asignaciones diarias.")

    def consultar_disponibilidad(self, fecha: datetime.date) -> List[Habitacion]:
        return [h for h in self.habitaciones if h.estado == 'disponible']

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
