import datetime
from classes import Hotel, Habitacion, Cliente, Reserva

# Ejemplo de uso del sistema de gestión de hotel
if __name__ == "__main__":
    hotel = Hotel()

    # Registro de habitaciones
    hotel.registrar_habitacion(Habitacion(101, "simple", 100.0))
    hotel.registrar_habitacion(Habitacion(102, "doble", 150.0))
    hotel.registrar_habitacion(Habitacion(201, "suite", 250.0))

    # Registro de clientes
    cliente1 = Cliente(1, "Juan", "Pérez", "Calle 123", "123456789", "juan@example.com")
    hotel.registrar_cliente(cliente1)

    # Registro de reservas
    reserva1 = Reserva(1, cliente1, hotel.habitaciones[0], datetime.date(2024, 10, 20), datetime.date(2024, 10, 25), 2)
    hotel.registrar_reserva(reserva1)

    # Generación de factura
    hotel.generar_factura(reserva1)

    # Consulta de disponibilidad
    print("Habitaciones disponibles:", hotel.consultar_disponibilidad(datetime.date(2024, 10, 20)))

    # Reporte de ingresos
    print("Total ingresos:", hotel.reporte_ingresos())

    # Reporte de ocupación promedio
    print("Ocupación promedio por tipo de habitación:", hotel.reporte_ocupacion_promedio())
