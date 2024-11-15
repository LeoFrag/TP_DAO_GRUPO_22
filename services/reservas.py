from models.reserva import Reserva
from services.facturas import FacturaService
from services.habitaciones import HabitacionService

class ReservaService:
    def __init__(self, gestorBD):
        self.reservas = []
        self.gestorBD = gestorBD
        self.facturasService = FacturaService(gestorBD)
        self.habitacionService = HabitacionService(gestorBD)


    def validar_fechas(self, fechaInicio, fechaFin):
        # Validar que la fecha de salida sea posterior a la de entrada
        if fechaFin < fechaInicio:
            return False
        return True

    def validar_reserva(self, num_personas):
        
        # Validación de que el número de habitación sea un número entero positivo
        if not num_personas.isdigit() or int(num_personas) <= 0:
            raise ValueError("El número de personas debe ser un entero positivo")
        
        return True
    
    def registrar_reserva(self, id_reserva, cliente_id, num_habitacion, fecha_inicio, fecha_fin, num_personas):
        # Validar los datos
        if self.validar_reserva(num_personas):
            reserva = Reserva(id_reserva, cliente_id, num_habitacion, fecha_inicio, fecha_fin, num_personas)
            self.gestorBD.insertar_reserva(reserva.id_reserva, reserva.cliente, reserva.habitacion, reserva.fecha_entrada, reserva.fecha_entrada, reserva.cantidad_personas)

    def obtener_reservas(self):
        reservas =self.gestorBD.obtener_reservas()
        return reservas
    
    def obtener_reservas_detalladas(self):
        reservas = self.gestorBD.obtener_reservas_detalladas()
        return reservas


    def buscar_habitaciones_disponibles(self,fechainicio, fechafin):
        habitaciones = self.gestorBD.obtener_habitaciones_disponibles(fechainicio, fechafin)
        return habitaciones
    
    def obtener_reservas_por_periodo(self, fechainicio, fechafin):
        reservas = self.gestorBD.obtener_reservas_por_periodo(fechainicio, fechafin)
        print(reservas)
        return reservas

    def finalizar_estadia(self, id_reserva, habitacion, dias):
        precio_por_noche = self.habitacionService.obtener_precio_por_noche(habitacion)
        total = precio_por_noche * dias
        id_cliente = self.gestorBD.obtener_cliente_reserva(id_reserva)
        self.facturasService.generar_factura(id_reserva, id_cliente[0], total)
        self.habitacionService.actualizar_estado_habitacion(habitacion, "disponible")
