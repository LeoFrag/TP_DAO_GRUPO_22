from models.habitacion import Habitacion

class HabitacionService:
    def __init__(self, gestorBD):
        self.habitaciones = []
        self.gestorBD = gestorBD


    def validar_habitacion(self, numero, tipo, precio):
        # Validación de campos requeridos
        if not numero or not tipo or not precio:
            raise ValueError("Todos los campos son requeridos")
        
        # Validación de que el número de habitación sea un número entero positivo
        if not numero.isdigit() or int(numero) <= 0:
            raise ValueError("El número de habitación debe ser un entero positivo")
        
        # Validación de que el precio sea un número válido y mayor a cero
        try:
            precio_float = float(precio)
            if precio_float <= 0:
                raise ValueError("El precio debe ser un número mayor a cero")
        except ValueError:
            raise ValueError("El precio debe ser un número válido")
        
        # Validación de longitud o formato adicional (opcional)
        if len(numero) > 4:
            raise ValueError("El número de habitación no puede exceder 4 dígitos")

        return True

    def registrar_habitacion(self, numero, tipo, precio):
        # Validar los datos
        if self.validar_habitacion(numero, tipo, precio):
            habitacion = Habitacion(numero, tipo, precio)
            self.gestorBD.insertar_habitacion(habitacion.numero, habitacion.tipo, habitacion.precio_por_noche)

    def obtener_habitaciones(self):
        habitaciones = self.gestorBD.obtener_habitaciones()
        return habitaciones
