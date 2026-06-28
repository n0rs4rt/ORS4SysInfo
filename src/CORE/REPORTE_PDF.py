import logging
from datetime import datetime
from fpdf import FPDF
from CORE.RUTAS import *

logger = logging.getLogger("logs")

class Reporte_PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.alias_nb_pages()
        self.azul_ocuro = (31, 47, 79)
        self.gris = (36, 36, 36)
        self.blanco = (255, 255, 255)
        self.add_font("DejaVuSans", "", fuente_texto)
        self.add_font("DejaVuSans", "B", fuente_texto_B)
        


    def procesador_datos_reporte_individual (self, datos_equipo):

        self.nombre_personalizado = datos_equipo[0]["custom_name"]
        self.hostname = datos_equipo[0]["hostname"]
        self.modelo = datos_equipo[0]["modelo"]
        self.fabricante_bios = datos_equipo[0]["fabricante_bios"]
        self.serial_bios = datos_equipo[0]["serial_bios"]
        if len(self.serial_bios) > 30:
            self.serial_bios = self.serial_bios[-30:]
        
        self.bios_version = datos_equipo[0]["bios_version"]
        if len(self.bios_version) > 50:
            self.bios_version = self.bios_version[:50]
        
        self.serial_motherboard = datos_equipo[0]["serial_motherboard"]
        self.modelo_motherboard = datos_equipo[0]["modelo_motherboard"]
        self.version_motherboard = datos_equipo[0]["version_motherboard"]
        self.procesador = datos_equipo[0]["procesador"]
        self.sistema_operativo = datos_equipo[0]["sistema_operativo"]
        self.licencia_os = datos_equipo[0]["licencia"]
        self.zona_horaria = datos_equipo[0]["zona_horaria"]
        self.idioma = datos_equipo[0]["idioma"]
        self.dominio_grupo = datos_equipo[0]["dominio_grupo_trabajo"]
        self.notas = datos_equipo[0]["notas_equipo"]
        self.fecha_registro = f"{datos_equipo[0]["fecha_registro"]} {datos_equipo[0]['hora_registro']}"
        self.memoria_total = 0
        

        self.usuarios = datos_equipo[1]
        self.discos = datos_equipo[2]
        self.memorias = datos_equipo[3]
        
        try:

            for memoria in self.memorias:
                self.memoria_total += float(memoria["capacidad"])

        except Exception as e:
            logger.error(f"Error al obtener la memoria total: {str(e)}")
        
        self.adaptador = datos_equipo[4]
        self.gpus = datos_equipo[5]
        
    def header (self):
        if self.page_no() == 1:
            self.set_font ("DejaVuSans","B",16)
            self.set_text_color(*self.azul_ocuro)
            self.cell(0,10, "REPORTE DE INVENTARIO TECNICO", ln=True, align="C")
            self.ln(4)

    def footer (self):
        self.set_y(-15)
        self.set_font ("DejaVuSans","",6)
        self.set_text_color(199, 199, 199)
        self.cell (55,5,f"Generado con ORS4Sysinfo - Inventario Tecnico",align="L")
        self.set_font ("DejaVuSans","",8)
        self.set_text_color(*self.azul_ocuro)
        self.cell (0,5,f"Pagina {self.page_no()} de {{nb}}" , ln=True, align="R")
        
    def generar_reporte (self):
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M") #fecha actual del reporte
        titulos = ("DejaVuSans","B",10) #formato de los titulos
        subtitulos = ("DejaVuSans","B",8) #formato de los subtitulos
        texto = ("DejaVuSans", "", 8) #formato del texto
        
        self.add_page()
        self.set_font(*subtitulos)
        self.set_text_color(*self.azul_ocuro)
        self.cell(60,5,"Equipo:",  align="L")
        self.set_font(*texto)
        self.set_text_color (*self.gris)
        self.cell(40,5,f"{self.nombre_personalizado}",align="L")
        self.ln(5)
        
        self.set_font (*subtitulos)
        self.set_text_color(*self.azul_ocuro)
        self.cell (60,5, "Host/Nombre del equipo:", align="L")
        self.set_font(*texto)
        self.set_text_color (*self.gris)
        self.cell(0,5,f"{self.hostname}", align="L")
        self.ln(5)

        self.set_font (*subtitulos)
        self.set_text_color(*self.azul_ocuro)
        self.cell(60,5,"Fecha del analisis:",  align="L")
        self.set_font (*texto)
        self.set_text_color (*self.gris)
        self.cell(0,5,f"{self.fecha_registro}", align="L")
        self.ln(5)
        
        self.set_font (*subtitulos)
        self.set_text_color(*self.azul_ocuro)
        self.cell(60,5,"Fecha de generacion del reporte:",  align="L")
        self.set_font (*texto)
        self.set_text_color (*self.gris)
        self.cell(0,5,f"{fecha}", ln=True, align="L")
        self.ln(3)
        
        #informacion general
        self.set_font (*titulos)
        self.set_text_color(*self.blanco)
        self.set_fill_color(*self.azul_ocuro)
        self.cell (0,6, "1. INFORMACION GENERAL", ln=True, align="L", fill=True)
        self.ln(3)
        
        self.set_font(*subtitulos)
        self.set_text_color(*self.azul_ocuro)
        self.cell (32,5, "Modelo:",align="L")
        self.set_font(*texto)
        self.set_text_color (*self.gris)
        self.cell(55,5,f"{self.modelo}", align="L")
        
        self.set_font(*subtitulos)
        self.set_text_color(*self.azul_ocuro)
        self.cell (25,5, "Procesador:", align="L")
        self.set_font(*texto)
        self.set_text_color (*self.gris)
        self.cell(0,5,f"{self.procesador}", align="L")
        self.ln(5)

        self.set_font(*subtitulos)
        self.set_text_color(*self.azul_ocuro)
        self.cell (32,5, "Sistema operativo:", align="L")
        self.set_font(*texto)
        self.set_text_color (*self.gris)
        self.cell(55,5,f"{self.sistema_operativo}", align="L")

        self.set_font(*subtitulos)
        self.set_text_color(*self.azul_ocuro)
        self.cell (25,5, "Memoria RAM:", align="L")
        self.set_font(*texto)
        self.set_text_color (*self.gris)
        self.cell(0,5,f"{self.memoria_total:.1f} GB",align="L")
        self.ln(5)

        self.set_font(*subtitulos)
        self.set_text_color(*self.azul_ocuro)
        self.cell (32,5, "Idioma:", align="L")
        self.set_font(*texto)
        self.set_text_color (*self.gris)
        self.cell(55,5,f"{self.idioma}", align="L")

        self.set_font(*subtitulos)
        self.set_text_color(*self.azul_ocuro)
        self.cell (25,5, "Zona horaria:", align="L")
        self.set_font(*texto)
        self.set_text_color (*self.gris)
        self.cell(0,5,f"{self.zona_horaria}",align="L")
        self.ln(5)

        self.set_font(*subtitulos)
        self.set_text_color(*self.azul_ocuro)
        self.cell (32,5, "Dominio/Grupo:", align="L")
        self.set_font(*texto)
        self.set_text_color (*self.gris)
        self.cell(55,5,f"{self.dominio_grupo}", align="L")

        self.set_font(*subtitulos)
        self.set_text_color(*self.azul_ocuro)
        self.cell (25,5, "Lic. Windows:",align="L")
        self.set_font(*texto)
        self.set_text_color (*self.gris)
        self.cell(0,5,f"{self.licencia_os} - Ultimos digitos", ln=True, align="L")
        self.ln(3)

        #informacion bios y placa base
        self.set_font(*titulos)
        self.set_text_color(*self.blanco)
        self.set_fill_color(*self.azul_ocuro)
        self.cell (0,6, "2. BIOS Y PLACA BASE", ln=True, align="L", fill=True)
        self.ln(3)

        self.set_font(*subtitulos)
        self.set_text_color(*self.azul_ocuro)
        self.cell (28,5, "Fabricante Bios:", align="L")
        self.set_font(*texto)
        self.set_text_color (*self.gris)
        self.cell(90,5,f"{self.fabricante_bios}", align="L")

        self.set_font(*subtitulos)
        self.set_text_color(*self.azul_ocuro)
        self.cell (26,5, "Serial Bios:", align="L")
        self.set_font(*texto)
        self.set_text_color (*self.gris)
        self.cell(0,5,f"{self.serial_bios}", align="L")
        self.ln(5)

        self.set_font(*subtitulos)
        self.set_text_color(*self.azul_ocuro)
        self.cell (28,5, "Version Bios:", align="L")
        self.set_font(*texto)
        self.set_text_color (*self.gris)
        self.cell(90,5,f"{self.bios_version}",align="L")

        self.set_font(*subtitulos)
        self.set_text_color(*self.azul_ocuro)
        self.cell (26,5, "Serial Placa B:", align="L")
        self.set_font(*texto)
        self.set_text_color (*self.gris)
        self.cell(0,5,f"{self.serial_motherboard}", align="L")
        self.ln(5)

        self.set_font(*subtitulos)
        self.set_text_color(*self.azul_ocuro)
        self.cell (28,5, "Placa Base:", align="L")
        self.set_font(*texto)
        self.set_text_color (*self.gris)
        self.cell(90,5,f"{self.modelo_motherboard}", align="L")

        self.set_font(*subtitulos)
        self.set_text_color(*self.azul_ocuro)
        self.cell (26,5, "Vers. Placa B:", align="L")
        self.set_font(*texto)
        self.set_text_color (*self.gris)
        self.cell(0,5,f"{self.version_motherboard}", ln=True, align="L")
        self.ln(3)
        
        #informacion usuarios registrados
        self.set_font(*titulos)
        self.set_text_color(*self.blanco)
        self.set_fill_color(*self.azul_ocuro)
        self.cell (0,6, "3. CUENTAS DE USUARIO", ln=True, align="L", fill=True)
        self.ln(3)
        
        for user in self.usuarios:
            self.set_font(*subtitulos)
            self.set_text_color(*self.azul_ocuro)
            self.cell (15,5, "Usuario:", align="L")
            self.set_font(*texto)
            self.set_text_color (*self.gris)
            self.cell(55,5, f"{user["nombre"]}", align="L")
            
            self.set_font(*subtitulos)
            self.set_text_color(*self.azul_ocuro)
            self.cell (25,5, "Tipo de cuenta:", align="L")
            self.set_font(*texto)
            self.set_text_color (*self.gris)
            self.cell(0,5, f"{user['tipo']}", align="L")
            self.ln(5)
        
        self.set_font(*subtitulos)
        self.set_text_color(*self.azul_ocuro)
        self.cell (30,5, "Total de usuarios:", align="L")
        self.set_font(*texto)
        self.set_text_color (*self.gris)
        self.cell(0,5, f"{len(self.usuarios)}", ln=True, align="L")
        self.ln(3)
        
        #informacion memorias
        self.set_font(*titulos)
        self.set_text_color(*self.blanco)
        self.set_fill_color(*self.azul_ocuro)
        self.cell (0,6, "4. MEMORIA RAM", ln=True, align="L", fill=True)
        self.ln(3)

        self.set_font(*subtitulos)
        self.set_text_color(*self.azul_ocuro)
        self.cell (5,5, "Nº",  align="C")
        self.cell (23,5, "Tipo", align="C")
        self.cell (19,5, "Capacidad",  align="C")
        self.cell (42,5, "Serial", align="C")
        self.cell (48,5, "Fabricante",  align="C")
        self.cell (0,5, "Part Number",  ln=True, align="C")
        
        i=1
        for mem in self.memorias:
            self.set_font(*texto)
            self.set_text_color (*self.gris)
            self.cell (5,5, f"{i}", align="C")
            self.cell (23,5, f"{mem['tipo']}",  align="C")
            self.cell (19,5, f"{mem['capacidad']} GB",  align="C")
            self.cell (42,5, f"{mem['serial']}",  align="C")
            self.cell (48,5, f"{mem['fabricante']}", align="C")
            self.cell (0,5, f"{mem['partnumber']}",  ln=True, align="C")
            i+=1
        self.ln(3)
        self.set_font(*subtitulos)
        self.set_text_color(*self.azul_ocuro)
        self.cell (33,5, "Total de capacidad:", align="L")
        self.set_font(*texto)
        self.set_text_color (*self.gris)
        self.cell(0,5, f"{self.memoria_total:.2f} GB", ln=True, align="L")
        self.ln(3)

        #informacion discos
        self.set_font(*titulos)
        self.set_text_color(*self.blanco)
        self.set_fill_color(*self.azul_ocuro)
        self.cell (0,6, "5. DISCOS Y ALMACENAMIENTO", ln=True, align="L", fill=True)
        self.ln(3)

        self.set_font(*subtitulos)
        self.set_text_color(*self.azul_ocuro)
        self.cell (5,5, "Nº", align="C")
        self.cell (70,5, "Modelo",align="C")
        self.cell (18,5, "Capacidad", align="C")
        self.cell (45,5, "Serial",align="C")
        self.cell (20,5, "Interfaz", align="C")
        self.cell (0,5, "Fallos criticos", ln=True, align="C")

        i=1
        
        for disco in self.discos:
            serial = disco['serial']
            modelo = disco['modelo']
            
            if len(serial) > 17:
                serial = serial[-17:]
            
            if len(modelo) > 34:
                modelo = modelo[-34:]
            
            self.set_font(*texto)
            self.set_text_color (*self.gris)
            self.cell (5,5, f"{i}", align="C")
            self.cell (70,5, f"{modelo}", align="C")
            self.cell (18,5, f"{disco['capacidad']}", align="C")
            self.cell (45,5, f"{serial}", align="C")
            self.cell (20,5, f"{disco['interfaz']}", align="C")
            self.cell (0,5, f"{disco['fallos_criticos']}", ln=True, align="C")
            i+=1
        self.ln(3)
        self.set_font(*subtitulos)
        self.set_text_color(*self.azul_ocuro)
        self.cell (28,5, "Total de Discos:", align="L")
        self.set_font(*texto)
        self.set_text_color (*self.gris)
        self.cell(0,5, f"{len(self.discos)}", ln=True, align="L")
        self.ln(3)

        #informacion graficas
        self.set_font(*titulos)
        self.set_text_color(*self.blanco)
        self.set_fill_color(*self.azul_ocuro)
        self.cell (0,6, "6. PLACAS GRAFICAS (GPU)", ln=True, align="L", fill=True)
        self.ln(3)

        self.set_font(*subtitulos)
        self.set_text_color(*self.azul_ocuro)
        self.cell (5,5, "Nº",  align="C")
        self.cell (80,5, "Modelo",  align="C")
        self.cell (23,5, "Capacidad", align="C")
        self.cell (0,5, "Fabricante", ln=True, align="C")

        i=1
        for graf in self.gpus:
            self.set_font(*texto)
            self.set_text_color (*self.gris)
            self.cell (5,5, f"{i}", align="C")
            self.cell (80,5, f"{graf['modelo']}", align="C")
            self.cell (23,5, f"{graf['capacidad']}", align="C")
            self.cell (0,5, f"{graf['fabricante']}",ln=True, align="C")
            i+=1
        self.ln(3)
        self.set_font(*subtitulos)
        self.set_text_color(*self.azul_ocuro)
        self.cell (10,5, f"Nota:", align="L")
        self.set_font(*texto)
        self.set_text_color (*self.gris)
        self.multi_cell (0,5, f"En las GPU integradas, una capacidad de 128 MB puede corresponder a la memoria mínima reservada. La memoria total compartida puede variar dinámicamente.", align="L")
        self.ln(5)
        
        #adaptadores red
        self.set_font(*titulos)
        self.set_text_color(*self.blanco)
        self.set_fill_color(*self.azul_ocuro)
        self.cell (0,6, "7. ADAPTADORES DE RED", ln=True, align="L", fill=True)
        self.ln(3)
        self.set_font(*subtitulos)
        self.set_text_color(*self.azul_ocuro)
        self.cell (5,5, "Nº", align="C")
        self.cell (90,5, "Nombre", align="C")
        self.cell (28,5, "Mac Adress",  align="C")
        self.cell (0,5, "Velocidad", ln=True, align="C")
        
        i=1
        for mac in self.adaptador:
            self.set_font(*texto)
            self.set_text_color (*self.gris)
            self.cell (5,5, f"{i}", align="C")
            self.cell (90,5, f"{mac['nombre']}",  align="C")
            self.cell (28,5, f"{mac['mac']}",  align="C")
            self.cell (0,5, f"{mac['velocidad']}", ln=True, align="C")
            i+=1
        self.ln(3)
        self.set_font(*subtitulos)
        self.set_text_color(*self.azul_ocuro)
        self.cell (48,5, f"Total de adaptadores de red:", align="L")
        self.set_font(*texto)
        self.set_text_color (*self.gris)
        self.cell (0,5, f"{len(self.adaptador)}", ln=True, align="L")
        self.ln(3)
        
        #informacion notas
        self.set_font(*titulos)
        self.set_text_color(*self.blanco)
        self.set_fill_color(*self.azul_ocuro)
        self.cell (0,6, "8. NOTAS", ln=True, align="L", fill=True)
        self.ln(3)
        self.set_font(*texto)
        self.set_text_color (*self.gris)
        self.multi_cell (0,5, f"{self.notas}", border = 1, align="L")
    def guardar_pdf (self,ruta_guardar):
        try:
            self.output(ruta_guardar)
            return True
        except Exception as e:
            logger.error(f"Error al guardar el reporte pdf {e}")
            return False
        
    def guardar_pdf_email (self):
        ruta_pdf = ruta_tmp / f"Reporte_{self.nombre_personalizado}_{self.hostname}.pdf"
        nombre = ruta_pdf.name
        
        try:
            self.output(ruta_pdf)
            tamano = ruta_pdf.stat().st_size / 1024
            
            return (ruta_pdf,nombre,tamano)
            
        except Exception as e:
            logger.error(f"Error al guardar el reporte pdf {e}")
            return False
