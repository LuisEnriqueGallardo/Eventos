from fpdf import FPDF
from datetime import datetime
import os

class GeneradorPDF:
    def __init__(self, nombre_archivo="evento.pdf"):
        self.nombre_archivo = nombre_archivo
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.pdf.set_font("Arial", size=12)

    def generar_evento(self, evento):
        """
        Genera un PDF con la información del evento.
        Args:
            evento (tuple): Información del evento en el siguiente orden:
                            No., fecha, nombre, apellido_paterno, apellido_materno, telefono, salon, descripcion
        """
        self.pdf.add_page()

        # Encabezado
        self.pdf.set_font("Arial", style="B", size=24)
        self.pdf.cell(0, 10, txt="Eventify", ln=True, align="C")
        self.pdf.set_font("Arial", size=12)
        self.pdf.cell(0, 10, txt="Transformando momentos en recuerdos inolvidables.", ln=True, align="C")
        self.pdf.ln(20)  # Espacio

        # Línea separadora
        self.pdf.set_draw_color(0, 0, 0)
        self.pdf.set_line_width(0.5)
        self.pdf.line(10, 40, 200, 40)
        self.pdf.ln(10)  # Espacio

        # Datos del evento
        self.pdf.set_font("Arial", style="B", size=14)
        self.pdf.cell(0, 10, txt="Detalles del Evento", ln=True, align="L")
        self.pdf.ln(5)

        self.pdf.set_font("Arial", size=12)
        self.pdf.cell(50, 10, txt="Número de Evento:", border=0)
        self.pdf.cell(0, 10, txt=f"{evento[0]}", ln=True)
        self.pdf.cell(50, 10, txt="Fecha:", border=0)
        self.pdf.cell(0, 10, txt=f"{evento[1].strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
        self.pdf.cell(50, 10, txt="Nombre del Cliente:", border=0)
        self.pdf.cell(0, 10, txt=f"{evento[2]} {evento[3]} {evento[4]}", ln=True)
        self.pdf.cell(50, 10, txt="Teléfono:", border=0)
        self.pdf.cell(0, 10, txt=f"{evento[5]}", ln=True)
        self.pdf.cell(50, 10, txt="Salón:", border=0) 
        self.pdf.cell(0, 10, txt=f"{evento[6]}", ln=True)
        self.pdf.cell(50, 10, txt="Descripción:", border=0)
        self.pdf.multi_cell(0, 10, txt=f"{evento[7]}")

        # Línea separadora
        self.pdf.ln(10)
        self.pdf.line(10, self.pdf.get_y(), 200, self.pdf.get_y())
        self.pdf.ln(10)

              # Texto grande "PAGADO"
        self.pdf.set_font("Arial", style="B", size=50)
        self.pdf.set_text_color(255, 0, 0)
        self.pdf.cell(0, 10, txt="PENDIENTE", ln=True, align="C")

        # Pie de página
        self.pdf.set_y(-30)
        self.pdf.set_font("Arial", size=10)
        self.pdf.cell(0, 10, txt="Gracias por confiar en Eventify.", ln=True, align="C")
        self.pdf.image("logoEven.png", x=10, y=self.pdf.get_y() - 20, w=33)

        # Guardar el PDF
        self._guardar_pdf()

    def agregar_servicios(self, servicios):
        """
        Agrega la información de los servicios contratados al PDF.
        Args:
            servicios (list): Lista de tuplas con la información de los servicios contratados.
                              Cada tupla debe contener (servicio, descripcion, telefono).
        """
        self.pdf.add_page()

        # Encabezado
        self.pdf.set_font("Arial", style="B", size=24)
        self.pdf.cell(0, 10, txt="Eventify", ln=True, align="C")
        self.pdf.set_font("Arial", size=12)
        self.pdf.cell(0, 10, txt="Transformando momentos en recuerdos inolvidables.", ln=True, align="C")
        self.pdf.ln(20)  # Espacio

        # Línea separadora
        self.pdf.set_draw_color(0, 0, 0)
        self.pdf.set_line_width(0.5)
        self.pdf.line(10, 40, 200, 40)
        self.pdf.ln(10)  # Espacio

        # Datos de los servicios
        self.pdf.set_font("Arial", style="B", size=14)
        self.pdf.cell(0, 10, txt="Servicios Contratados", ln=True, align="L")
        self.pdf.ln(5)

        self.pdf.set_font("Arial", size=12)
        for servicio in servicios:
            self.pdf.cell(50, 10, txt="Servicio:", border=0)
            self.pdf.cell(0, 10, txt=f"{servicio[1]}", ln=True)
            self.pdf.cell(50, 10, txt="Descripción:", border=0)
            self.pdf.multi_cell(0, 10, txt=f"{servicio[2]}")
            self.pdf.cell(50, 10, txt="Teléfono de Contacto:", border=0)
            self.pdf.cell(0, 10, txt=f"{servicio[3]}", ln=True)
            self.pdf.ln(5)
            self.pdf.cell(0, 10, txt="--- Siguiente ---", ln=True, align="C")

        # Línea separadora
        self.pdf.ln(10)
        self.pdf.line(10, self.pdf.get_y(), 200, self.pdf.get_y())
        self.pdf.ln(10)

        # Pie de página
        self.pdf.set_y(-30)
        self.pdf.set_font("Arial", size=10)
        self.pdf.cell(0, 10, txt="Gracias por confiar en Eventify.", ln=True, align="C")
        self.pdf.image("logoEven.png", x=10, y=self.pdf.get_y() - 20, w=33)

        # Guardar el PDF
        self._guardar_pdf()

    def agregar_evento_pagado(self, evento):
        """
        Agrega la información del evento pagado al PDF.
        Args:
            evento (tuple): Información del evento en el siguiente orden:
                            No., fecha, descripcion, nombre_completo, total, anticipo, servicio
        """
        self.pdf.add_page()

        # Encabezado
        self.pdf.set_font("Arial", style="B", size=24)
        self.pdf.cell(0, 10, txt="Eventify", ln=True, align="C")
        self.pdf.set_font("Arial", size=12)
        self.pdf.cell(0, 10, txt="Transformando momentos en recuerdos inolvidables.", ln=True, align="C")
        self.pdf.ln(20)  # Espacio

        # Línea separadora
        self.pdf.set_draw_color(0, 0, 0)
        self.pdf.set_line_width(0.5)
        self.pdf.line(10, 40, 200, 40)
        self.pdf.ln(10)  # Espacio

        # Datos del evento pagado
        self.pdf.set_font("Arial", style="B", size=14)
        self.pdf.cell(0, 10, txt="Detalles del Evento Pagado", ln=True, align="L")
        self.pdf.ln(5)

        self.pdf.set_font("Arial", size=12)
        self.pdf.cell(50, 10, txt="ID del Evento:", border=0)
        self.pdf.cell(0, 10, txt=f"{evento[0]}", ln=True)
        self.pdf.cell(50, 10, txt="Fecha:", border=0)
        self.pdf.cell(0, 10, txt=f"{evento[1]}", ln=True)
        self.pdf.cell(50, 10, txt="Descripción:", border=0)
        self.pdf.multi_cell(0, 10, txt=f"{evento[2]}")
        self.pdf.cell(50, 10, txt="Nombre del Cliente:", border=0)
        self.pdf.cell(0, 10, txt=f"{evento[3]}", ln=True)
        self.pdf.cell(50, 10, txt="Monto Total Pagado:", border=0)
        self.pdf.cell(0, 10, txt=f"{evento[4]}", ln=True)
        self.pdf.cell(50, 10, txt="Anticipo:", border=0)
        self.pdf.cell(0, 10, txt=f"{evento[5]}", ln=True)
        self.pdf.cell(50, 10, txt="Servicio:", border=0)
        self.pdf.cell(0, 10, txt=f"{evento[6]}", ln=True)

        # Línea separadora
        self.pdf.ln(10)
        self.pdf.line(10, self.pdf.get_y(), 200, self.pdf.get_y())
        self.pdf.ln(10)

        # Texto grande "PAGADO"
        self.pdf.set_font("Arial", style="B", size=50)
        self.pdf.set_text_color(0, 255, 0)
        self.pdf.cell(0, 10, txt="PAGADO", ln=True, align="C")

        # Pie de página
        self.pdf.set_y(-30)
        self.pdf.set_font("Arial", size=10)
        self.pdf.cell(0, 10, txt="Gracias por confiar en Eventify.", ln=True, align="C")
        self.pdf.image("logoEven.png", x=10, y=self.pdf.get_y() - 20, w=33)

        # Guardar el PDF
        self._guardar_pdf()

    def _guardar_pdf(self):
        # Verificar y crear el directorio si es necesario
        directorio = os.path.dirname(self.nombre_archivo)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)

        # Guardar el PDF
        self.pdf.output(self.nombre_archivo, "F")

        # Verificar si el archivo se ha guardado correctamente antes de abrirlo
        if os.path.exists(self.nombre_archivo):
            os.startfile(self.nombre_archivo)
            print(f"PDF generado y guardado como: {self.nombre_archivo}")
        else:
            print(f"Error: No se pudo guardar el archivo PDF en {self.nombre_archivo}")