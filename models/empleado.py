class Empleado:

    def __init__(self, id_empleado: int, nombre: str, apellido: str, cargo: str, sueldo: float):
        self.id_empleado = id_empleado
        self.nombre = nombre
        self.apellido = apellido
        self.cargo = cargo # Recepcionista, servicio de limpieza, etc
        self.sueldo = sueldo
        
    def __repr__(self):
        return f"Empleado {self.id_empleado} - {self.nombre} {self.apellido} ({self.cargo})"
