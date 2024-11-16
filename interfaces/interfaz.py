import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from interfaces.habitaciones import HabitacionesTab
from interfaces.clientes import ClientesTab
from interfaces.reservas import ReservasTab
from interfaces.facturas import FacturasTab
from interfaces.reportes import ReportesTab
from interfaces.empleados import EmpleadosTab


class HotelApp(tk.Tk):
    def __init__(self, gestorBD):
        super().__init__()
        self.title("Gestión de Hotel")
        self.geometry("1400x700")
        self.configure(bg="#f5f5f5")  # Fondo principal
        self.gestorBD = gestorBD  # Obtener la instancia de la base de datos

        # Establecer el tamaño mínimo de la ventana
        self.minsize(1000, 700)  # Aquí defines el tamaño mínimo que quieres

        # Estilos de color para ttk
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#f5f5f5")
        self.style.configure("TLabel", background="#f5f5f5", foreground="#333")
        self.style.configure("TButton", background="#4CAF50", foreground="white", font=("Arial", 10, "bold"))
        self.style.map("TButton", background=[("active", "#45a049")])

        # Sidebar
        self.sidebar = tk.Frame(self, width=200, bg="#333", padx=10, pady=10)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar_title = tk.Label(self.sidebar, text="Gestión de Hotel", font=("Arial", 18), fg="white", bg="#333")
        self.sidebar_title.pack(pady=20)

        # Botones de Tabs en Sidebar
        self.tab_buttons = {
            "habitaciones": tk.Button(self.sidebar, text="Habitaciones", bg="#4CAF50", fg="white", command=lambda: self.show_tab("habitaciones")),
            "clientes": tk.Button(self.sidebar, text="Clientes", bg="#4CAF50", fg="white", command=lambda: self.show_tab("clientes")),
            "reservas": tk.Button(self.sidebar, text="Reservas", bg="#4CAF50", fg="white", command=lambda: self.show_tab("reservas")),
            "empleados": tk.Button(self.sidebar, text="Empleados", bg="#4CAF50", fg="white", command=lambda: self.show_tab("empleados")),
            "facturas": tk.Button(self.sidebar, text="Facturas", bg="#4CAF50", fg="white", command=lambda: self.show_tab("facturas")),
            "informes": tk.Button(self.sidebar, text="Informes", bg="#4CAF50", fg="white", command=lambda: self.show_tab("informes")),
        }

        for button in self.tab_buttons.values():
            button.pack(fill="x", pady=5)

        # Main Content Area
        self.main_content = tk.Frame(self, bg="#f5f5f5")
        self.main_content.pack(side="right", expand=True, fill="both")

        # Tabs as Frames
        self.tabs = {}
        for tab in ["habitaciones", "clientes", "reservas","facturas", "informes", "empleados"]:
            frame = ttk.Frame(self.main_content)
            frame.place(relwidth=1, relheight=1)
            self.tabs[tab] = frame

        # Initialize tabs with content
        self.setup_habitaciones_tab()
        self.setup_clientes_tab()
        self.setup_reservas_tab()
        self.setup_empleados_tab()
        self.setup_facturas_tab()
        self.setup_reportes_tab()

        # Show initial tab
        self.show_tab("habitaciones")

    def show_tab(self, tab_name):
        for tab, frame in self.tabs.items():
            frame.place_forget()
        self.tabs[tab_name].place(relwidth=1, relheight=1)

    def setup_habitaciones_tab(self):
        habitaciones = HabitacionesTab(self.tabs["habitaciones"], self.gestorBD)

    def setup_clientes_tab(self):
        clientes = ClientesTab(self.tabs["clientes"], self.gestorBD)

    def setup_empleados_tab(self):
        empleados = EmpleadosTab(self.tabs["empleados"], self.gestorBD)

    def setup_reservas_tab(self):
        reservas = ReservasTab(self.tabs["reservas"], self.tabs["facturas"], self.gestorBD)

    def setup_facturas_tab(self):
        facturas = FacturasTab(self.tabs["facturas"], self.gestorBD)

    def setup_reportes_tab(self):
        reportes = ReportesTab(self.tabs["informes"], self.gestorBD)

