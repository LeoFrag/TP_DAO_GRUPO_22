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
