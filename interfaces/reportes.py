import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
from tkinter import messagebox
import os
from services.reservas import ReservaService
from services.habitaciones import HabitacionService
import matplotlib.dates as mdates
from collections import defaultdict
import matplotlib.pyplot as plt


class ReportesTab:
    def __init__(self, parent_frame, gestorBD):
        self.tab = parent_frame
        self.gestorBD = gestorBD
        self.reservasService = ReservaService(self.gestorBD)
        self.habitacionesService = HabitacionService(self.gestorBD)
        self.setup_ui()

    def setup_ui(self):
        # Botón para abrir la ventana de selección de fechas
        btn_listar_reservas = ttk.Button(
            self.tab, 
            text="Listar reservas en un periodo", 
            command=self.abrir_ventana_fechas
        )
        btn_listar_reservas.pack(pady=10)

        # Botón para abrir la ventana de generación de reporte de ingresos
        btn_ingresos = ttk.Button(
            self.tab, 
            text="Generar reporte de ingresos por habitaciones", 
            command=self.generar_reporte_ingresos
        )
        btn_ingresos.pack(pady=10)

        # Botón para abrir la ventana de generación de reporte de ingresos
        btn_ingresos = ttk.Button(
            self.tab, 
            text="Generar reporte de ocupacion", 
            command=self.generar_reporte_ocupacion
        )
        btn_ingresos.pack(pady=10)


    def abrir_ventana_fechas(self):
        # Crear una ventana emergente
        ventana_fechas = tk.Toplevel(self.tab)
        ventana_fechas.title("Seleccionar Periodo de Reservas")

        # Etiqueta y calendario para Fecha Desde
        tk.Label(ventana_fechas, text="Fecha Desde:").pack(pady=5)
        self.fecha_desde = DateEntry(ventana_fechas, date_pattern='yyyy-mm-dd')
        self.fecha_desde.pack(pady=5)

        # Etiqueta y calendario para Fecha Hasta
        tk.Label(ventana_fechas, text="Fecha Hasta:").pack(pady=5)
        self.fecha_hasta = DateEntry(ventana_fechas, date_pattern='yyyy-mm-dd')
        self.fecha_hasta.pack(pady=5)

        # Botón para generar el reporte
        btn_generar = ttk.Button(
            ventana_fechas, 
            text="Generar Reporte", 
            command=self.generar_reporte_pdf
        )
        btn_generar.pack(pady=10)

    def generar_reporte_pdf(self):
        # Obtener las fechas seleccionadas
        fecha_desde = self.fecha_desde.get_date()
        fecha_hasta = self.fecha_hasta.get_date()

        # Validación de fechas
        if fecha_desde > fecha_hasta:
            messagebox.showerror("Error", "La fecha 'Desde' debe ser anterior a la fecha 'Hasta'.")
            return

        # Consultar la base de datos para obtener las reservas en el rango de fechas
        reservas = self.reservasService.obtener_reservas_por_periodo(fecha_desde, fecha_hasta)

        if not reservas:
            messagebox.showinfo("Información", "No se encontraron reservas en el periodo seleccionado.")
            return

        # Crear el PDF del reporte
        self.crear_pdf_reservas(fecha_desde, fecha_hasta, reservas)
        messagebox.showinfo("Reporte Generado", "El reporte de reservas ha sido generado con éxito.")


    def calcular_ingresos_por_mes(self, reservas):
        # Inicializar un diccionario para almacenar los ingresos por mes
        ingresos_por_mes = defaultdict(float)

        for reserva in reservas:
            # Desempaquetamos los datos de la reserva
            id_reserva, id_cliente, numero_habitacion, fecha_entrada, fecha_salida, cantidad_personas = reserva

            # Convertir las fechas de string a datetime
            fecha_entrada = datetime.strptime(fecha_entrada, '%Y-%m-%d')  # Asumiendo el formato 'YYYY-MM-DD'
            fecha_salida = datetime.strptime(fecha_salida, '%Y-%m-%d')    # Asumiendo el formato 'YYYY-MM-DD'

            # Calcular el número de noches que estuvo la reserva
            dias_estadia = (fecha_salida - fecha_entrada).days

            # Obtener el precio por noche de la habitación
            precio_noche = self.habitacionesService.obtener_precio_por_noche(numero_habitacion)
            # Calcular los ingresos por esta reserva
            ingresos_reserva = dias_estadia * precio_noche

            # Agrupar los ingresos por mes de la fecha de entrada
            mes = fecha_entrada.strftime('%m')  # Formato MM
            ingresos_por_mes[mes] += ingresos_reserva

        return dict(ingresos_por_mes)
    
    def generar_reporte_ingresos(self):

        # Consultar la base de datos para obtener las reservas en el rango de fechas
        reservas = self.reservasService.obtener_reservas()

        if not reservas:
            messagebox.showinfo("Información", "No se encontraron reservas en el periodo seleccionado.")
            return

        # Calcular ingresos por habitación
        ingresos_por_mes = self.calcular_ingresos_por_mes(reservas)

        # Nombre del archivo PDF
        nombre_pdf = f"reporte_ingresos.pdf"

        # Crear el gráfico y obtener la ruta de la imagen
        img_path = self.crear_grafico_ingresos(ingresos_por_mes)

        # Crear el PDF con el reporte
        self.crear_pdf_ingresos(ingresos_por_mes, nombre_pdf, img_path)

        messagebox.showinfo("Reporte Generado", "El reporte de ingresos ha sido generado con éxito.")

    def generar_reporte_ocupacion(self):

        # Consultar la base de datos para obtener las reservas en el rango de fechas
        reservas = self.reservasService.obtener_reservas()

        if not reservas:
            messagebox.showinfo("Información", "No se encontraron reservas.")
            return

        # Calcular la ocupación promedio por tipo de habitación
        ocupacion_promedio = self.calcular_ocupacion_por_tipo_habitacion(reservas)

        # Nombre del archivo PDF
        nombre_pdf = f"reporte_ocupacion.pdf"

        # Crear el gráfico y obtener la ruta de la imagen
        img_path = self.crear_grafico_ocupacion(ocupacion_promedio)

        # Crear el PDF con el reporte
        self.crear_pdf_ocupacion(ocupacion_promedio, nombre_pdf, img_path)

        messagebox.showinfo("Reporte Generado", "El reporte de ocupación ha sido generado con éxito.")

    def calcular_ocupacion_por_tipo_habitacion(self, reservas):
        # Inicializar un diccionario para almacenar la ocupación por tipo de habitación
        ocupacion_por_tipo = defaultdict(float)
        cantidad_por_tipo = defaultdict(int)  # Para contar cuántas reservas por tipo

        for reserva in reservas:
            # Desempaquetamos los datos de la reserva
            id_reserva, id_cliente, numero_habitacion, fecha_entrada, fecha_salida, cantidad_personas = reserva

            tipo_habitacion = self.habitacionesService.obtener_tipo_habitacion(numero_habitacion)
            # Convertir las fechas de string a datetime
            fecha_entrada = datetime.strptime(fecha_entrada, '%Y-%m-%d')  # Asumiendo el formato 'YYYY-MM-DD'
            fecha_salida = datetime.strptime(fecha_salida, '%Y-%m-%d')    # Asumiendo el formato 'YYYY-MM-DD'

            # Calcular el número de noches que estuvo la reserva
            dias_estadia = (fecha_salida - fecha_entrada).days

            # Agrupar la ocupación por tipo de habitación
           # Incrementar el contador de ocupación por tipo de habitación
            ocupacion_por_tipo[tipo_habitacion] += dias_estadia
            cantidad_por_tipo[tipo_habitacion] += 1  # Contamos el total de habitaciones de cada tipo

        # Calcular el promedio de ocupación por tipo de habitación
        ocupacion_promedio = {tipo: ocupacion_por_tipo[tipo] / cantidad_por_tipo[tipo] for tipo in ocupacion_por_tipo}
        
        return ocupacion_promedio
    def crear_grafico_ocupacion(self, ocupacion_promedio):
        # Crear gráfico de torta para la ocupación promedio por tipo de habitación
        labels = list(ocupacion_promedio.keys())
        sizes = list(ocupacion_promedio.values())

        plt.figure(figsize=(8, 8))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#66b3ff', '#99ff99', '#ffcc99'])
        plt.title("Ocupación Promedio por Tipo de Habitación", fontsize=16)

        # Guardar el gráfico como una imagen temporal
        img_path = "grafico_ocupacion.png"
        plt.tight_layout()
        plt.savefig(img_path)

        # Cerrar el gráfico para liberar memoria
        plt.close()

        return img_path
    def crear_pdf_ingresos(self,ingresos_por_mes, nombre_pdf, img_path): 
        # Configuración del archivo PDF
        c = canvas.Canvas(nombre_pdf, pagesize=A4)
        ancho, alto = A4

        # Título
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, alto - 50, "Reporte de Ingresos por Habitaciones")
        c.setFont("Helvetica", 10)
        c.drawString(50, alto - 70, f"Periodo: 2024")
        c.drawString(50, alto - 90, f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d')}")

        # Encabezado de la tabla de ingresos
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, alto - 120, "Mes")
        c.drawString(200, alto - 120, "Ingresos ($)")

        # Cuerpo de la tabla de ingresos
        y_offset = alto - 140
        c.setFont("Helvetica", 9)
        for mes, ingresos in ingresos_por_mes.items():
            c.drawString(50, y_offset, mes)
            c.drawString(200, y_offset, f"{ingresos:.2f}")
            y_offset -= 20
            if y_offset < 50:  # Nueva página si el espacio en la actual se acaba
                c.showPage()  # Inicia una nueva página
                y_offset = alto - 50

        # Crear una nueva página para el gráfico
        c.showPage()  # Esto crea una nueva página
        y_offset = alto - 300  # Reinicia el offset de la página para la imagen

        # Insertar el gráfico en la nueva página
        c.drawImage(img_path, 50, y_offset, width=500, height=300)

        c.save()
        os.startfile(nombre_pdf)  # Abre automáticamente el PDF al finalizar (solo en Windows)



    def crear_grafico_ingresos(self, ingresos_por_mes):
        # Asegurarse de que todos los meses del 1 al 12 estén en el diccionario
        ingresos_por_mes_completo = {str(i).zfill(2): 0.0 for i in range(1, 13)}  # Inicializa todos los meses con 0
        ingresos_por_mes_completo.update(ingresos_por_mes)  # Actualiza con los datos existentes

        # Preparar los datos para el gráfico
        meses = list(ingresos_por_mes_completo.keys())  # Lista de meses como strings: '01', '02', ..., '12'
        ingresos = list(ingresos_por_mes_completo.values())  # Lista de ingresos correspondientes a cada mes

        # Crear gráfico de líneas
        plt.figure(figsize=(10, 6))
        plt.plot(meses, ingresos, marker='o', color='b', linestyle='-', linewidth=2, markersize=6)

        # Configurar el gráfico
        plt.title("Ingresos por Habitaciones (Mensual)", fontsize=16)
        plt.xlabel("Mes", fontsize=12)
        plt.ylabel("Ingresos (en $)", fontsize=12)
        plt.xticks(rotation=45)  # Rotar las etiquetas del eje X para que se lean mejor
        plt.grid(True)

        # Configurar los límites y formato del eje X
        plt.xlim(0, 12)  # Asegura que el eje X vaya de 1 a 12
        plt.xticks(range(1, 13), ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'])  # Meses en español

        # Guardar el gráfico como una imagen temporal
        img_path = "grafico_ingresos.png"
        plt.tight_layout()
        plt.savefig(img_path)

        # Cerrar el gráfico para liberar memoria
        plt.close()

        return img_path

        
    def crear_pdf_reservas(self, fecha_desde, fecha_hasta, reservas):
        # Configuración del archivo PDF
        nombre_pdf = f"reporte_reservas_{fecha_desde}_{fecha_hasta}.pdf"
        c = canvas.Canvas(nombre_pdf, pagesize=A4)
        ancho, alto = A4

        # Título
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, alto - 50, "Reporte de Reservas")
        c.setFont("Helvetica", 10)
        c.drawString(50, alto - 70, f"Periodo: {fecha_desde} - {fecha_hasta}")
        c.drawString(50, alto - 90, f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d')}")

        # Encabezado de la tabla
        c.setFont("Helvetica-Bold", 10)
        headers = ["ID Reserva", "Cliente", "Habitación", "Fecha Entrada", "Fecha Salida", "Estado"]
        x_offset = 50
        y_offset = alto - 120
        for header in headers:
            c.drawString(x_offset, y_offset, header)
            x_offset += 90

        # Cuerpo de la tabla con las reservas
        y_offset -= 20
        c.setFont("Helvetica", 9)
        for reserva in reservas:
            x_offset = 50
            for dato in reserva:
                c.drawString(x_offset, y_offset, str(dato))
                x_offset += 90
            y_offset -= 20
            if y_offset < 50:  # Nueva página si el espacio en la actual se acaba
                c.showPage()
                y_offset = alto - 50

        c.save()
        os.startfile(nombre_pdf)

    def crear_pdf_ocupacion(self,ocupacion_promedio, nombre_pdf, img_path):
        # Configuración del archivo PDF
        c = canvas.Canvas(nombre_pdf, pagesize=A4)
        ancho, alto = A4

        # Título
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, alto - 50, "Reporte de Ocupación Promedio por Tipo de Habitación")
        c.setFont("Helvetica", 10)
        c.drawString(50, alto - 90, f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d')}")

        # Encabezado de la tabla de ocupación
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, alto - 120, "Tipo de Habitación")
        c.drawString(200, alto - 120, "Ocupación Promedio (días)")

        # Cuerpo de la tabla de ocupación
        y_offset = alto - 140
        c.setFont("Helvetica", 9)
        for tipo, ocupacion in ocupacion_promedio.items():
            c.drawString(50, y_offset, str(tipo))  # Tipo de habitación
            c.drawString(200, y_offset, f"{ocupacion:.2f}")  # Ocupación promedio
            y_offset -= 20
            if y_offset < 50:  # Nueva página si el espacio en la actual se acaba
                c.showPage()  # Inicia una nueva página
                y_offset = alto - 50

        # Crear una nueva página para el gráfico
        c.showPage()  # Esto crea una nueva página
        y_offset = alto - 300  # Reinicia el offset de la página para la imagen

        # Insertar el gráfico en la nueva página
        c.drawImage(img_path, 50, y_offset, width=500, height=300)

        c.save()
        os.startfile(nombre_pdf)  # Abre automáticamente el PDF al finalizar (solo en Windows)