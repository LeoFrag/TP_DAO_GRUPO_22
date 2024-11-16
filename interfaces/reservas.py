import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from services.reservas import ReservaService
from datetime import datetime


class ReservasTab:
    def __init__(self, parent_frame, facturas_frame, gestorBD):
        self.tab = parent_frame
        self.tab_frame = facturas_frame
        self.gestorBD = gestorBD
        self.reservasService = ReservaService(gestorBD)
        self.setup_ui()

    def setup_ui(self):
        # Título
        tk.Label(self.tab, text="Gestión de Reservas", font=("Arial", 16, "bold"), fg="#333").pack(pady=10)

        # Formulario para fechas
        form_frame = ttk.Frame(self.tab, padding=10)
        form_frame.pack(fill="x")

        ttk.Label(form_frame, text="Fecha de Entrada").grid(row=0, column=0, padx=5, pady=5)
        self.entry_date = Calendar(form_frame, date_pattern='yyyy-mm-dd')
        self.entry_date.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Fecha de Salida").grid(row=1, column=0, padx=5, pady=5)
        self.exit_date = Calendar(form_frame, date_pattern='yyyy-mm-dd')
        self.exit_date.grid(row=1, column=1, padx=5, pady=5)

        # Botones para buscar y finalizar estadías
        buttons_frame = ttk.Frame(form_frame)
        buttons_frame.grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Button(
            buttons_frame,
            text="Buscar Habitaciones Disponibles",
            command=self.buscar_habitaciones
        ).pack(side="left", padx=5)

        ttk.Button(
            buttons_frame,
            text="Finalizar Estadía",
            command=self.finalizar_estadia
        ).pack(side="left", padx=5)

        # Tabla de reservas
        table_frame = ttk.Frame(self.tab)
        table_frame.pack(fill="both", expand=True, pady=10)

        scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical")
        self.reservation_table = ttk.Treeview(
            table_frame,
            columns=("ID Reserva", "Cliente", "Habitación", "Fecha Entrada", "Fecha Salida"),
            show="headings",
            yscrollcommand=scrollbar_y.set
        )

        # Configuración de las columnas
        self.reservation_table.heading("ID Reserva", text="ID Reserva")
        self.reservation_table.heading("Cliente", text="Cliente")
        self.reservation_table.heading("Habitación", text="Habitación")
        self.reservation_table.heading("Fecha Entrada", text="Fecha Entrada")
        self.reservation_table.heading("Fecha Salida", text="Fecha Salida")

        self.reservation_table.pack(side="left", fill="both", expand=True)
        scrollbar_y.config(command=self.reservation_table.yview)
        scrollbar_y.pack(side="right", fill="y")

        # Campos adicionales (Formulario lateral)
        self.extra_frame = ttk.Frame(form_frame)
        self.extra_frame.grid(row=0, column=2, rowspan=3, padx=20)
        self.extra_frame.grid_forget()  # Inicialmente oculto

        ttk.Label(self.extra_frame, text="Cliente").grid(row=0, column=0, pady=5)
        self.cliente_combobox = ttk.Combobox(self.extra_frame, state="readonly")
        self.cliente_combobox.grid(row=1, column=0, pady=5)

        ttk.Label(self.extra_frame, text="Habitación").grid(row=2, column=0, pady=5)
        self.habitacion_combobox = ttk.Combobox(self.extra_frame, state="readonly")
        self.habitacion_combobox.grid(row=3, column=0, pady=5)

        ttk.Label(self.extra_frame, text="Cantidad de Personas").grid(row=4, column=0, pady=5)
        self.num_people = ttk.Entry(self.extra_frame)
        self.num_people.grid(row=5, column=0, pady=5)

        ttk.Button(
            self.extra_frame,
            text="Registrar Reserva",
            command=self.registrar_reserva
        ).grid(row=6, column=0, pady=10)

        # Cargar reservas iniciales
        self.cargar_reservas()

    def cargar_reservas(self):
        reservas = self.reservasService.obtener_reservas_detalladas()
        for reserva in reservas:
            id_reserva, nombre, apellido, habitacion, fecha_entrada, fecha_salida = reserva
            nombre_completo = f"{nombre} {apellido}"
            self.reservation_table.insert("", "end", values=(id_reserva, nombre_completo, habitacion, fecha_entrada, fecha_salida))

    def buscar_habitaciones(self):
        self.fecha_inicio = datetime.strptime(self.entry_date.get_date(), "%Y-%m-%d").date()
        self.fecha_fin = datetime.strptime(self.exit_date.get_date(), "%Y-%m-%d").date()

        if not self.reservasService.validar_fechas(self.fecha_inicio, self.fecha_fin):
            messagebox.showerror("Error", "La fecha de salida debe ser posterior a la de entrada.")
            return

        habitaciones_disponibles = self.reservasService.buscar_habitaciones_disponibles(self.fecha_inicio, self.fecha_fin)
        print(habitaciones_disponibles)
        if habitaciones_disponibles:
            print(habitaciones_disponibles)

            self.extra_frame.grid(row=0, column=2, rowspan=3, padx=20)
            clientes = self.gestorBD.obtener_clientes()
            self.clientes_dict = {f"{c[1]} {c[2]}": c[0] for c in clientes}
            self.cliente_combobox["values"] = list(self.clientes_dict.keys())
            self.habitacion_combobox["values"] = [h[0] for h in habitaciones_disponibles]
        else:
            messagebox.showinfo("Sin disponibilidad", "No hay habitaciones disponibles para estas fechas.")
            self.extra_frame.grid_forget()

    def registrar_reserva(self):
        try:
            nombre_cliente = self.cliente_combobox.get()
            cliente_id = self.clientes_dict[nombre_cliente]
            habitacion = self.habitacion_combobox.get()
            num_personas = self.num_people.get()

            id_reserva = self.gestorBD.obtener_proximo_id_reserva()
            self.reservasService.registrar_reserva(id_reserva, cliente_id, habitacion, self.fecha_inicio, self.fecha_fin, num_personas)

            self.reservation_table.insert("", "end", values=(id_reserva, nombre_cliente, habitacion, self.fecha_inicio, self.fecha_fin))
            messagebox.showinfo("Reserva Registrada", "La reserva se ha registrado exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def finalizar_estadia(self):
        selected_item = self.reservation_table.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Selecciona una reserva para finalizar la estadía.")
            return

        reserva_data = self.reservation_table.item(selected_item)["values"]
        id_reserva = reserva_data[0]
        habitacion = reserva_data[2]

        if messagebox.askyesno("Confirmar", "¿Finalizar esta estadía?"):
            dias = (datetime.strptime(reserva_data[4], "%Y-%m-%d") - datetime.strptime(reserva_data[3], "%Y-%m-%d")).days
            self.reservasService.finalizar_estadia(id_reserva, habitacion, dias)
            self.tab_frame.event_generate("<<FacturaGenerada>>")
            self.reservation_table.delete(selected_item)
            messagebox.showinfo("Éxito", "Estadía finalizada correctamente.")
