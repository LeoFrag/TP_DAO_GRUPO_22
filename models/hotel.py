
import datetime
from collections import defaultdict
from typing import List, Dict
from db.insercion import insertar_habitacion, insertar_cliente, insertar_reserva  # Importar el método
from db.consultas import obtener_habitacion_por_numero
from db.consultas import validar_fecha_reserva

from models.habitacion import Habitacion
from models.cliente import Cliente
from models.reserva import Reserva
from models.factura import Factura
from models.empleado import Empleado

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


    def registrar_reserva(self, id_cliente: int, numero_habitacion: int, fecha_entrada: datetime.date, fecha_salida: datetime.date, cantidad_personas: int):
        # Validar disponibilidad de la habitación en las fechas solicitadas
        if not validar_fecha_reserva(numero_habitacion, fecha_entrada, fecha_salida):
            raise ValueError("La habitación ya está reservada en esas fechas.")
        
        # Crear instancia de reserva y guardar en la base de datos
        reserva = Reserva(
            id_reserva=len(self.reservas) + 1,
            cliente=id_cliente,
            habitacion=numero_habitacion,
            fecha_entrada=fecha_entrada,
            fecha_salida=fecha_salida,
            cantidad_personas=cantidad_personas
        )

        # Obtener los datos de la habitación
        datos = obtener_habitacion_por_numero(numero_habitacion)
        habitacion = Habitacion(datos[0], datos[1], datos[2], datos[3])

        # Cambiar el estado de la habitación a 'Ocupada'
        habitacion.cambiar_estado("Ocupada")

        # Insertar la reserva en la base de datos
        insertar_reserva(id_cliente, habitacion.numero, fecha_entrada, fecha_salida, cantidad_personas)
        print(f"Reserva registrada: {reserva}")


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

        '''    def registrar_reserva(self, reserva: Reserva):

        if self._validar_fecha_reserva(reserva.habitacion, reserva.fecha_entrada, reserva.fecha_salida):
            reserva.habitacion.estado = 'ocupada'
            self.reservas.append(reserva)
        else:
            raise ValueError("La habitación ya está reservada en esas fechas.")'''
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
