# habitaciones.py
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from services.reservas import ReservaService


class ReservasTab:
    def __init__(self, parent_frame, gestorBD):
        self.tab = parent_frame
        self.gestorBD = gestorBD
        self.reservasService = ReservaService(gestorBD)
        self.setup_ui()

    def setup_ui(self):

        tk.Label(self.tab, text="Gestión de Reservas", font=("Arial", 16, "bold"), fg="#333").pack(pady=10)
        
        form_frame = ttk.Frame(self.tab, padding=10)
        form_frame.pack(fill="x")

        # Fechas de entrada y salida (Calendarios en lugar de Entry)
        ttk.Label(form_frame, text="Fecha de Entrada").grid(row=0, column=0, padx=5, pady=5)
        self.entry_date = Calendar(form_frame, date_pattern='yyyy-mm-dd')  # Calendario para la fecha de entrada
        self.entry_date.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Fecha de Salida").grid(row=1, column=0, padx=5, pady=5)
        self.exit_date = Calendar(form_frame, date_pattern='yyyy-mm-dd')  # Calendario para la fecha de salida
        self.exit_date.grid(row=1, column=1, padx=5, pady=5)

        # Botón para buscar habitaciones
        add_button = ttk.Button(form_frame, text="Buscar Habitaciones Disponibles", command=self.buscar_habitaciones)
        add_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Tabla para mostrar habitaciones disponibles
        self.reservation_table = ttk.Treeview(self.tab, columns=("Número Habitación", "Tipo"), show="headings")
        self.reservation_table.heading("Número Habitación", text="Número Habitación")
        self.reservation_table.heading("Tipo", text="Tipo")
        self.reservation_table.pack(fill="both", expand=True, pady=10)

        # Campos adicionales (ocultos inicialmente)
        self.cliente_combobox = ttk.Combobox(self.tab, state="readonly")
        self.cliente_combobox.pack(pady=5)
        
        self.habitacion_combobox = ttk.Combobox(self.tab, state="readonly")
        self.habitacion_combobox.pack(pady=5)
        
        ttk.Label(self.tab, text="Cantidad de Personas").pack(pady=5)
        self.num_people = ttk.Entry(self.tab)
        self.num_people.pack(pady=5)
        
        # Inicialmente los campos adicionales están ocultos
        self.cliente_combobox.pack_forget()
        self.habitacion_combobox.pack_forget()
        self.num_people.pack_forget()

    def buscar_habitaciones(self):
            # Obtener las fechas de entrada y salida seleccionadas
            fecha_inicio = self.entry_date.get_date()
            fecha_fin = self.exit_date.get_date()

            # Llamar al método de reservas_service para obtener habitaciones disponibles
            habitaciones_disponibles = self.reservasService.buscar_habitaciones_disponibles(fecha_inicio, fecha_fin)

            # Limpiar la tabla
            for item in self.reservation_table.get_children():
                self.reservation_table.delete(item)

            if habitaciones_disponibles:
                # Mostrar habitaciones en la tabla
                for habitacion in habitaciones_disponibles:
                    self.reservation_table.insert("", "end", values=(habitacion[0], habitacion[1]))
                
                # Mostrar campos adicionales
                self.cliente_combobox.pack(pady=5)
                self.habitacion_combobox.pack(pady=5)
                self.num_people.pack(pady=5)

                # Llenar el ComboBox de clientes
                clientes = self.gestorBD.obtener_clientes()  # Método para obtener todos los clientes desde la base de datos
                self.cliente_combobox['values'] = [cliente['nombre'] for cliente in clientes]

                # Llenar el ComboBox de habitaciones disponibles
                self.habitacion_combobox['values'] = [habitacion[0] for habitacion in habitaciones_disponibles]

            else:
                tk.messagebox.showinfo("Sin habitaciones disponibles", "No se encontraron habitaciones disponibles para las fechas seleccionadas.")
                # Ocultar campos si no hay habitaciones disponibles
                self.cliente_combobox.pack_forget()
                self.habitacion_combobox.pack_forget()
                self.num_people.pack_forget()