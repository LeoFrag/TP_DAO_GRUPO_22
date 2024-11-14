import re
from models.cliente import Cliente

class ClienteService:
    def __init__(self, gestorBD):
        self.clientes = []
        self.gestorBD = gestorBD

    def validar_cliente(self, nombre, apellido, telefono, email, direccion):
        # Validación de campos requeridos
        if not nombre or not apellido or not telefono or not email or not direccion:
            raise ValueError("Todos los campos son requeridos")

        # Validación de que el nombre solo contenga letras y espacios
        if not nombre.isalpha():
            raise ValueError("El nombre debe contener solo letras")
        
        # Validación de que el apellido solo contenga letras y espacios
        if not apellido.isalpha():
            raise ValueError("El apellido debe contener solo letras")

        # Validación de teléfono (debe ser numérico y tener entre 7 y 15 dígitos)
        if not telefono.isdigit() or len(telefono) < 7 or len(telefono) > 15:
            raise ValueError("El teléfono debe ser un número válido entre 7 y 15 dígitos")

        # Validación de dirección (mínimo 10 caracteres)
        if len(direccion) < 10:
            raise ValueError("La dirección debe tener al menos 10 caracteres")

        return True

    def registrar_cliente(self, nombre, apellido, telefono, email, direccion):
        # Validar los datos
        if self.validar_cliente(nombre, apellido, telefono, email, direccion):
            id = self.gestorBD.obtener_proximo_id_cliente()
            cliente = Cliente(id, nombre, apellido, telefono, email, direccion)
            self.gestorBD.insertar_cliente(cliente.id_cliente, cliente.nombre, cliente.apellido, cliente.direccion, cliente.telefono, cliente.email)

    def obtener_clientes(self):
        clientes = self.gestorBD.obtener_clientes()
        return clientes