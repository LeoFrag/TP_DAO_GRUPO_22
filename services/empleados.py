import re
from models.empleado import Empleado

class EmpleadoService:
    def __init__(self, gestorBD):
        self.empleados = []
        self.gestorBD = gestorBD

    def obtener_empleados(self):
        
        empleados = self.gestorBD.obtener_empleados()
        return empleados
    
    