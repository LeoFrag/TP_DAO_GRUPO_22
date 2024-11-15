# habitaciones.py
import tkinter as tk
from tkinter import ttk, messagebox
from services.habitaciones import HabitacionService
from tkcalendar import Calendar


class HabitacionesTab:
    def __init__(self, parent_frame, gestorBD):
        self.tab = parent_frame
        self.gestorBD = gestorBD
        self.habitacionservice = HabitacionService(self.gestorBD)
        self.setup_ui()


    def setup_ui(self):
        
        tk.Label(self.tab, text="Gestión de Habitaciones", font=("Arial", 16, "bold"), fg="#333").pack(pady=10)

        form_frame = ttk.Frame(self.tab, padding=10)
        form_frame.pack(fill="x")

        ttk.Label(form_frame, text="Número de Habitación").grid(row=0, column=0, padx=5, pady=5)
        self.room_number = ttk.Entry(form_frame)
        self.room_number.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Tipo de Habitación").grid(row=1, column=0, padx=5, pady=5)
        self.room_type = ttk.Combobox(form_frame, values=["Simple", "Doble", "Suite"], state="readonly")
        self.room_type.grid(row=1, column=1, padx=5, pady=5)


        ttk.Label(form_frame, text="Precio por Noche").grid(row=2, column=0, padx=5, pady=5)
        self.room_price = ttk.Entry(form_frame)
        self.room_price.grid(row=2, column=1, padx=5, pady=5)

        add_button = ttk.Button(
            form_frame,
            text="Añadir Habitación",
            command=lambda: self.registrar_habitacion())

        add_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Crear extra_frame para el filtro de habitaciones por fecha
        extra_frame = ttk.Frame(form_frame, padding=10)
        extra_frame.grid(row=4, column=0, columnspan=2, pady=10)

        # Etiqueta y calendario para filtrar por fecha
        ttk.Label(extra_frame, text="Filtrar Habitaciones por Fecha").grid(row=0, column=0, padx=5, pady=5)
        self.filter_date = Calendar(extra_frame, date_pattern='yyyy-mm-dd')  # Calendario para seleccionar la fecha
        self.filter_date.grid(row=0, column=1, padx=5, pady=5)

        # Botón para filtrar habitaciones disponibles
        filter_button = ttk.Button(extra_frame, text="Filtrar", command=self.filtrar_habitaciones_disponibles)
        filter_button.grid(row=0, column=2, padx=5, pady=5)

        self.room_table = ttk.Treeview(self.tab, columns=("Número", "Tipo", "Precio"), show="headings")
        self.room_table.heading("Número", text="Número de Habitación")
        self.room_table.heading("Tipo", text="Tipo")
        self.room_table.heading("Precio", text="Precio por noche")
        self.room_table.pack(fill="both", expand=True, pady=10)

        # Cargar clientes al iniciar la vista
        self.cargar_habitaciones()

    def cargar_habitaciones(self):
        habitaciones = self.habitacionservice.obtener_habitaciones()  # Supongo que este método devuelve una lista de clientes
        for habitacion in habitaciones:
            self.room_table.insert("", "end", values=(habitacion[1], habitacion[2], habitacion[4]))

    def registrar_habitacion(self):
        try:
            # Llama al servicio para registrar la habitación
            self.habitacionservice.registrar_habitacion(
                self.room_number.get(),
                self.room_type.get(),
                self.room_price.get()
            )
            # Si se registra correctamente, actualiza la tabla
            self.room_table.insert("", "end", values=(self.room_number.get(), self.room_type.get(), self.room_price.get()))

        except ValueError as e:
            # Muestra un cuadro de diálogo emergente con el mensaje de error
            messagebox.showerror("Error", str(e))

    def filtrar_habitaciones_disponibles(self):
        try:
            # Llama al servicio para obtener las habitaciones disponibles
            habitaciones_disponibles = self.habitacionservice.obtener_habitaciones_disponibles(self.filter_date.get_date())
            self.room_table.delete(*self.room_table.get_children())
            for habitacion in habitaciones_disponibles:
                print(habitacion)
                self.room_table.insert("", "end", values=(habitacion[0], habitacion[1], habitacion[2]))

        except ValueError as e:
            # Muestra un cuadro de diálogo emergente con el mensaje de error
            messagebox.showerror("Error", str(e))