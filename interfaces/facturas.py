# habitaciones.py
import tkinter as tk
from tkinter import ttk

class FacturasTab:
    def __init__(self, parent_frame, gestorBD):
        self.tab = parent_frame
        self.gestorBD = gestorBD
        self.setup_ui()

    def setup_ui(self):

        tk.Label(self.tab, text="Generar Factura", font=("Arial", 16, "bold"), fg="#333", bg="#f5f5f5").pack(pady=10)
        ttk.Label(self.tab, text="ID Reserva:").pack(pady=10)
        self.id_reserva_factura_entry = ttk.Entry(self.tab)
        self.id_reserva_factura_entry.pack(pady=5)
        ttk.Button(self.tab, text="Generar Factura").pack(pady=10)