from models.reserva import Reserva

class ReservaService:
    def __init__(self, gestorBD):
        self.reservas = []
        self.gestorBD = gestorBD


    def validar_fechas(self, fechaInicio, fechaFin):
        return True

    def registrar_reserva(self):
        # Validar los datos
        if self.validar_reserva():
            reserva = Reserva()
            self.gestorBD.insertar_reserva()

    def buscar_habitaciones_disponibles(self,fechainicio, fechafin):
        if self.validar_fechas(fechainicio, fechafin):
            self.gestorBD.obtener_habitaciones_disponibles(fechainicio, fechafin)
