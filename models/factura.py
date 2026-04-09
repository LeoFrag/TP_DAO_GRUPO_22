from models.cliente import Cliente
from models.reserva import Reserva
import datetime

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


