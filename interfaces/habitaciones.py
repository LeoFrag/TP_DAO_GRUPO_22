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
        # Configuración de estilos
        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 11))
        style.configure("TButton", font=("Helvetica", 11))
        style.configure("Heading.TLabel", font=("Helvetica", 16, "bold"))
        style.configure("TLabelframe.Label", font=("Helvetica", 12, "bold"))

        # Título
        ttk.Label(self.tab, text="Gestión de Habitaciones", style="Heading.TLabel", anchor="center").pack(pady=20, fill="x")

        # Marco principal
        main_frame = ttk.Frame(self.tab, padding=20)
        main_frame.pack(fill="both", expand=True)

        # Marco del formulario
        form_frame = ttk.LabelFrame(main_frame, text="Añadir Habitación", padding=15)
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Campos del formulario
        ttk.Label(form_frame, text="Número de Habitación").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.room_number = ttk.Entry(form_frame, width=30)
        self.room_number.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Tipo de Habitación").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.room_type = ttk.Combobox(form_frame, values=["Simple", "Doble", "Suite"], state="readonly", width=28)
        self.room_type.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Precio por Noche").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.room_price = ttk.Entry(form_frame, width=30)
        self.room_price.grid(row=2, column=1, padx=5, pady=5)

        add_button = ttk.Button(form_frame, text="Añadir Habitación", command=self.registrar_habitacion, width=28)
        add_button.grid(row=3, column=0, columnspan=2, pady=15)

        # Marco de filtro
        filter_frame = ttk.LabelFrame(main_frame, text="Filtrar Habitaciones", padding=15)
        filter_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ttk.Label(filter_frame, text="Fecha", anchor="center").grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.filter_date = Calendar(filter_frame, date_pattern='yyyy-mm-dd', width=28, height=28)
        self.filter_date.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        filter_frame.columnconfigure(0, weight=1)

        filter_button = ttk.Button(filter_frame, text="Filtrar Disponibles", command=self.filtrar_habitaciones_disponibles, width=28)
        filter_button.grid(row=2, column=0, pady=15)

        # Tabla de habitaciones
        table_frame = ttk.Frame(main_frame)
        table_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.room_table = ttk.Treeview(table_frame, columns=("Número", "Tipo", "Precio"), show="headings", height=10)
        self.room_table.heading("Número", text="Número de Habitación")
        self.room_table.heading("Tipo", text="Tipo")
        self.room_table.heading("Precio", text="Precio por noche")
        self.room_table.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.room_table.yview)
        scrollbar.pack(side="right", fill="y")
        self.room_table.configure(yscrollcommand=scrollbar.set)

        # Configurar el peso de las filas y columnas
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Cargar habitaciones al iniciar la vista
        self.cargar_habitaciones()

    def cargar_habitaciones(self):
        habitaciones = self.habitacionservice.obtener_habitaciones()
        for habitacion in habitaciones:
            self.room_table.insert("", "end", values=(habitacion[1], habitacion[2], habitacion[4]))

    def registrar_habitacion(self):
        try:
            self.habitacionservice.registrar_habitacion(
                self.room_number.get(),
                self.room_type.get(),
                self.room_price.get()
            )
            self.room_table.insert("", "end", values=(self.room_number.get(), self.room_type.get(), self.room_price.get()))
            messagebox.showinfo("Éxito", "Habitación registrada correctamente")
            self.limpiar_campos()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def filtrar_habitaciones_disponibles(self):
        try:
            habitaciones_disponibles = self.habitacionservice.obtener_habitaciones_disponibles(self.filter_date.get_date())
            self.room_table.delete(*self.room_table.get_children())
            for habitacion in habitaciones_disponibles:
                self.room_table.insert("", "end", values=(habitacion[0], habitacion[1], habitacion[2]))
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def limpiar_campos(self):
        self.room_number.delete(0, tk.END)
        self.room_type.set('')
        self.room_price.delete(0, tk.END)

