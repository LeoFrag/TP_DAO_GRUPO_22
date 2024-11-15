# habitaciones.py
import tkinter as tk
from tkinter import ttk, messagebox
from services.empleados import EmpleadoService
from services.habitaciones import HabitacionService  # Servicio para gestionar habitaciones
from tkcalendar import Calendar  # Asegúrate de instalar la librería tkcalendar


class EmpleadosTab:
    def __init__(self, parent_frame, gestorBD):
        self.tab = parent_frame
        self.gestorBD = gestorBD
        self.empleadoService = EmpleadoService(self.gestorBD)
        self.habitacionService = HabitacionService(self.gestorBD)  # Servicio para manejar habitaciones
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.tab, text="Gestión de Empleados", font=("Arial", 16, "bold"), fg="#333").pack(pady=10)
        
        # Tabla de empleados
        self.empleado_table = ttk.Treeview(self.tab, columns=("ID", "Nombre", "Apellido", "Cargo", "Sueldo"), show="headings")
        self.empleado_table.heading("ID", text="ID")
        self.empleado_table.heading("Nombre", text="Nombre")
        self.empleado_table.heading("Apellido", text="Apellido")
        self.empleado_table.heading("Cargo", text="Cargo")
        self.empleado_table.heading("Sueldo", text="Sueldo")
        self.empleado_table.pack(fill="both", expand=True, pady=10)

        # Formulario de asignación (Frame principal)
        self.asignacion_frame = ttk.Frame(self.tab, padding=10)
        self.asignacion_frame.pack(fill="both", expand=True, pady=10)

        # Sub-frame izquierdo (Formulario y calendario)
        left_frame = ttk.Frame(self.asignacion_frame)
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(left_frame, text="Empleado (Limpieza):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.empleado_combobox = ttk.Combobox(left_frame, state="readonly")
        self.empleado_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(left_frame, text="Fecha:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.calendario = Calendar(left_frame, selectmode="day", date_pattern="yyyy-mm-dd")
        self.calendario.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.buscar_habitaciones_btn = ttk.Button(left_frame, text="Buscar Habitaciones Disponibles", command=self.buscar_habitaciones)
        self.buscar_habitaciones_btn.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

        # Sub-frame derecho (Habitaciones y botón de asignación)
        right_frame = ttk.Frame(self.asignacion_frame)
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ttk.Label(right_frame, text="Habitaciones Disponibles:").pack(anchor="w", pady=(0, 5))
        self.habitacion_table = ttk.Treeview(right_frame, columns=("Número", "Tipo"), show="headings", height=10)
        self.habitacion_table.heading("Número", text="Número")
        self.habitacion_table.heading("Tipo", text="Tipo")
        self.habitacion_table.pack(fill="both", expand=True, pady=5)

        self.asignar_btn = ttk.Button(right_frame, text="Asignar Limpieza", command=self.asignar_limpieza)
        self.asignar_btn.pack(pady=10, fill="x")

        # Ajuste de proporciones
        self.asignacion_frame.grid_columnconfigure(0, weight=1)
        self.asignacion_frame.grid_columnconfigure(1, weight=1)
        left_frame.grid_columnconfigure(1, weight=1)

        # Cargar empleados al iniciar la vista
        self.cargar_empleados()

    def cargar_empleados(self):
        empleados = self.empleadoService.obtener_empleados()
        for empleado in empleados:
            self.empleado_table.insert("", "end", values=(empleado[0], empleado[1], empleado[2], empleado[3], empleado[4]))
        
        # Filtrar empleados con cargo de "Limpieza" para el combobox
        empleados_limpieza = [f"{emp[0]} - {emp[2]}, {emp[1]}" for emp in empleados if emp[3].lower() == "limpieza"]
        self.empleado_combobox["values"] = empleados_limpieza

    def buscar_habitaciones(self):
        fecha = self.calendario.get_date()
        habitaciones_disponibles = self.habitacionService.obtener_habitaciones_disponibles(fecha)
        
        # Limpiar la tabla de habitaciones antes de cargar nuevas
        for item in self.habitacion_table.get_children():
            self.habitacion_table.delete(item)

        for habitacion in habitaciones_disponibles:
            self.habitacion_table.insert("", "end", values=(habitacion[0], habitacion[1]))

    def asignar_limpieza(self):
        empleado_seleccionado = self.empleado_combobox.get()
        id_empleado_seleccionado = empleado_seleccionado.split("-")[0].strip()
        habitacion_seleccionada = self.habitacion_table.focus()
        numero_habitacion_seleccionada = self.habitacion_table.item(habitacion_seleccionada)["values"][0]
        if not empleado_seleccionado:
            messagebox.showerror("Error", "Debe seleccionar un empleado de limpieza.")
            return

        if not habitacion_seleccionada:
            messagebox.showerror("Error", "Debe seleccionar una habitación.")
            return

        fecha = self.calendario.get_date()

        # Llamar al servicio y recibir estado y mensaje
        success, message = self.habitacionService.asignar_limpieza(numero_habitacion_seleccionada, id_empleado_seleccionado, fecha)
        
        if success:
            messagebox.showinfo("Éxito", message)
            self.buscar_habitaciones()  # Actualizar habitaciones disponibles
        else:
            messagebox.showerror("Error", message)