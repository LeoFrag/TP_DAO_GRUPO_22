import datetime
import sqlite3  # Asegúrate de usar la librería adecuada para tu base de datos
from classes import Hotel, Habitacion, Cliente, Reserva
import tkinter as tk
from interfaz import HotelApp

# Conectar a la base de datos
conexion_db = sqlite3.connect("hotel.db")  

# Inicializar instancia de Hotel con la conexión a la base de datos
hotel = Hotel(conexion_db)

# Inicializar Tkinter
root = tk.Tk()
app = HotelApp(root, hotel)
root.mainloop()

# Ejemplo de uso del sistema de gestión de hotel
if __name__ == "__main__":
    hotel = Hotel(conexion_db)
