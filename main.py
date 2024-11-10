import datetime
from classes import Hotel, Habitacion, Cliente, Reserva 
import tkinter as tk
from interfaz import HotelApp

# Inicializar instancia de Hotel
hotel = Hotel()

# Inicializar Tkinter
root = tk.Tk()
app = HotelApp(root, hotel)
root.mainloop()

# Ejemplo de uso del sistema de gestión de hotel
if __name__ == "__main__":
    hotel = Hotel()
