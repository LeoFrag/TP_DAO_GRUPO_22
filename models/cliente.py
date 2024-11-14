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
