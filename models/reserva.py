import datetime
from models.cliente import Cliente
from models.habitacion import Habitacion

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
