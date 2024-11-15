import re
from models.factura import Factura

class FacturaService:
    def __init__(self, gestorBD):
        self.clientes = []
        self.gestorBD = gestorBD

    def validar_factura(self):
        pass

    def registrar_cliente(self, nombre, apellido, telefono, email, direccion):
        pass

    def obtener_facturas_detalladas(self):
        facturas_detalladas = self.gestorBD.obtener_facturas_detalladas()
        return facturas_detalladas