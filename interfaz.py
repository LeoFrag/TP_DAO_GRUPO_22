import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from classes import Hotel, Habitacion
from db.consultas import obtener_habitaciones, obtener_clientes

# Clase principal de la aplicación Tkinter
class HotelApp:
    def __init__(self, root, hotel):
        self.root = root
        self.hotel = hotel
        self.root.title("Sistema de Gestión de Hotel")
        self.root.geometry("600x400")

        # Crear pestañas
        self.create_tabs()

    def create_tabs(self):
        # Configuración de las pestañas
        self.tab_control = ttk.Notebook(self.root)
        ttk.Style().theme_use("clam")

        # Pestañas
        self.tab_habitaciones = ttk.Frame(self.tab_control)
        self.tab_clientes = ttk.Frame(self.tab_control)
        self.tab_reservas = ttk.Frame(self.tab_control)
        self.tab_facturas = ttk.Frame(self.tab_control)
        self.tab_reportes = ttk.Frame(self.tab_control)

        # Añadir pestañas al control de pestañas
        self.tab_control.add(self.tab_habitaciones, text="Habitaciones")
        self.tab_control.add(self.tab_clientes, text="Clientes")
        self.tab_control.add(self.tab_reservas, text="Reservas")
        self.tab_control.add(self.tab_facturas, text="Facturas")
        self.tab_control.add(self.tab_reportes, text="Reportes")
        
        self.tab_control.pack(expand=1, fill="both")

        # Configuración de cada pestaña
        self.setup_habitaciones_tab()
        self.setup_clientes_tab()
        self.setup_reservas_tab()
        self.setup_facturas_tab()
        self.setup_reportes_tab()

    def setup_habitaciones_tab(self):
        # Campos para registrar habitaciones con etiquetas de error
        ttk.Label(self.tab_habitaciones, text="Número de Habitación:").pack()
        self.numero_habitacion_entry = ttk.Entry(self.tab_habitaciones)
        self.numero_habitacion_entry.pack()

        ttk.Label(self.tab_habitaciones, text="Tipo:").pack()
        self.tipo_habitacion_entry = ttk.Entry(self.tab_habitaciones)
        self.tipo_habitacion_entry.pack()

        ttk.Label(self.tab_habitaciones, text="Precio por Noche:").pack()
        self.precio_habitacion_entry = ttk.Entry(self.tab_habitaciones)
        self.precio_habitacion_entry.pack()

        ttk.Button(
            self.tab_habitaciones,
            text="Registrar Habitación",
            command=lambda: self.hotel.registrar_habitacion(
                self.numero_habitacion_entry.get(),
                self.tipo_habitacion_entry.get(),
                self.precio_habitacion_entry.get()
            )
        ).pack()

        # Botón para ver habitaciones
        ttk.Button(self.tab_habitaciones, text="Ver Habitaciones", command=self.ver_habitaciones).pack()

    def ver_habitaciones(self):
            # Crear una ventana nueva
            ventana_habitaciones = tk.Toplevel(self.root)
            ventana_habitaciones.title("Habitaciones del Hotel")
            ventana_habitaciones.geometry("600x400")

            # Crear un estilo para el Treeview
            style = ttk.Style()
            style.theme_use("default")

            style.configure("mystyle.Treeview", 
                            font=('Helvetica', 10),  # Tamaño de fuente legible
                            rowheight=30,  # Altura de las filas
                            background="white",  # Fondo blanco
                            foreground="black",  # Texto en negro
                            fieldbackground="white",
                            highlightthickness=1, 
                            bd=1)  

            # Configurar el encabezado de la tabla
            style.configure("mystyle.Treeview.Heading", 
                            font=('Helvetica', 10, 'bold'),  # Fuente más grande y en negrita
                            background="#E2EAFC",  # Color de fondo del encabezado
                            foreground="black",
                            )  # Color de texto del encabezado

            # Aplicar el estilo a las líneas de la tabla
            style.map("mystyle.Treeview", 
                    background=[("selected", "#c1d3fe")],  # Color de selección
                    foreground=[("selected", "black")])

            # Crear el Treeview para mostrar la tabla
            tree = ttk.Treeview(ventana_habitaciones, 
                                columns=("Numero", "Tipo", "Precio", "Estado"), 
                                show="headings", 
                                style="mystyle.Treeview")

            # Agregar barras de desplazamiento
            vsb = ttk.Scrollbar(ventana_habitaciones, orient="vertical", command=tree.yview)
            vsb.pack(side="right", fill="y")
            tree.configure(yscrollcommand=vsb.set)

            # Configurar encabezados de columna
            tree.heading("Numero", text="Número")
            tree.heading("Tipo", text="Tipo")
            tree.heading("Precio", text="Precio por Noche")
            tree.heading("Estado", text="Estado")

            # Configurar el ancho de las columnas
            tree.column("Numero", width=100, anchor="center")
            tree.column("Tipo", width=150, anchor="center")
            tree.column("Precio", width=150, anchor="center")
            tree.column("Estado", width=120, anchor="center")


            habitaciones = obtener_habitaciones()

            # Insertar los datos de las habitaciones en el Treeview
            for habitacion in habitaciones:
                # Desempaquetamos la tupla para pasar los valores a las columnas
                numero, tipo, precio, estado = habitacion
                tree.insert("", "end", values=(numero, tipo, precio, estado))
            # Empacar el Treeview
            tree.pack(fill="both", expand=True)

    def setup_clientes_tab(self):
        
        ttk.Label(self.tab_clientes, text="Nombre:").pack()
        self.nombre_cliente_entry = ttk.Entry(self.tab_clientes)
        self.nombre_cliente_entry.pack()

        ttk.Label(self.tab_clientes, text="Apellido:").pack()
        self.apellido_cliente_entry = ttk.Entry(self.tab_clientes)
        self.apellido_cliente_entry.pack()

        ttk.Label(self.tab_clientes, text="Telefono:").pack()
        self.telefono_cliente_entry = ttk.Entry(self.tab_clientes)
        self.telefono_cliente_entry.pack()

        ttk.Label(self.tab_clientes, text="Email:").pack()
        self.email_cliente_entry = ttk.Entry(self.tab_clientes)
        self.email_cliente_entry.pack()

        ttk.Label(self.tab_clientes, text="Direccion:").pack()
        self.direccion_cliente_entry = ttk.Entry(self.tab_clientes)
        self.direccion_cliente_entry.pack()

        ttk.Button(
                    self.tab_clientes,
                    text="Registrar Cliente",
                    command=lambda: self.hotel.registrar_cliente(
                        self.nombre_cliente_entry.get(),
                        self.apellido_cliente_entry.get(),
                        self.telefono_cliente_entry.get(),
                        self.email_cliente_entry.get(),
                        self.direccion_cliente_entry.get()
                    )
                ).pack()

        # Botón para ver habitaciones
        ttk.Button(self.tab_clientes, text="Ver Clientes", command=self.ver_clientes).pack()

    def ver_clientes(self):
        # Crear una ventana nueva
        ventana_clientes = tk.Toplevel(self.root)
        ventana_clientes.title("Clientes del Hotel")
        ventana_clientes.geometry("600x400")

        # Crear un estilo para el Treeview
        style = ttk.Style()
        style.theme_use("default")

        style.configure("mystyle.Treeview", 
                        font=('Helvetica', 10),  # Tamaño de fuente legible
                        rowheight=30,  # Altura de las filas
                        background="white",  # Fondo blanco
                        foreground="black",  # Texto en negro
                        fieldbackground="white",
                        highlightthickness=1, 
                        bd=1)  

        # Configurar el encabezado de la tabla
        style.configure("mystyle.Treeview.Heading", 
                        font=('Helvetica', 10, 'bold'),  # Fuente más grande y en negrita
                        background="#E2EAFC",  # Color de fondo del encabezado
                        foreground="black",
                        )  # Color de texto del encabezado

        # Aplicar el estilo a las líneas de la tabla
        style.map("mystyle.Treeview", 
                background=[("selected", "#c1d3fe")],  # Color de selección
                foreground=[("selected", "black")])

        # Crear el Treeview para mostrar la tabla
        tree = ttk.Treeview(ventana_clientes, 
                            columns=("ID", "Nombre", "Apellido", "Telefono", "Email", "Direccion"), 
                            show="headings", 
                            style="mystyle.Treeview")

        # Agregar barras de desplazamiento
        vsb = ttk.Scrollbar(ventana_clientes, orient="vertical", command=tree.yview)
        vsb.pack(side="right", fill="y")
        tree.configure(yscrollcommand=vsb.set)

        # Configurar encabezados de columna
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Apellido", text="Apellido")
        tree.heading("Telefono", text="Telefono")
        tree.heading("Email", text="Email")
        tree.heading("Direccion", text="Direccion")

        # Configurar el ancho de las columnas
        tree.column("ID", width=100, anchor="center")
        tree.column("Nombre", width=150, anchor="center")
        tree.column("Apellido", width=150, anchor="center")
        tree.column("Telefono", width=120, anchor="center")
        tree.column("Email", width=120, anchor="center")
        tree.column("Direccion", width=120, anchor="center")

        clientes = obtener_clientes()

        # Insertar los datos de las clientes en el Treeview
        for cliente in clientes:
            # Desempaquetamos la tupla para pasar los valores a las columnas
            id_cliente, nombre, apellido, telefono, email, direccion = cliente
            tree.insert("", "end", values=(id_cliente, nombre, apellido, telefono, email, direccion))

        # Empacar el Treeview
        tree.pack(fill="both", expand=True)

    def setup_reservas_tab(self):
        ttk.Label(self.tab_reservas, text="ID Cliente:").pack()
        self.id_cliente_reserva_entry = ttk.Entry(self.tab_reservas)
        self.id_cliente_reserva_entry.pack()

        ttk.Label(self.tab_reservas, text="Número de Habitación:").pack()
        self.numero_habitacion_reserva_entry = ttk.Entry(self.tab_reservas)
        self.numero_habitacion_reserva_entry.pack()

        ttk.Label(self.tab_reservas, text="Fecha Entrada (YYYY-MM-DD):").pack()
        self.fecha_entrada_reserva_entry = ttk.Entry(self.tab_reservas)
        self.fecha_entrada_reserva_entry.pack()

        ttk.Label(self.tab_reservas, text="Fecha Salida (YYYY-MM-DD):").pack()
        self.fecha_salida_reserva_entry = ttk.Entry(self.tab_reservas)
        self.fecha_salida_reserva_entry.pack()

        ttk.Button(self.tab_reservas, text="Registrar Reserva", command=Hotel.registrar_reserva).pack()


    def setup_facturas_tab(self):
        ttk.Label(self.tab_facturas, text="ID Reserva:").pack()
        self.id_reserva_factura_entry = ttk.Entry(self.tab_facturas)
        self.id_reserva_factura_entry.pack()

        ttk.Button(self.tab_facturas, text="Generar Factura", command=Hotel.generar_factura).pack()

    def setup_reportes_tab(self):
        ttk.Button(self.tab_reportes, text="Generar Reporte de Ocupación", command=Hotel.reporte_ocupacion_promedio).pack()

