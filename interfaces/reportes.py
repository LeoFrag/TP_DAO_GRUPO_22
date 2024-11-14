# habitaciones.py
import tkinter as tk
from tkinter import ttk

class ReportesTab:
    def __init__(self, parent_frame, gestorBD):
        self.tab = parent_frame
        self.gestorBD = gestorBD
        self.setup_ui()

    def setup_ui(self):
        ttk.Button(self.tab, text="Generar Reporte de Ocupación").pack(pady=10)