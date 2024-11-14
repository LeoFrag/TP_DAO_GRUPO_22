
# habitaciones.py
import tkinter as tk
from tkinter import ttk, messagebox
from services.clientes import ClienteService

class ClientesTab:
    def __init__(self, parent_frame, gestorBD):
        self.tab = parent_frame
        self.gestorBD = gestorBD
        self.clienteService = ClienteService(self.gestorBD)
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.tab, text="Gestión de Clientes", font=("Arial", 16, "bold"), fg="#333").pack(pady=10)
        form_frame = ttk.Frame(self.tab, padding=10)
        form_frame.pack(fill="x")
        ttk.Label(form_frame, text="Nombre").grid(row=0, column=0, padx=5, pady=5)
        self.client_name = ttk.Entry(form_frame)
        self.client_name.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Apellido").grid(row=1, column=0, padx=5, pady=5)
        self.client_lastname = ttk.Entry(form_frame)
        self.client_lastname.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Teléfono").grid(row=2, column=0, padx=5, pady=5)
        self.client_phone = ttk.Entry(form_frame)
        self.client_phone.grid(row=2, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Direccion").grid(row=3, column=0, padx=5, pady=5)
        self.client_direccion = ttk.Entry(form_frame)
        self.client_direccion.grid(row=3, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Email").grid(row=4, column=0, padx=5, pady=5)
        self.client_email = ttk.Entry(form_frame)
        self.client_email.grid(row=4, column=1, padx=5, pady=5)

        add_button = ttk.Button(
            form_frame,
            text="Añadir Cliente",
            command=lambda: self.registrar_cliente()
        )
        add_button.grid(row=5, column=0, columnspan=2, pady=10)
        self.client_table = ttk.Treeview(self.tab, columns=("Nombre", "Apellido", "Teléfono", "Email", "Direccion"), show="headings")
        self.client_table.heading("Nombre", text="Nombre")
        self.client_table.heading("Apellido", text="Apellido")
        self.client_table.heading("Teléfono", text="Teléfono")
        self.client_table.heading("Email", text="Email")
        self.client_table.heading("Direccion", text="Direccion")
        self.client_table.pack(fill="both", expand=True, pady=10)
            # Cargar clientes al iniciar la vista
        self.cargar_clientes()

    def cargar_clientes(self):
        clientes = self.clienteService.obtener_clientes()  # Supongo que este método devuelve una lista de clientes
        for cliente in clientes:
            self.client_table.insert("", "end", values=(cliente[1], cliente[2], cliente[4], cliente[5], cliente[3]))

    def registrar_cliente(self):
        try:
            # Llama al servicio para registrar la habitación
            self.clienteService.registrar_cliente(
                    self.client_name.get(),
                    self.client_lastname.get(),
                    self.client_phone.get(),
                    self.client_direccion.get(),
                    self.client_email.get()
            )

            # Si se registra correctamente, actualiza la tabla
            self.client_table.insert("", "end", values=(self.client_name.get(),
                    self.client_lastname.get(),
                    self.client_phone.get(),
                    self.client_direccion.get(),
                    self.client_email.get()))

        except ValueError as e:
            # Muestra un cuadro de diálogo emergente con el mensaje de error
            messagebox.showerror("Error", str(e))