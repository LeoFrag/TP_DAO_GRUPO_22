import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os
from services.reservas import ReservaService
from services.habitaciones import HabitacionService
import matplotlib.pyplot as plt
from collections import defaultdict

class ReportesTab:
    def __init__(self, parent_frame, gestorBD):
        self.tab = parent_frame
        self.gestorBD = gestorBD
        self.reservasService = ReservaService(self.gestorBD)
        self.habitacionesService = HabitacionService(self.gestorBD)
        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style()
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TButton", padding=10, font=('Helvetica', 10))
        style.configure("TLabel", background="#f0f0f0", font=('Helvetica', 11))
        style.configure("Header.TLabel", font=('Helvetica', 16, 'bold'))

        main_frame = ttk.Frame(self.tab, style="TFrame")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        ttk.Label(main_frame, text="Informes y Reportes", style="Header.TLabel").pack(pady=(0, 20))

        reports_frame = ttk.Frame(main_frame, style="TFrame")
        reports_frame.pack(fill="x", expand=True)

        self.create_report_button(reports_frame, "Listar reservas en un periodo", self.abrir_ventana_fechas)
        self.create_report_button(reports_frame, "Generar reporte de ingresos por habitaciones", self.generar_reporte_ingresos)
        self.create_report_button(reports_frame, "Generar reporte de ocupación", self.generar_reporte_ocupacion)

    def create_report_button(self, parent, text, command):
        frame = ttk.Frame(parent, style="TFrame")
        frame.pack(fill="x", pady=5)
        
        btn = ttk.Button(frame, text=text, command=command, style="TButton")
        btn.pack(fill="x")

        description = ttk.Label(frame, text=self.get_description(text), style="TLabel")
        description.pack(fill="x")

    def get_description(self, button_text):
        descriptions = {
            "Listar reservas en un periodo": "Visualice todas las reservas realizadas en un rango de fechas específico",
            "Generar reporte de ingresos por habitaciones": "Obtenga un informe detallado de los ingresos generados por cada habitación",
            "Generar reporte de ocupación": "Visualice las estadísticas de ocupación del hotel en diferentes periodos"
        }
        return descriptions.get(button_text, "")

    def abrir_ventana_fechas(self):
        ventana_fechas = tk.Toplevel(self.tab)
        ventana_fechas.title("Seleccionar Periodo de Reservas")
        ventana_fechas.geometry("300x200")

        ttk.Label(ventana_fechas, text="Fecha Desde:", style="TLabel").pack(pady=5)
        self.fecha_desde = DateEntry(ventana_fechas, date_pattern='yyyy-mm-dd', style="TEntry")
        self.fecha_desde.pack(pady=5)

        ttk.Label(ventana_fechas, text="Fecha Hasta:", style="TLabel").pack(pady=5)
        self.fecha_hasta = DateEntry(ventana_fechas, date_pattern='yyyy-mm-dd', style="TEntry")
        self.fecha_hasta.pack(pady=5)

        ttk.Button(ventana_fechas, text="Generar Reporte", command=self.generar_reporte_pdf, style="TButton").pack(pady=10)

    def generar_reporte_pdf(self):
        fecha_desde = self.fecha_desde.get_date()
        fecha_hasta = self.fecha_hasta.get_date()

        if fecha_desde > fecha_hasta:
            messagebox.showerror("Error", "La fecha 'Desde' debe ser anterior a la fecha 'Hasta'.")
            return

        reservas = self.reservasService.obtener_reservas_por_periodo(fecha_desde, fecha_hasta)

        if not reservas:
            messagebox.showinfo("Información", "No se encontraron reservas en el periodo seleccionado.")
            return

        self.crear_pdf_reservas(fecha_desde, fecha_hasta, reservas)
        messagebox.showinfo("Reporte Generado", "El reporte de reservas ha sido generado con éxito.")

    def generar_reporte_ingresos(self):
        reservas = self.reservasService.obtener_reservas()

        if not reservas:
            messagebox.showinfo("Información", "No se encontraron reservas.")
            return

        ingresos_por_mes = self.calcular_ingresos_por_mes(reservas)
        nombre_pdf = f"reporte_ingresos.pdf"
        img_path = self.crear_grafico_ingresos(ingresos_por_mes)
        self.crear_pdf_ingresos(ingresos_por_mes, nombre_pdf, img_path)
        messagebox.showinfo("Reporte Generado", "El reporte de ingresos ha sido generado con éxito.")

    def generar_reporte_ocupacion(self):
        reservas = self.reservasService.obtener_reservas()

        if not reservas:
            messagebox.showinfo("Información", "No se encontraron reservas.")
            return

        ocupacion_promedio = self.calcular_ocupacion_por_tipo_habitacion(reservas)
        nombre_pdf = f"reporte_ocupacion.pdf"
        img_path = self.crear_grafico_ocupacion(ocupacion_promedio)
        self.crear_pdf_ocupacion(ocupacion_promedio, nombre_pdf, img_path)
        messagebox.showinfo("Reporte Generado", "El reporte de ocupación ha sido generado con éxito.")

    def calcular_ingresos_por_mes(self, reservas):
        ingresos_por_mes = defaultdict(float)
        for reserva in reservas:
            id_reserva, id_cliente, numero_habitacion, fecha_entrada, fecha_salida, cantidad_personas, finalizada = reserva
            fecha_entrada = datetime.strptime(fecha_entrada, '%Y-%m-%d')
            fecha_salida = datetime.strptime(fecha_salida, '%Y-%m-%d')
            dias_estadia = (fecha_salida - fecha_entrada).days
            precio_noche = self.habitacionesService.obtener_precio_por_noche(numero_habitacion)
            ingresos_reserva = dias_estadia * precio_noche
            mes = fecha_entrada.strftime('%m')
            ingresos_por_mes[mes] += ingresos_reserva
        return dict(ingresos_por_mes)

    def calcular_ocupacion_por_tipo_habitacion(self, reservas):
        ocupacion_por_tipo = defaultdict(float)
        cantidad_por_tipo = defaultdict(int)
        for reserva in reservas:
            id_reserva, id_cliente, numero_habitacion, fecha_entrada, fecha_salida, cantidad_personas, finalizada = reserva
            tipo_habitacion = self.habitacionesService.obtener_tipo_habitacion(numero_habitacion)
            fecha_entrada = datetime.strptime(fecha_entrada, '%Y-%m-%d')
            fecha_salida = datetime.strptime(fecha_salida, '%Y-%m-%d')
            dias_estadia = (fecha_salida - fecha_entrada).days
            ocupacion_por_tipo[tipo_habitacion] += dias_estadia
            cantidad_por_tipo[tipo_habitacion] += 1
        return {tipo: ocupacion_por_tipo[tipo] / cantidad_por_tipo[tipo] for tipo in ocupacion_por_tipo}

    def crear_grafico_ocupacion(self, ocupacion_promedio):
        labels = list(ocupacion_promedio.keys())
        sizes = list(ocupacion_promedio.values())
        plt.figure(figsize=(8, 8))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#66b3ff', '#99ff99', '#ffcc99'])
        plt.title("Ocupación Promedio por Tipo de Habitación", fontsize=16)
        img_path = "grafico_ocupacion.png"
        plt.tight_layout()
        plt.savefig(img_path)
        plt.close()
        return img_path

    def crear_grafico_ingresos(self, ingresos_por_mes):
        ingresos_por_mes_completo = {str(i).zfill(2): 0.0 for i in range(1, 13)}
        ingresos_por_mes_completo.update(ingresos_por_mes)
        meses = list(ingresos_por_mes_completo.keys())
        ingresos = list(ingresos_por_mes_completo.values())
        plt.figure(figsize=(10, 6))
        plt.plot(meses, ingresos, marker='o', color='b', linestyle='-', linewidth=2, markersize=6)
        plt.title("Ingresos por Habitaciones (Mensual)", fontsize=16)
        plt.xlabel("Mes", fontsize=12)
        plt.ylabel("Ingresos (en $)", fontsize=12)
        plt.xticks(range(1, 13), ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'], rotation=45)
        plt.grid(True)
        plt.xlim(0, 12)
        img_path = "grafico_ingresos.png"
        plt.tight_layout()
        plt.savefig(img_path)
        plt.close()
        return img_path

    def crear_pdf_reservas(self, fecha_desde, fecha_hasta, reservas):
        nombre_pdf = f"reporte_reservas_{fecha_desde}_{fecha_hasta}.pdf"
        c = canvas.Canvas(nombre_pdf, pagesize=A4)
        ancho, alto = A4
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, alto - 50, "Reporte de Reservas")
        c.setFont("Helvetica", 10)
        c.drawString(50, alto - 70, f"Periodo: {fecha_desde} - {fecha_hasta}")
        c.drawString(50, alto - 90, f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d')}")
        c.setFont("Helvetica-Bold", 10)
        headers = ["ID Reserva", "Cliente", "Habitación", "Fecha Entrada", "Fecha Salida", "Cantidad"]
        x_offset = 50
        y_offset = alto - 120
        for header in headers:
            c.drawString(x_offset, y_offset, header)
            x_offset += 90
        y_offset -= 20
        c.setFont("Helvetica", 9)
        for reserva in reservas:
            x_offset = 50
            for dato in reserva:
                c.drawString(x_offset, y_offset, str(dato))
                x_offset += 90
            y_offset -= 20
            if y_offset < 50:
                c.showPage()
                y_offset = alto - 50
        c.save()
        os.startfile(nombre_pdf)

    def crear_pdf_ingresos(self, ingresos_por_mes, nombre_pdf, img_path):
        c = canvas.Canvas(nombre_pdf, pagesize=A4)
        ancho, alto = A4
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, alto - 50, "Reporte de Ingresos por Habitaciones")
        c.setFont("Helvetica", 10)
        c.drawString(50, alto - 70, f"Periodo: 2024")
        c.drawString(50, alto - 90, f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d')}")
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, alto - 120, "Mes")
        c.drawString(200, alto - 120, "Ingresos ($)")
        y_offset = alto - 140
        c.setFont("Helvetica", 9)
        for mes, ingresos in ingresos_por_mes.items():
            c.drawString(50, y_offset, mes)
            c.drawString(200, y_offset, f"{ingresos:.2f}")
            y_offset -= 20
            if y_offset < 50:
                c.showPage()
                y_offset = alto - 50
        c.showPage()
        y_offset = alto - 300
        c.drawImage(img_path, 50, y_offset, width=500, height=300)
        c.save()
        os.startfile(nombre_pdf)

    def crear_pdf_ocupacion(self, ocupacion_promedio, nombre_pdf, img_path):
        c = canvas.Canvas(nombre_pdf, pagesize=A4)
        ancho, alto = A4
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, alto - 50, "Reporte de Ocupación Promedio por Tipo de Habitación")
        c.setFont("Helvetica", 10)
        c.drawString(50, alto - 90, f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d')}")
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, alto - 120, "Tipo de Habitación")
        c.drawString(200, alto - 120, "Ocupación Promedio (días)")
        y_offset = alto - 140
        c.setFont("Helvetica", 9)
        for tipo, ocupacion in ocupacion_promedio.items():
            c.drawString(50, y_offset, str(tipo))
            c.drawString(200, y_offset, f"{ocupacion:.2f}")
            y_offset -= 20
            if y_offset < 50:
                c.showPage()
                y_offset = alto - 50
        c.showPage()
        y_offset = alto - 300
        c.drawImage(img_path, 50, y_offset, width=500, height=300)
        c.save()
        os.startfile(nombre_pdf)