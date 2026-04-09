import re
from models.factura import Factura
from datetime import date


class FacturaService:
    def __init__(self, gestorBD):
        self.clientes = []
        self.gestorBD = gestorBD

    def validar_factura(self):
        pass

    def registrar_factura(self,id_reserva, id_cliente, total):
        id_factura = self.gestorBD.obtener_proximo_id_factura()
        fecha_emision = date.today()

        print(fecha_emision)
        self.gestorBD.insertar_factura(id_factura, id_cliente, id_reserva, fecha_emision, total)

    def obtener_facturas_detalladas(self):
        facturas_detalladas = self.gestorBD.obtener_facturas_detalladas()
        return facturas_detalladas
    
    def generar_factura(self, id_reserva, id_cliente, total):
        self.registrar_factura(id_reserva, id_cliente, total)
        return True