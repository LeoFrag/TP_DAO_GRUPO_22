# habitaciones.py
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from services.reservas import ReservaService
from datetime import datetime, date

class ReservasTab:
    def __init__(self, parent_frame, facturas_frame, gestorBD):
        self.tab = parent_frame
        self.tab_frame = facturas_frame
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
        self.reservation_table = ttk.Treeview(self.tab, columns=("ID Reserva", "Cliente", "Habitacion", "Fecha Entrada", "Fecha Salida"), show="headings")
        self.reservation_table.heading("ID Reserva", text="ID Reserva")
        self.reservation_table.heading("Cliente", text="Cliente")
        self.reservation_table.heading("Habitacion", text="Habitacion")
        self.reservation_table.heading("Fecha Entrada", text="Fecha Entrada")
        self.reservation_table.heading("Fecha Salida", text="Fecha Salida")
        self.reservation_table.pack(fill="both", expand=True, pady=10)

        self.finalizar_button = ttk.Button(form_frame, text="Finalizar Estadía", command=self.finalizar_estadia)
        self.finalizar_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Campos adicionales que aparecerán al costado derecho
        self.extra_frame = ttk.Frame(form_frame)
        self.extra_frame.grid(row=0, column=2, rowspan=3, padx=20)  # Ajustar el padding para moverlo más a la derecha

        # Campos que estarán inicialmente ocultos
        ttk.Label(self.extra_frame, text="Cliente").grid(row=0, column=0, pady=5)
        self.cliente_combobox = ttk.Combobox(self.extra_frame, state="readonly")
        self.cliente_combobox.grid(row=1, column=0, pady=5)

        ttk.Label(self.extra_frame, text="Habitación").grid(row=2, column=0, pady=5)
        self.habitacion_combobox = ttk.Combobox(self.extra_frame, state="readonly")
        self.habitacion_combobox.grid(row=3, column=0, pady=5)

        ttk.Label(self.extra_frame, text="Cantidad de Personas").grid(row=4, column=0, pady=5)
        self.num_people = ttk.Entry(self.extra_frame)
        self.num_people.grid(row=5, column=0, pady=5)

        # Botón para registrar reserva
        self.register_button = ttk.Button(self.extra_frame, text="Registrar Reserva", command=self.registrar_reserva)  # Sin command por ahora
        self.register_button.grid(row=6, column=0, pady=10)
        
        # Inicialmente los campos adicionales están ocultos
        self.extra_frame.grid_forget()

        # Cargar clientes al iniciar la vista
        self.cargar_reservas()


    def cargar_reservas(self):
        reservas = self.reservasService.obtener_reservas_detalladas()  # Supongo que este método devuelve una lista de clientes
        for reserva in reservas:
            id_reserva = reserva[0]
            nombre_completo = f"{reserva[1]} {reserva[2]}"  # Nombre y apellido concatenados
            numero_habitacion = reserva[3]
            fecha_entrada = reserva[4]
            fecha_salida = reserva[5]
            
            self.reservation_table.insert("", "end", values=(id_reserva, nombre_completo, numero_habitacion, fecha_entrada, fecha_salida))


    def buscar_habitaciones(self):
        # Obtener las fechas de entrada y salida seleccionadas
        self.fecha_inicio = datetime.strptime(self.entry_date.get_date(), "%Y-%m-%d").date()
        self.fecha_fin = datetime.strptime(self.exit_date.get_date(), "%Y-%m-%d").date()

        # Validar las fechas
        if not self.reservasService.validar_fechas(self.fecha_inicio, self.fecha_fin):
            tk.messagebox.showinfo("Error", "La fecha de salida debe ser posterior a la de entrada.")
            return
        
        # Obtener habitaciones disponibles
        habitaciones_disponibles = self.reservasService.buscar_habitaciones_disponibles(self.fecha_inicio, self.fecha_fin)
        if habitaciones_disponibles:
            self.extra_frame.grid(row=0, column=2, rowspan=3, padx=20)

            # Cargar clientes en el diccionario y en el Combobox
            self.clientes_dict = {f"{cliente[1]} {cliente[2]}": cliente[0] for cliente in self.gestorBD.obtener_clientes()}
            self.cliente_combobox['values'] = list(self.clientes_dict.keys())

            # Llenar el ComboBox de habitaciones disponibles
            self.habitacion_combobox['values'] = [habitacion[0] for habitacion in habitaciones_disponibles]

        else:
            tk.messagebox.showinfo("Sin habitaciones disponibles", "No se encontraron habitaciones disponibles para las fechas seleccionadas.")
            self.extra_frame.grid_forget()

    def registrar_reserva(self):
        try:

            nombre_cliente = self.cliente_combobox.get()
            cliente_id = self.clientes_dict.get(nombre_cliente)
            habitacion = self.habitacion_combobox.get()
            num_personas = self.num_people.get()

            id_reserva = self.gestorBD.obtener_proximo_id_reserva()
            self.reservasService.registrar_reserva(id_reserva, cliente_id, habitacion, self.fecha_inicio, self.fecha_fin, num_personas)

            # Si se registra correctamente, actualiza la tabla
            self.reservation_table.insert("", "end", values=(id_reserva, nombre_cliente, habitacion, self.fecha_inicio, self.fecha_fin))

            tk.messagebox.showinfo("Reserva Registrada", "La reserva ha sido registrada exitosamente.")

        except ValueError as e:
            # Muestra un cuadro de diálogo emergente con el mensaje de error
            tk.messagebox.showerror("Error", str(e))
        
    def finalizar_estadia(self):
        selected_item = self.reservation_table.selection()
        if not selected_item:
            tk.messagebox.showwarning("Advertencia", "Por favor, selecciona una reserva para finalizar la estadía.")
            return

        # Obtener los valores de la reserva seleccionada
        reserva_data = self.reservation_table.item(selected_item)["values"]
        id_reserva = reserva_data[0]  # Suponiendo que el ID de la reserva está en la primera columna
        cliente = reserva_data[1]
        habitacion = reserva_data[2]
        # Convertir las fechas de entrada y salida a objetos de fecha
        fecha_entrada = datetime.strptime(reserva_data[3], "%Y-%m-%d").date()
        fecha_salida = datetime.strptime(reserva_data[4], "%Y-%m-%d").date()

        # Calcular la diferencia en días
        dias = (fecha_salida - fecha_entrada).days
        # Confirmación para finalizar estadía
        if tk.messagebox.askyesno("Finalizar Estadía", "¿Estás seguro de que deseas finalizar la estadía de esta reserva?"):
            # Lógica para finalizar la estadía (puede ser una actualización en la base de datos, por ejemplo)
            self.reservasService.finalizar_estadia(id_reserva, habitacion, dias)  # Implementa este método en ReservaService
            self.tab_frame.event_generate("<<FacturaGenerada>>")
            # Eliminar la reserva de la tabla
            self.reservation_table.delete(selected_item)

            # Mostrar mensaje de éxito
            tk.messagebox.showinfo("Éxito", "La estadía ha sido finalizada correctamente.")

            