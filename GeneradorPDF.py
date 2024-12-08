from fpdf import FPDF
from datetime import datetime
import os

class GeneradorPDF:
    def __init__(self, nombre_archivo="evento.pdf"):
        self.nombre_archivo = nombre_archivo
        self.pdf = FPDF()
        self.pdf.set_font("Arial", size=12)
    
    def generar_evento(self, evento):
        """
        Genera el PDF con los detalles de un evento y lo guarda.
        
        evento: tupla con los datos del evento en el siguiente orden:
            No., fecha, nombre, apellido_paterno, apellido_materno, telefono, salon, descripcion
        """
        self.pdf.add_page()
        
        # Encabezado
        self.pdf.set_font("Arial", style='B', size=16)
        self.pdf.cell(200, 10, txt="Detalles del Evento", ln=True, align='C')
        self.pdf.ln(10)  # Espacio

        # Datos del evento
        self.pdf.set_font("Arial", size=12)
        self.pdf.cell(0, 10, txt=f"ID del Evento: {evento[0]}", ln=True)
        self.pdf.cell(0, 10, txt=f"Fecha: {evento[1].strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
        self.pdf.cell(0, 10, txt=f"Nombre del Cliente: {evento[2]} {evento[3]} {evento[4]}", ln=True)
        self.pdf.cell(0, 10, txt=f"Teléfono: {evento[5]}", ln=True)
        self.pdf.cell(0, 10, txt=f"Salón: {evento[6]}", ln=True)
        self.pdf.cell(0, 10, txt=f"Descripción: {evento[7]}", ln=True)

        # Guardar el PDF
        self.pdf.output(self.nombre_archivo)
        # Abrir el PDF después de guardarlo
        os.startfile(self.nombre_archivo)
        print(f"PDF generado y guardado como: {self.nombre_archivo}")
