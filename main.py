import datetime
import tkinter as tk
from interfaces.interfaz import HotelApp
from db.gestorBD import GestorBD

def main():
 
    gestorBD = GestorBD() 
    gestorBD.crear_tablas()
    interfazHotel = HotelApp(gestorBD)
    interfazHotel.mainloop()

# Ejemplo de uso del sistema de gestión de hotel
if __name__ == "__main__":
    main()

"""
A INSTALAR

pip install tkinter
pip install tkcalendar
pip install datetime
pip install pillow
pip install reportlab
pip install matplotlib
pip install ttkthemes

"""