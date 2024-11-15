import tkinter as tk
from tkinter import ttk
from services.facturas import FacturaService
from services.clientes import ClienteService
class FacturasTab:
    def __init__(self, parent_frame, gestorBD):
        self.tab = parent_frame
        self.gestorBD = gestorBD
        self.facturasService = FacturaService(gestorBD)
        self.clientesService = ClienteService(gestorBD)
        self.setup_ui()

    def setup_ui(self):
        # Título
        tk.Label(self.tab, text="Facturas generadas", font=("Arial", 16, "bold"), fg="#333", bg="#f5f5f5").pack(pady=10)
        
        # Crear el Treeview con las columnas
        self.tree = ttk.Treeview(self.tab, columns=("ID", "Cliente", "Reserva", "Fecha de emisión", "Total"), show="headings")
        
        # Configurar encabezados de columna
        self.tree.heading("ID", text="ID")
        self.tree.heading("Cliente", text="Cliente")
        self.tree.heading("Reserva", text="Reserva")
        self.tree.heading("Fecha de emisión", text="Fecha de emisión")
        self.tree.heading("Total", text="Total")
        
        # Configurar el tamaño de las columnas
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Cliente", width=150, anchor="center")
        self.tree.column("Reserva", width=100, anchor="center")
        self.tree.column("Fecha de emisión", width=120, anchor="center")
        self.tree.column("Total", width=80, anchor="center")

        # Empaquetar el Treeview en el frame
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        self.cargar_facturas()

    def cargar_facturas(self):
        facturas = self.facturasService.obtener_facturas_detalladas()
        for factura in facturas:
            nombre_completo = f"{factura[1]} {factura[2]}"  # nombre y apellido concatenados
            self.tree.insert(
                "", 
                "end", 
                values=(
                    factura[0],  # nro_reserva
                    nombre_completo, 
                    factura[3],  # numero_habitacion
                    factura[4],  # fecha_emision
                    factura[5]   # total
                )
            )