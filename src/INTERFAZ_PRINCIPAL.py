import customtkinter as ctk, threading, pythoncom, tkinter as tk, os, webbrowser
from PIL import Image
from tkinter import filedialog

from CORE.CONFIG_LOGS import config_logging
from CORE.RUTAS import *
from CORE.BASE_DATOS import DB_Equipos
from ESCANEAR import Escanear
from CORE.REPORTE_PDF import Reporte_PDF
from CORE.EMAIL import Email

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

logger = config_logging()

class Interfaz (ctk.CTk):
    def __init__(self):
        super().__init__()

        self.db = DB_Equipos()
        self.db.crear_db()

        self.title ("ORS4SYSINFO")

        self.update_idletasks()

        ancho = 1500
        alto = 800

        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)

        self.geometry(f"{ancho}x{alto}+{x}+{y}")

        self.minsize(ancho, alto)

        self.iconbitmap(ruta_icono)

        self.frame_equipo_seleccionado = None # Variable bandera para almacenar el frame del equipo seleccionado
        self.equipo_detalles_seleccionado = None # Variable bandera para almacenar los detalles del equipo seleccionado y no volver a crear la interfaz si ya esta seleccionado
        
        self.contenedor_principal()
        self.contenedores_secundarios()
        self.widget_frame_header()
        self.frame_contenedor_isquierdo_derecho()
        self.widget_frame_derecho_scanear()

        self.actualizar_interfaz_equipos_registrados()


        self.after(1, lambda: self.state("zoomed")) #maximizamos la ventana al abrir

        self.bind("<Button-1>", self.restaura_nombre_custom_host)
        self.bind("<Button-3>", self.restaura_nombre_custom_host)
        
        self.custom_name_equipos_seleccionado = False
    def contenedor_principal (self):
        """
        Contenedor unico de la interfaz
        """
        self.frame_contenedor = ctk.CTkFrame(self, fg_color="#ffffff")
        self.frame_contenedor.pack(fill="both", expand=True)
        self.frame_contenedor.grid_columnconfigure(0, weight=1)
        self.frame_contenedor.grid_rowconfigure(1, weight=1)

    def contenedores_secundarios (self):
        """
        Contenedores secundarios de la interfaz (equipos registrados, sin registros, equipos)
        """

        self.frame_header = ctk.CTkFrame(self.frame_contenedor,fg_color="transparent")
        self.frame_header.grid(row=0, column=0, sticky="ew")
        self.frame_header.grid_columnconfigure(1, weight=1)

        self.contenedor_equipos = ctk.CTkFrame(self.frame_contenedor,fg_color="transparent") # contenedor de los equipos registrados y de los datos
        self.contenedor_equipos.grid(row=1, column=0, sticky="nsew")
        self.contenedor_equipos.grid_rowconfigure(0, weight=1)
        self.contenedor_equipos.grid_columnconfigure(1, weight=1)

    def widget_frame_header (self):
        """
        widgets del frame header
        """
        frame_logo = ctk.CTkFrame(self.frame_header, fg_color="transparent")
        frame_logo.grid(row=0, column=0, padx=25, pady=5)

        logo = ctk.CTkImage(light_image=Image.open(ruta_logo), dark_image=Image.open(ruta_logo), size=(55, 50))
        label_logo = ctk.CTkLabel(frame_logo, image=logo, text="", fg_color="transparent")
        label_logo.grid(row=0, column=0,rowspan=2)

        label_titulo = ctk.CTkLabel (frame_logo, text="ORS4SysInfo", font=("Arial", 20, "bold"), fg_color="transparent", text_color="#203A6E", anchor="s")
        label_titulo.grid(row=0, column=1, padx=5, sticky="ws")
        label_subtitulo = ctk.CTkLabel (frame_logo, text="Inventario tecnico de equipos", font=("Arial", 12, ), fg_color="transparent", text_color="#1A3D83", anchor="n")
        label_subtitulo.grid(row=1, column=1, padx=5)

        frame_espacio = ctk.CTkFrame(self.frame_header,height=4, fg_color="transparent")
        frame_espacio.grid(row=0, column=1, sticky="ew")

        logo_escanear = ctk.CTkImage(light_image=Image.open(logo_scan), size=(16, 16))
        boton_escanear = ctk.CTkButton(self.frame_header, image = logo_escanear, text = "Escanear equipo", font=("Arial", 12,"bold" ), fg_color="#1477E9",hover_color="#206CC2", text_color="white", width=155, height=36, compound="left", cursor="hand2",border_width=1, border_color="#BAC8D9", corner_radius=4, command=self.escanear_equipo)
        boton_escanear.grid(row=0, column=2, padx=10, sticky="w")

        frame_exportar = ctk.CTkFrame(self.frame_header, fg_color="transparent",border_width=2, border_color="#F5F5F5", corner_radius=4, cursor="hand2")
        frame_exportar.grid(row=0, column=3, padx=10, sticky="w")

        download_logo = ctk.CTkImage(light_image=Image.open(logo_download), size=(20, 16))

        label_logo_download = ctk.CTkLabel(frame_exportar, image=download_logo, text="",cursor="hand2")
        label_logo_download.grid(row=0, column=0, padx=5)
        label_logo_download.bind("<Button-1>", lambda event: self.copia_seguridad._open_dropdown_menu())
        valor_default = ctk.StringVar(value= "Copia de seguridad")

        self.copia_seguridad = ctk.CTkOptionMenu(frame_exportar, variable=valor_default, values=["Exportar", "Importar"], font=("Arial", 12, "bold" ), text_color="#203A6E", fg_color="#FFFFFF", button_color="#FFFFFF", button_hover_color="#FFFFFF", dropdown_fg_color="#FFFFFF", dropdown_text_color="#203A6E", dropdown_hover_color="#F2F7FB",width=100, corner_radius=6, command=self.menu_copia_seguridad)
        self.copia_seguridad.grid(row=0, column=1, padx=(0,4), pady=4, sticky="w")

        frame_config = ctk.CTkFrame(self.frame_header, fg_color="transparent",border_width=2, border_color="#F5F5F5", corner_radius=4)
        frame_config.grid(row=0, column=4, padx=(10,35), sticky="w")
        logo_config = ctk.CTkImage(light_image=Image.open(logo_configuracion), size=(18, 18))
        label_config = ctk.CTkLabel(frame_config, image=logo_config, text="", cursor="hand2")
        label_config.grid(row=0, column=0, padx=(10,0), pady=3, sticky="w")
        label_config.bind("<Button-1>", lambda event: self.menu_op._open_dropdown_menu())
        frame_config.grid_columnconfigure(1, weight=1)
        
        valor = ctk.StringVar(value= "")

        self.menu_op = ctk.CTkOptionMenu(frame_config, variable=valor, values=["Configurar Correo (SMTP)", "Acerca de Ors4SysInfo"], font=("Arial", 12, "bold" ), text_color="#203A6E", fg_color="#FFFFFF", button_color="#FFFFFF", button_hover_color="#FFFFFF", dropdown_fg_color="#FFFFFF", dropdown_text_color="#203A6E",width=5, dropdown_hover_color="#F2F7FB", corner_radius=6, command=self.menu_config)
        self.menu_op.grid(row=0, column=1, padx=(0,4), pady=4, sticky="w")

    def frame_contenedor_isquierdo_derecho (self):
        """
        frame contenedor de equipos registrados
        """

        #FRAME LATERAL IZQUIERDO QUE CONTIENE EL FRAME CON SCROLL DE TODOS LOS EQUIPOS REGISTRADOS
        self.frame_registros_equipos = ctk.CTkFrame(self.contenedor_equipos,fg_color="transparent", corner_radius=6, border_width=2, border_color="#F5F5F5")
        self.frame_registros_equipos.grid(row=0, column=0, sticky="ns", padx=(10,5), pady=5)
        self.frame_registros_equipos.grid_columnconfigure(0, weight=1)
        self.frame_registros_equipos.grid_rowconfigure(2, weight=1)

        #FRAME DERECHO QUE INDICA QUE CONTIENE LOS WIDGET DE MSJ INICIAL Y ESCANEO
        self.frame_derecho_scanear = ctk.CTkFrame(self.contenedor_equipos,fg_color="transparent", corner_radius=6, border_width=2, border_color="#F5F5F5")
        self.frame_derecho_scanear.grid(row=0, column=1, sticky="nsew", padx=(5,10), pady=5)
        self.frame_derecho_scanear.grid_columnconfigure(0, weight=1)
        self.frame_derecho_scanear.grid_rowconfigure(0, weight=1)
        self.frame_derecho_scanear.grid_rowconfigure(4, weight=1)

    def widget_frame_derecho_scanear (self):
        """
        wiget del frame derecho central
        """

        logo_sin_regis = ctk.CTkImage(light_image=Image.open(logo_sin_registro), size=(320, 230))
        label_sin_registro = ctk.CTkLabel(self.frame_derecho_scanear, image=logo_sin_regis, text="")
        label_sin_registro.grid(row=0, column=0, padx=10, pady=(120,10), sticky="wesn")

        self.titulo_equipos_registrados = ctk.CTkLabel(self.frame_derecho_scanear, text= "No hay equipos registrados", font=("Arial", 22, "bold"), text_color="#203A6E")
        self.titulo_equipos_registrados.grid(row=1, column=0, padx=10, pady=(10,0), sticky="we")

        self.descripcion_equipos_registrados = ctk.CTkLabel(self.frame_derecho_scanear, text= "Escanea un equipo para comenzar a contruir", font=("Arial", 14,), text_color="#203A6E", anchor="s")
        self.descripcion_equipos_registrados.grid(row=2, column=0, padx=10, sticky="we")
        self.descripcion_equipos_registrados2 = ctk.CTkLabel(self.frame_derecho_scanear, text= "tu inventario tecnico", font=("Arial", 14, ), text_color="#203A6E")
        self.descripcion_equipos_registrados2.grid(row=3, column=0, padx=10, sticky="we")

        logo_escanear = ctk.CTkImage(light_image=Image.open(logo_scan), size=(22,22))
        self.boton_escanear = ctk.CTkButton(self.frame_derecho_scanear, image=logo_escanear, text="Escanear primer equipo", font=("Arial", 14, "bold"), compound="left",width=135, height=40, text_color="#FFFFFF",fg_color="#1477E9", hover_color="#206CC2", cursor="hand2", command=self.escanear_equipo)
        self.boton_escanear.grid(row=4, column=0, padx=10, pady=10)

        #frame para los detalles (escanea, guarda, organiza)
        frame_detalles = ctk.CTkFrame(self.frame_derecho_scanear,fg_color= "transparent")
        frame_detalles.grid(row=5, column=0, padx=25, pady=(0,60), sticky="we")
        frame_detalles.grid_columnconfigure(0, weight=1)
        frame_detalles.grid_columnconfigure(2, weight=1)
        frame_detalles.grid_columnconfigure(4, weight=1)

        frame_escanea = ctk.CTkFrame(frame_detalles,fg_color= "transparent")
        frame_escanea.grid(row=0, column=0, padx=10)

        lupa = ctk.CTkImage(light_image=Image.open(logo_lupa), size=(20, 20))
        label_lupa = ctk.CTkLabel(frame_escanea, image=lupa, text="",anchor="s")
        label_lupa.grid(row=0, column=0,rowspan=3,sticky="n",padx=5)

        label_titulo_esc = ctk.CTkLabel(frame_escanea, text="Escanea", font=("Arial", 13, "bold"), text_color="#203A6E")
        label_titulo_esc.grid(row=0, column=1, padx=5, sticky="ws")
        label_esc_descripcion = ctk.CTkLabel(frame_escanea, text="Obten toda la informacion", font=("Arial", 11.5,), text_color="#203A6E")
        label_esc_descripcion.grid(row=1, column=1, padx=5, sticky="wn")
        label_esc_descripcion_con = ctk.CTkLabel(frame_escanea, text="tecnica necesaria", font=("Arial", 11.5, ), text_color="#203A6E",anchor="n")
        label_esc_descripcion_con.grid(row=2, column=1, padx=5, sticky="wn")

        frame_separador1 = ctk.CTkFrame(frame_detalles, width=2, height=60, fg_color="#BAC8D9")
        frame_separador1.grid(row=0, column=1, padx=10)

        frame_guarda = ctk.CTkFrame(frame_detalles,fg_color= "transparent")
        frame_guarda.grid(row=0, column=2, padx=10)

        registro_logo = ctk.CTkImage (light_image=Image.open(logo_registro), size=(18, 20))
        label_logo_registro = ctk.CTkLabel(frame_guarda, image=registro_logo, text="",anchor="s")
        label_logo_registro.grid(row=0, column=0,rowspan=3,sticky="n",padx=5)

        label_titulo_guar = ctk.CTkLabel(frame_guarda, text="Guarda", font=("Arial", 13, "bold"), text_color="#203A6E")
        label_titulo_guar.grid(row=0, column=1, padx=5, sticky="ws")

        label_descripcion_guar = ctk.CTkLabel (frame_guarda, text="Alamacena los datos de forma", font=("Arial", 11.5,), text_color="#203A6E")
        label_descripcion_guar.grid(row=1, column=1, padx=5, sticky="wn")
        label_descripcion_guar_con = ctk.CTkLabel(frame_guarda, text="local y organizada", font=("Arial", 11.5, ), text_color="#203A6E",anchor="n")
        label_descripcion_guar_con.grid(row=2, column=1, padx=5, sticky="wn")

        frame_separador2 = ctk.CTkFrame(frame_detalles, width=2, height=60, fg_color="#BAC8D9")
        frame_separador2.grid(row=0, column=3, padx=10)

        frame_consulta = ctk.CTkFrame(frame_detalles,fg_color= "transparent")
        frame_consulta.grid(row=0, column=4, padx=10)

        consulta_logo = ctk.CTkImage (light_image=Image.open(logo_consulta), size=(24, 20))

        label_logo_consulta = ctk.CTkLabel(frame_consulta, image=consulta_logo, text="",anchor="s")
        label_logo_consulta.grid(row=0, column=0,rowspan=3,sticky="n",padx=5)

        label_titulo_cons = ctk.CTkLabel(frame_consulta, text="Consulta", font=("Arial", 13, "bold"), text_color="#203A6E")
        label_titulo_cons.grid(row=0, column=1, padx=5, sticky="ws")
        label_cons_descripcion = ctk.CTkLabel(frame_consulta, text="Visualiza hardware, sistema, usuarios", font=("Arial", 11.5,), text_color="#203A6E")
        label_cons_descripcion.grid(row=1, column=1, padx=5, sticky="wn")
        label_cons_descripcion_con = ctk.CTkLabel(frame_consulta, text="y componentes del equipo", font=("Arial", 11.5, ), text_color="#203A6E",anchor="n")
        label_cons_descripcion_con.grid(row=2, column=1, padx=5, sticky="wn")

    def actualizar_interfaz_equipos_registrados (self):
        """
        LEE LA CANTIDAD DE EQUIPOS EN LA BASE DE DATOS
        PERMITE LA BUSQUEDA Y LLAMA A LOS METODOS QUE CREAN LOS WIDGETS
        """
        if hasattr (self, "label_equipos_registrados") and self.label_equipos_registrados.winfo_exists(): #si el label ya estaba creado lo destruimos para actualizarlo nuevamente
            self.label_equipos_registrados.destroy()

        n = self.db.cantidad_equipos()
        self.label_equipos_registrados = ctk.CTkLabel(self.frame_registros_equipos, text=f"Equipos registrados: ({n}) ", font=("Arial", 14, "bold"), text_color="#203A6E", anchor="w")
        self.label_equipos_registrados.grid(row=0, column=0, padx=10, pady=10, sticky="we")
        self.label_equipos_registrados.grid_columnconfigure(0, weight=1)
        
        #contenedor buscar
        frame_busqueda = ctk.CTkFrame(self.frame_registros_equipos, fg_color="transparent", border_width=1, border_color="#E2E5E7")
        frame_busqueda.grid(row=1, column=0, padx=10, sticky="we")
        frame_busqueda.grid_columnconfigure(0, weight=1)
        
        self.entry_buscar = ctk.CTkEntry(frame_busqueda, placeholder_text="Buscar equipo", font=("Arial", 13), text_color="#203A6E",border_width=0, fg_color="transparent")
        self.entry_buscar.grid(row=0, column=0, padx=10, sticky="we")
        logo_buscar = ctk.CTkImage(Image.open(logo_busqueda), size=(13, 13))
        label_buscar = ctk.CTkLabel(frame_busqueda, image=logo_buscar, text="", font=("Arial", 12), text_color="#203A6E", anchor="w",cursor="hand2")
        label_buscar.grid(row=0, column=1, padx=(0,10), pady=5)
        self.entry_buscar.bind("<Return>",self.buscar_equipos)
        label_buscar.bind("<Button-1>",self.buscar_equipos)
        self.entry_buscar.bind("<Escape>",lambda event: self.focus_set())

        if n:
            self._frame_lista_equipos()
            self.titulo_equipos_registrados.configure(text=f"Selecciona un equipo")
            self.descripcion_equipos_registrados.configure(text="Escanea o selecciona un equipo para ver su información")
            self.descripcion_equipos_registrados2.configure(text="técnica guardada")
            self.boton_escanear.configure(text="Realizar nuevo escaneo")
            return

        
        else:
            #en caso de que no haya equipos registrados porque fueron eliminados entra si el frame de lista ya estaba creado
            if hasattr(self, "frame_lista_equipos") and self.frame_lista_equipos.winfo_exists():
                self.frame_lista_equipos.destroy()
                
                self.titulo_equipos_registrados.configure(text=f"No hay equipos registrados")
                self.descripcion_equipos_registrados.configure(text="Elige un equipo de la lista para ver toda su información")
                self.descripcion_equipos_registrados2.configure(text="tu inventario tecnico")
                self.boton_escanear.configure(text="Escanear primer equipo")
                
                
                #limpio las variables que tienen las referencias de los widgets anbtigos que fueron destruidos
                self.frame_equipo_seleccionado = None
                self.entry_custom_name = None
                self.nombre_custom = None
                self.custom_name_equipos_seleccionado = False
                self.equipo_detalles_seleccionado = None

    def escanear_equipo (self):
        """
        METODO QUE MUESTRA LA VENTANA INTERFAZ DE ESCANEANDO INFORMACION
        """

        self.ventana_escaneo = ctk.CTkToplevel(self)
        ancho = 450
        alto = 250
        self.ventana_escaneo.geometry("400x200")
        self.ventana_escaneo.title("Escaneando equipo")
        x = self.winfo_rootx() + (self.winfo_width() // 2) - (ancho // 2)
        y = self.winfo_rooty() + (self.winfo_height() // 2) - (alto // 2)
        self.ventana_escaneo.geometry(f"{ancho}x{alto}+{x}+{y}")

        self.ventana_escaneo.lift()
        self.ventana_escaneo.grab_set()
        self.ventana_escaneo.configure(fg_color="#FFFFFF")
        self.ventana_escaneo.overrideredirect(True)

        #creo um frame para simular el marco de la ventana
        frame_ventana = ctk.CTkFrame(self.ventana_escaneo, fg_color="#FFFFFF",border_width=2, border_color="#E2E5E7", corner_radius=10)
        frame_ventana.pack(fill="both", expand=True)

        escanear_logo = ctk.CTkImage (light_image=Image.open(logo_escanear), size=(100, 80))
        label_escaneando = ctk.CTkLabel(frame_ventana, image=escanear_logo, text="",anchor="s")
        label_escaneando.pack(pady=10)

        label_escaneando = ctk.CTkLabel(frame_ventana, text="Escaneando equipo", font=("Arial", 18, "bold"), text_color="#203A6E")
        label_escaneando.pack(pady=(10,3))
        label_descripcion = ctk.CTkLabel(frame_ventana, text="Recopilando la informacion del sistema. Esto puede tardar varios segundos...", font=("Arial", 12, ), text_color="#203A6E")
        label_descripcion.pack()

        self.barra_progreso = ctk.CTkProgressBar(frame_ventana, width=300, height=12, mode="indeterminate", fg_color="#BAC8D9",indeterminate_speed=0.5)
        self.barra_progreso.pack(pady=10)
        self.barra_progreso.start()
        threading.Thread(target=self._iniciar_proceso_escaneo).start() #iniciamos el scaneo que tarda en un hilo para que la interfaz no se bloquee

    def _iniciar_proceso_escaneo (self):
        """
        METODO QUE INICIA EL PROCESO DE ESCANEO
        """
        try:
            pythoncom.CoInitialize() #obligatorio iniciarlo para procesos en hilos con wmi
            escanear = Escanear()
            escanear.obtener_datos()
            escanear.guardar_notas_equipo()
            escanear.preparar_datos_db()
            escanear.insertar_datos_db()
            pythoncom.CoUninitialize()
            self.after(0,self._terminar_proceso_escaneo) #cuanto termine llamamos al metodo


        except Exception as e:
            logger.error(f"Error al escanear el equipo: {str(e)}")
            self.after(0,self._terminar_proceso_escaneo())

    def _terminar_proceso_escaneo (self):
        """
        METODO QUE TERMINA EL PROCESO DE ESCANEO
        """
        self.barra_progreso.stop()
        self.ventana_escaneo.destroy()
        # self.equipo_detalles_seleccionado = None #limpiamos la variable
        self.actualizar_interfaz_equipos_registrados() #volvemos a cargar la interfaz para actualizar los equipos

    def _frame_lista_equipos (self, resultado_busqueda = None):
        """
        METODO QUE CREA LA LISTA DE EQUIPOS REGISTRADOS EN UN FRAME SCROLL Y REGISTRA LOS EVENTOS DEL CLICK
        """

        lista_equipos = resultado_busqueda
        
        if hasattr(self, "frame_lista_equipos") and self.frame_lista_equipos.winfo_exists():
            self.frame_lista_equipos.destroy()
            #limpio las variables que tienen las referencias de los widgets antiguos que fueron destruidos
            self.frame_equipo_seleccionado = None
            self.entry_custom_name = None
            self.nombre_custom = None
            self.custom_name_equipos_seleccionado = False

        
        #contenedor de la lista de los equipos registrados
        self.frame_lista_equipos = ctk.CTkScrollableFrame(self.frame_registros_equipos,width=300,fg_color="transparent")
        self.frame_lista_equipos.grid(row=2, column=0, padx=(1,2), pady=10, sticky="ns")
        self.frame_lista_equipos.grid_columnconfigure(0, weight=1)

        if lista_equipos is None:
            lista_equipos = self.db.consultar_nombres_equipos() #UN DICCIONARIO DE LA DB QUE TIENE EL ID DEL EQUIPO EN LA DB, CUSTOM_NAME HOSTNAME ETC
        
        elif lista_equipos == []:
            return
        
        if lista_equipos:
            
            for i,equipo in enumerate(lista_equipos):

                frame_equipo = ctk.CTkFrame(self.frame_lista_equipos, fg_color="#FFFFFF", border_width=1, border_color="#E2E5E7", corner_radius=4,cursor="hand2")
                frame_equipo.grid(row=i, column=0,pady=3, sticky="nsew")
                frame_equipo.grid_columnconfigure(0, weight=1)
                frame_equipo.grid_columnconfigure(1, weight=1)
                frame_equipo.columnconfigure(2, weight=1)
                frame_equipo.es_frame_equipo = True #SOLO PARA DETECTAR EL WIDGET FRAME

                custom_name = equipo['custom_name']
                hostname = equipo['hostname']
                sn_ultimos_digitos = equipo['serial_bios']
                
                equipo_logo = ctk.CTkImage(light_image=Image.open(logo_equipo),size=(25, 25))

                label_logo_equipo = ctk.CTkLabel(frame_equipo, image=equipo_logo, text="",anchor="center", cursor="hand2")
                label_logo_equipo.grid(row=0, column=0,rowspan=3, padx=(2,0), pady=2,sticky="wnes")

                entry_custom_name = ctk.CTkEntry(frame_equipo, font=("Arial", 13, "bold"), text_color="#203A6E", placeholder_text_color="#203A6E", border_width=0, bg_color="transparent", fg_color="transparent", justify = "left")
                entry_custom_name.insert(0, custom_name)
                entry_custom_name.grid(row=0, column=1, pady=(2,0),  sticky="ws")
                entry_custom_name.configure(state="disabled")

                label_hostname = ctk.CTkLabel (frame_equipo, text=hostname[:15], font=("Arial", 12,), text_color="#203A6E", cursor="hand2",anchor="center")
                label_hostname.grid(row=1, column=1, padx=2, sticky="w")
                
                
                label_serial = ctk.CTkLabel (frame_equipo, text=f"SN: {sn_ultimos_digitos[-5:]}", font=("Arial", 12,"bold"), text_color="#203A6E", anchor = "center", cursor="hand2")
                label_serial.grid(row=2, column=1, padx=2,pady=(0,2), sticky="w")

                label_fecha = ctk.CTkLabel (frame_equipo, text=equipo['fecha_registro'], font=("Arial", 13,), text_color="#203A6E", anchor = "center", cursor="hand2")
                label_fecha.grid(row=0, column=2, padx=(0,4),pady=(2,0), sticky="en")

                label_hora = ctk.CTkLabel (frame_equipo, text=equipo['hora_registro'], font=("Arial", 12,), text_color="#203A6E", anchor="n", cursor="hand2")
                label_hora.grid(row=1, column=2, padx=(0,4), pady=(0,2), sticky="en")

                #CREO EL ATRIBUTO id_equipo PARA GUARDAR EL ID DE LA DB CUANDO HAGAN CLICKPODER REALIZAR LA CONSULTA CON EL ID DE LA DB
                frame_equipo.id_equipo = equipo["id_equipo"]

                #CREO EL ATRIBUTO custom_name PARA GUARDAR EL WIDGET label_custom_name PARA QUE SEA ACCESIBLE Y MODIFICABLE
                frame_equipo.custom_name = entry_custom_name

                #CREO LOS BINDS EVENTOS CUANDO CLICKEN EN LOS EQUIPOS
                frame_equipo.bind("<Button-1>", self.obtener_datos_equipo_selecionado)
                label_logo_equipo.bind("<Button-1>", self.obtener_datos_equipo_selecionado)
                entry_custom_name.bind("<Button-1>", self.obtener_datos_equipo_selecionado)
                label_hostname.bind("<Button-1>", self.obtener_datos_equipo_selecionado)
                label_fecha.bind("<Button-1>", self.obtener_datos_equipo_selecionado)
                label_hora.bind("<Button-1>", self.obtener_datos_equipo_selecionado)
                
                
                # self.custom_name_equipos_seleccionado = None #bandera para detectar el click derecho y no duplicarlo 
                
                frame_equipo.bind("<Button-3>", self.menu_click_derecho)
                label_logo_equipo.bind("<Button-3>", self.menu_click_derecho)
                
                entry_custom_name.bind("<Button-3>", self.menu_click_derecho)
                entry_custom_name.bind ("<Escape>", self.restaura_nombre_custom_host)
                entry_custom_name.bind ("<Return>", self.guardar_nombre_custom_host)
                
                label_hostname.bind("<Button-3>", self.menu_click_derecho)
                label_fecha.bind("<Button-3>", self.menu_click_derecho)
                label_hora.bind("<Button-3>", self.menu_click_derecho)
        else:
            self._interfaz_error_cargar_lista_equipos()

    def obtener_datos_equipo_selecionado (self, event):
        """
        METODO QUE MANEJA E IDENTIFICA EL EQUIPO SELECCIONADO Y ENVIA EL ID PARA OBTENER Y MOSTRAR LOS DATOS EN LA DB
        """
        if self.frame_equipo_seleccionado:
            if hasattr(self, "frame_equipo_seleccionado") and self.frame_equipo_seleccionado.winfo_exists():
                self.frame_equipo_seleccionado.configure (fg_color="#FFFFFF",border_width=1,border_color="#E2E5E7", corner_radius=4,)

        try:
            widget = event.widget

            while not hasattr(widget, "es_frame_equipo"):
                widget = widget.master

            widget.configure (fg_color="#EBF8FE",border_width=2, border_color="#85BBFC") #CAMBIAMOS EL COLOR DEL FRAME SELECCION

            id_equipo = widget.id_equipo #obtenemos el id que guardamos en el frame del equipo

            self.frame_equipo_seleccionado = widget

            self.mostrar_datos_equipo_seleccionado(id_equipo) #METODO QUE CONSULTA EN LA DB LOS DATOS DEL EQUIPO


        except Exception as e:
            logger.error(f"Error al obtener el id del equipo lista frame: {str(e)}")
            return

    def mostrar_datos_equipo_seleccionado (self,id_equipo):
        """
        METODO QUE MANEJA E IDENTIFICA EL EQUIPO SELECCIONADO Y ENVIA EL ID PARA OBTENER
        MOSTRAR LOS DATOS EN LA DB
        CREA EL FRAME CONTENEDOR BASE DE LOS DETALLES DE EQUIPO
        """

        if id_equipo == self.equipo_detalles_seleccionado: #self.id_equipo_seleccionado contiene el numero id del equipo seleccionado
            return
        
        equipo = self.db.obtener_datos_equipo(id_equipo) #obtenemos los datos de la db en una tupla
        self.frame_derecho_scanear.grid_remove()#ocultamos el frame de scanear del mensaje inicial para mostrar los detalles del equipo
        
        if hasattr (self, "frame_detalles_tecnicos") and self.frame_detalles_tecnicos.winfo_exists():
            self.frame_detalles_tecnicos.destroy()

        self.frame_detalles_tecnicos = ctk.CTkFrame(self.contenedor_equipos, fg_color="transparent", corner_radius=6, border_width=2, border_color="#F5F5F5")
        self.frame_detalles_tecnicos.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.frame_detalles_tecnicos.grid_columnconfigure(0, weight=1)
        self.frame_detalles_tecnicos.grid_rowconfigure(2, weight=1)
    
        frame_header_detalles_tecnicos = ctk.CTkFrame(self.frame_detalles_tecnicos, fg_color="transparent", corner_radius=6, border_width=0, border_color="#F5F5F5")
        frame_header_detalles_tecnicos.grid(row=0, column=0, sticky="ew", columnspan=2, padx=(5,10), pady=5) #cubre 2 columnas
        frame_header_detalles_tecnicos.grid_columnconfigure(2, weight=1)

        logo_equipo = ctk.CTkImage(light_image=Image.open(logo_equipo2),size=(45, 45))
        label_logo_equipo = ctk.CTkLabel(frame_header_detalles_tecnicos, image=logo_equipo, text="", fg_color="transparent", anchor="center")
        label_logo_equipo.grid(row=0, column=0, rowspan=2, padx=10, pady=10)

        label_custom_name = ctk.CTkLabel(frame_header_detalles_tecnicos, text=equipo[0]["custom_name"], font=("Arial", 14, "bold"), text_color="#203A6E", anchor="s")
        label_custom_name.grid(row=0, column=1, padx=10, pady=(10,0),sticky="w")

        label_hostname = ctk.CTkLabel(frame_header_detalles_tecnicos, text=equipo[0]["hostname"], font=("Arial", 12,), text_color="#203A6E",  anchor="n")
        label_hostname.grid(row=1, column=1, padx=10, pady=(0,10),sticky="w")

        logo_exportar_pdf = ctk.CTkImage(light_image=Image.open(logo_pdf),size=(15, 18))
        boton_exportar_pdf = ctk.CTkButton(frame_header_detalles_tecnicos, image=logo_exportar_pdf, compound="left",text="Exportar PDF", font=("Arial", 12,"bold"), text_color="#203A6E", fg_color="transparent", border_width=1, border_color="#BAC8D9", corner_radius=4, hover_color="#F8F8F8", height=36,cursor="hand2", command= lambda:self.exportar_reporte_pdf(id_equipo)) #Le pasamos el id del equipo para exportar los datos
        boton_exportar_pdf.grid(row=0, column=2, rowspan=2, padx=5, pady=5, sticky="e")
        
        logo_enviar_email = ctk.CTkImage(light_image=Image.open(logo_email),size=(18, 13))
        boton_enviar_email = ctk.CTkButton(frame_header_detalles_tecnicos,image=logo_enviar_email, compound="left",text="Enviar reporte por email", font=("Arial", 12,"bold"), text_color="#203A6E", fg_color="transparent", border_width=1, border_color="#BAC8D9", corner_radius=4, hover_color="#F8F8F8", height=36,cursor="hand2", command= lambda:self._interfaz_reporte_email (id_equipo)) #Le pasamos el id del equipo para enviar los datos
        boton_enviar_email.grid(row=0, column=3, rowspan=2, padx=5, pady=5, sticky="e")
        

        #contenedor que para la informacion generl tecnica
        self.frame_fila1_detalles_tecnicos=ctk.CTkFrame(self.frame_detalles_tecnicos, fg_color="transparent")
        self.frame_fila1_detalles_tecnicos.grid(row=1, column=0, padx=1, sticky="nsew")
        self.frame_fila1_detalles_tecnicos.grid_columnconfigure(0, weight=1)
        self.frame_fila1_detalles_tecnicos.grid_columnconfigure(1, weight=1)

        self.interfaz_informacion_general(equipo[0])#llamamos a la interfaz de informacion general
        self.interfaz_usuarios(equipo[1])#llamamos a la interfaz de usuarios

        # contenedor que para la informacion discos memorias etc
        self.frame_fila2_detalles_tecnicos=ctk.CTkFrame(self.frame_detalles_tecnicos, fg_color="transparent")
        self.frame_fila2_detalles_tecnicos.grid(row=2, column=0, padx=1, sticky="nsew")
        self.frame_fila2_detalles_tecnicos.grid_columnconfigure(0, weight=1)
        self.frame_fila2_detalles_tecnicos.grid_columnconfigure(1, weight=1)
        self.frame_fila2_detalles_tecnicos.grid_columnconfigure(2, weight=1)
        self.frame_fila2_detalles_tecnicos.grid_columnconfigure(3, weight=1)
        self.frame_fila2_detalles_tecnicos.grid_rowconfigure(1, weight=1)

        self.interfaz_discos(equipo[2])#llamamos a la interfaz de discos
        self.interfaz_memoria(equipo[3])#llamamos a la interfaz de memorias ram
        self.interfaz_adaptador_red(equipo[4])
        self.interfaz_GPUs(equipo[5])
        self.interfaz_notas(equipo[0]["notas_equipo"],id_equipo)
        
        #creamos y guardamos el id del equipo seleccionado para compararlo al inicio de este metodo para no volver a cargar la interfaz caso que este cargada
        self.equipo_detalles_seleccionado = id_equipo 

    def interfaz_informacion_general (self,informacion_general):
        """
        muestra todos los elementos del contenedor informacion general
        """

        nombre_host = informacion_general["hostname"]
        modelo = informacion_general["modelo"]
        fabricante_bios = informacion_general["fabricante_bios"]
        serial_bios = informacion_general["serial_bios"]
        bios_version = informacion_general["bios_version"]
        serial_placa_madre = informacion_general["serial_motherboard"]
        modelo_placa_madre = informacion_general["modelo_motherboard"]
        version_placa_madre = informacion_general["version_motherboard"]
        procesador = informacion_general["procesador"]
        licencia = informacion_general["licencia"]
        sistema_operativo = informacion_general["sistema_operativo"]
        zona_horaria = informacion_general["zona_horaria"]
        idioma = informacion_general["idioma"]
        dominio_grupo_trabajo = informacion_general["dominio_grupo_trabajo"]

        #contenedor de toda la informacion general
        frame_informacion_general = ctk.CTkFrame(self.frame_fila1_detalles_tecnicos, fg_color="#FAFDFF", corner_radius=6, border_width=2, border_color="#F5F5F5")
        frame_informacion_general.grid(row=1, column=0, padx=(15,0), sticky="we") #cubre 2 columnas

        #contenedor derecho
        contenedor_izquierdo = ctk.CTkFrame(frame_informacion_general, fg_color="transparent")
        contenedor_izquierdo.grid(row=0, column=0, padx=(5,10),pady=5, sticky="weswn")

        logo_signo = ctk.CTkImage(light_image=Image.open(logo_exclamacion),size=(20, 20))
        label_logo_signo = ctk.CTkLabel(contenedor_izquierdo, image=logo_signo, text="", fg_color="transparent", anchor="center")
        label_logo_signo.grid(row=0, column=0, padx=10, pady=10)

        label_informacion = ctk.CTkLabel(contenedor_izquierdo, text="Informacion general", font=("Arial", 12, "bold"), text_color="#203A6E", anchor="center")
        label_informacion.grid(row=0, column=1, padx=(0,10),sticky="w")

        logo_host = ctk.CTkImage(light_image=Image.open(logo_equipo),size=(15, 15))
        label_logo_host = ctk.CTkLabel(contenedor_izquierdo, image=logo_host, text="", fg_color="transparent", anchor="center")
        label_logo_host.grid(row=1, column=0, padx=10, pady=5)

        label_hostname = ctk.CTkLabel(contenedor_izquierdo, text=f"Nombre del equipo:", font=("Arial", 12,), text_color="#203A6E",anchor="center")
        label_hostname.grid(row=1, column=1, padx=(0,10),sticky="w")

        hostname = ctk.CTkLabel(contenedor_izquierdo, text=nombre_host, font=("Arial", 12,"bold"), text_color="#2C4371",anchor="center")
        hostname.grid(row=1, column=2, padx=(0,10),sticky="w")

        modelo_logo = ctk.CTkImage(light_image=Image.open(logo_modelo),size=(15, 12))
        label_modelo_logo = ctk.CTkLabel(contenedor_izquierdo, image=modelo_logo, text="", fg_color="transparent", anchor="center")
        label_modelo_logo.grid(row=2, column=0, padx=10, )

        label_modelo = ctk.CTkLabel(contenedor_izquierdo, text="Modelo:", font=("Arial", 12,), text_color="#203A6E",anchor="center")
        label_modelo.grid(row=2, column=1, padx=(0,10),sticky="w")

        modelo_pc = ctk.CTkLabel(contenedor_izquierdo, text=modelo, font=("Arial", 12,"bold"), text_color="#2C4371",anchor="center")
        modelo_pc.grid(row=2, column=2, padx=(0,10),sticky="w")

        logo_sistema = ctk.CTkImage(light_image=Image.open(logo_sistema_operativo),size=(14, 12))
        label_sistema_logo = ctk.CTkLabel(contenedor_izquierdo, image=logo_sistema, text="", fg_color="transparent", anchor="center")
        label_sistema_logo.grid(row=3, column=0, padx=10, )

        label_sistema = ctk.CTkLabel(contenedor_izquierdo, text="Sistema operativo:", font=("Arial", 12,), text_color="#203A6E",anchor="center")
        label_sistema.grid(row=3, column=1, padx=(0,10),sticky="w")

        sistema_op = ctk.CTkLabel(contenedor_izquierdo, text=sistema_operativo, font=("Arial", 12,"bold"), text_color="#2C4371",anchor="center")
        sistema_op.grid(row=3, column=2, padx=(0,10),sticky="w")

        idioma_logo = ctk.CTkImage (light_image=Image.open(logo_idioma),size=(15, 15))
        label_idioma_logo = ctk.CTkLabel(contenedor_izquierdo, image=idioma_logo, text="", fg_color="transparent", anchor="center")
        label_idioma_logo.grid(row=4, column=0, padx=10, )

        label_idioma = ctk.CTkLabel(contenedor_izquierdo, text="Idioma:", font=("Arial", 12,), text_color="#203A6E",anchor="center")
        label_idioma.grid(row=4, column=1, padx=(0,10),sticky="w")

        idioma_pc = ctk.CTkLabel(contenedor_izquierdo, text=idioma, font=("Arial", 12,"bold"), text_color="#2C4371",anchor="center")
        idioma_pc.grid(row=4, column=2, padx=(0,10),sticky="w")
        zona_h_logo = ctk.CTkImage (light_image=Image.open(logo_zona_horaria),size=(15, 15))
        label_logo_zona_h = ctk.CTkLabel(contenedor_izquierdo, image=zona_h_logo, text="", fg_color="transparent", anchor="center")
        label_logo_zona_h.grid(row=5, column=0, padx=10 )

        label_zona_h = ctk.CTkLabel(contenedor_izquierdo, text="Zona horaria:", font=("Arial", 12,), text_color="#203A6E",anchor="center")
        label_zona_h.grid(row=5, column=1, padx=(0,10),sticky="w")

        zona_h_pc = ctk.CTkLabel(contenedor_izquierdo, text=zona_horaria, font=("Arial", 12,"bold"), text_color="#2C4371",anchor="center")
        zona_h_pc.grid(row=5, column=2, padx=(0,10),sticky="w")

        dominio_logo = ctk.CTkImage (light_image=Image.open(logo_dominio),size=(15, 15))
        label_dominio_logo = ctk.CTkLabel(contenedor_izquierdo, image=dominio_logo, text="", fg_color="transparent", anchor="center")
        label_dominio_logo.grid(row=6, column=0, padx=10, )

        label_dominio = ctk.CTkLabel(contenedor_izquierdo, text="Dominio:", font=("Arial", 12,), text_color="#203A6E",anchor="center")
        label_dominio.grid(row=6, column=1, padx=(0,10),sticky="w")

        dominio_pc = ctk.CTkLabel(contenedor_izquierdo, text=dominio_grupo_trabajo, font=("Arial", 12,"bold"), text_color="#2C4371",anchor="center")
        dominio_pc.grid(row=6, column=2, padx=(0,10),sticky="w")

        licencia_logo = ctk.CTkImage(light_image=Image.open(logo_key),size=(18, 11))
        label_licencia_logo = ctk.CTkLabel(contenedor_izquierdo, image=licencia_logo, text="", fg_color="transparent", anchor="center")
        label_licencia_logo.grid(row=7, column=0, padx=10, )

        label_licencia = ctk.CTkLabel(contenedor_izquierdo, text="Licencia de Windows:", font=("Arial", 12,), text_color="#203A6E",anchor="center")
        label_licencia.grid(row=7, column=1, padx=(0,10),sticky="w")

        licencia_pc = ctk.CTkLabel(contenedor_izquierdo, text=licencia, font=("Arial", 12,"bold"), text_color="#2C4371",anchor="center")
        licencia_pc.grid(row=7, column=2, padx=(0,10),sticky="w")

        #linea separadora
        fame_separador = ctk.CTkFrame(frame_informacion_general,fg_color="#BAC8D9", width=2,)
        fame_separador.grid(row=0, column=1, rowspan=7, padx=10, pady=10, sticky="ns")

        #contenedor_derecho
        contenedor_derecho = ctk.CTkFrame(frame_informacion_general, fg_color="transparent")
        contenedor_derecho.grid(row=0, column=2, padx=(0,10),pady=5, sticky="wesn")

        fabricante_logo = ctk.CTkImage(light_image=Image.open(logo_fabricante),size=(15, 15))
        label_fabricante_logo = ctk.CTkLabel(contenedor_derecho, image=fabricante_logo, text="", fg_color="transparent", anchor="center")
        label_fabricante_logo.grid(row=0, column=0, padx=10, )

        label_fabricante = ctk.CTkLabel(contenedor_derecho, text="Fabricante BIOS:", font=("Arial", 12,), text_color="#203A6E",anchor="center")
        label_fabricante.grid(row=0, column=1, padx=(0,10),sticky="wns")

        fabricante_bios_pc = ctk.CTkLabel(contenedor_derecho, text=fabricante_bios, font=("Arial", 12,"bold"), text_color="#2C4371",wraplength=200,anchor="center")
        fabricante_bios_pc.grid(row=0, column=2, padx=(0,10),pady=10,sticky="w")

        bios_version_logo = ctk.CTkImage(light_image=Image.open(logo_bios_version),size=(19, 18))
        label_bios_version_logo = ctk.CTkLabel(contenedor_derecho, image=bios_version_logo, text="", fg_color="transparent", anchor="center")
        label_bios_version_logo.grid(row=1, column=0, padx=10, )

        label_bios_version = ctk.CTkLabel(contenedor_derecho, text="Version BIOS:", font=("Arial", 12,), text_color="#203A6E",anchor="center")
        label_bios_version.grid(row=1, column=1, padx=(0,10),sticky="w")

        bios_version_pc = ctk.CTkLabel(contenedor_derecho, text=bios_version, font=("Arial", 12,"bold"), text_color="#2C4371", wraplength=200, anchor="center")
        bios_version_pc.grid(row=1, column=2, padx=(0,10),sticky="w")

        serial_bios_logo = ctk.CTkImage(light_image=Image.open(logo_bios_version),size=(19, 18))
        label_serial_bios_logo = ctk.CTkLabel(contenedor_derecho, image=serial_bios_logo, text="", fg_color="transparent", anchor="center")
        label_serial_bios_logo.grid(row=2, column=0, padx=10, )

        label_serial_bios = ctk.CTkLabel(contenedor_derecho, text="Serial BIOS:", font=("Arial", 12,), text_color="#203A6E",anchor="center")
        label_serial_bios.grid(row=2, column=1, padx=(0,10),sticky="w")

        serial_bios_pc = ctk.CTkLabel(contenedor_derecho, text=serial_bios, font=("Arial", 12,"bold"), text_color="#2C4371",anchor="center")
        serial_bios_pc.grid(row=2, column=2, padx=(0,10),sticky="w")

        logo_motherboard = ctk.CTkImage (light_image=Image.open(logo_placa),size=(18, 15))
        label_motherboard_logo = ctk.CTkLabel(contenedor_derecho, image=logo_motherboard, text="", fg_color="transparent", anchor="center")
        label_motherboard_logo.grid(row=3, column=0, padx=10, )

        label_motherboard = ctk.CTkLabel (contenedor_derecho, text="Placa madre:", font=("Arial", 12,), text_color="#203A6E",anchor="center")
        label_motherboard.grid(row=3, column=1, padx=(0,10),sticky="w")

        placa_motherboard_pc = ctk.CTkLabel(contenedor_derecho, text=modelo_placa_madre, font=("Arial", 12,"bold"), text_color="#2C4371",anchor="center")
        placa_motherboard_pc.grid(row=3, column=2, padx=(0,10),sticky="w")

        logo_serial_motherboard = ctk.CTkImage(light_image=Image.open(logo_serial_placa),size=(19, 15))
        label_logo_serial_motherboard = ctk.CTkLabel(contenedor_derecho, image=logo_serial_motherboard, text="", fg_color="transparent", anchor="center")
        label_logo_serial_motherboard.grid(row=4, column=0, padx=10, )

        label_serial_motherboard = ctk.CTkLabel(contenedor_derecho, text="Serial placa base:", font=("Arial", 12,), text_color="#203A6E",anchor="center")
        label_serial_motherboard.grid(row=4, column=1, padx=(0,10),sticky="w")

        serial_motherboard_pc = ctk.CTkLabel(contenedor_derecho, text=serial_placa_madre, font=("Arial", 12,"bold"), text_color="#2C4371",anchor="center")
        serial_motherboard_pc.grid(row=4, column=2, padx=(0,10),sticky="w")

        version_placa_logo = ctk.CTkImage(light_image=Image.open(logo_version_placa),size=(18, 14))
        label_version_placa_logo = ctk.CTkLabel(contenedor_derecho, image=version_placa_logo, text="", fg_color="transparent", anchor="center")
        label_version_placa_logo.grid(row=5, column=0, padx=10, )

        label_version_placa = ctk.CTkLabel(contenedor_derecho, text="Version placa base:", font=("Arial", 12,), text_color="#203A6E",anchor="center")
        label_version_placa.grid(row=5, column=1, padx=(0,10),sticky="w")

        version_placa_pc = ctk.CTkLabel(contenedor_derecho, text=version_placa_madre, font=("Arial", 12,"bold"), text_color="#2C4371",anchor="center")
        version_placa_pc.grid(row=5, column=2, padx=(0,10),sticky="w")

        procesador_logo = ctk.CTkImage(light_image=Image.open(logo_procesador),size=(18, 17))
        label_procesador_logo = ctk.CTkLabel(contenedor_derecho, image=procesador_logo, text="", fg_color="transparent", anchor="center")
        label_procesador_logo.grid(row=6, column=0, padx=10, )

        label_procesador = ctk.CTkLabel(contenedor_derecho, text="Procesador:", font=("Arial", 12,), text_color="#203A6E",anchor="center")
        label_procesador.grid(row=6, column=1, padx=(0,10),sticky="w")

        procesador_pc = ctk.CTkLabel(contenedor_derecho, text=procesador, font=("Arial", 12,"bold"), text_color="#2C4371",anchor="center",wraplength=200 )
        procesador_pc.grid(row=6, column=2, padx=(0,10),sticky="w")

    def interfaz_usuarios (self, usuarios):
        """
        METODO QUE CREA EL FRAME DE USUARIOS EN EL FRAME DE DETALLES TECNICOS
        """

        contenedor_usuarios = ctk.CTkFrame(self.frame_fila1_detalles_tecnicos,fg_color="#FAFDFF", corner_radius=6, border_width=2, border_color="#F5F5F5")
        contenedor_usuarios.grid(row=1, column=1, padx=(5,15), sticky="nsew")
        contenedor_usuarios.grid_rowconfigure(0, weight=1)
        contenedor_usuarios.grid_columnconfigure(1, weight=1)

        usuarios_logo = ctk.CTkImage(light_image=Image.open(logo_usuarios),size=(20, 15))
        label_usuario_logo = ctk.CTkLabel(contenedor_usuarios, image=usuarios_logo, text="", fg_color="transparent", anchor="center")
        label_usuario_logo.grid(row=0, column=0,padx=10, sticky="w")

        label_cantidad_user = ctk.CTkLabel(contenedor_usuarios, text=f"Usuarios registrados ({len(usuarios)})", font=("Arial", 12,"bold"), text_color="#203A6E",anchor="w")
        label_cantidad_user.grid(row=0, column=1, sticky="w")

        fame_lista_usuarios = ctk.CTkScrollableFrame(contenedor_usuarios, fg_color="transparent")
        fame_lista_usuarios.grid(row=1, column=0, padx=2, pady=2, columnspan=2, sticky="ewsn")


        for i, user in enumerate(usuarios):

            frame_usuario = ctk.CTkFrame(fame_lista_usuarios,fg_color= "#F1F8F8", corner_radius=6, border_width=2, border_color="#E1F8F8")
            frame_usuario.grid(row=(i+1), column=0, columnspan=3, padx=2, pady=2, sticky="we")


            usuario_logo = ctk.CTkImage(light_image=Image.open(logo_usuario),size=(30, 30))
            label_usuario_logo = ctk.CTkLabel(frame_usuario, image=usuario_logo, text="", fg_color="transparent", anchor="center")
            label_usuario_logo.grid(row=0, column=0, padx=5, pady=2, rowspan=2, sticky="w")

            label_usuario = ctk.CTkLabel(frame_usuario, text="Usuario:", font=("Arial", 12,), text_color="#2C4371",anchor="s")
            label_usuario.grid(row=0, column=1, padx=5,sticky="w")

            usuario = ctk.CTkLabel(frame_usuario, text=user["nombre"], font=("Arial", 12,"bold"), text_color="#2C4371",anchor="s",wraplength=110)
            usuario.grid(row=0, column=2, padx=5, pady=2,sticky="w")

            label_tipo = ctk.CTkLabel(frame_usuario, text="Tipo:", font=("Arial", 12,), text_color="#2C4371",anchor="n")
            label_tipo.grid(row=1, column=1, padx=5, pady=2,sticky="w")

            tipo_user = ctk.CTkLabel(frame_usuario, text=user["tipo"], font=("Arial", 12,"bold"), text_color="#2C4371",anchor="n")
            tipo_user.grid(row=1, column=2, padx=5, pady=2,sticky="w")

    def interfaz_discos (self, discos):

        """
        METODO QUE CREA EL FRAME DE DISCOS EN EL FRAME DE DETALLES TECNICOS
        """
        #FRAME DE DISCCOS PARA DAR UN ESTILO DE CAJA CON BORDES
        contenedor_almacenamiento = ctk.CTkFrame(self.frame_fila2_detalles_tecnicos,fg_color="#FAFDFF", corner_radius=6, border_width=2, border_color="#F5F5F5")
        contenedor_almacenamiento.grid(row=0, column=0, padx=(15,0), pady=5, sticky="ewsn")
        contenedor_almacenamiento.grid_columnconfigure(1, weight=1)
        contenedor_almacenamiento.grid_rowconfigure(0, weight=1)

        almacenamiento_logo = ctk.CTkImage(light_image=Image.open(logo_almacenamiento),size=(20, 15))
        label_almacenamiento_logo = ctk.CTkLabel(contenedor_almacenamiento, image=almacenamiento_logo, text="", fg_color="transparent", anchor="center")
        label_almacenamiento_logo.grid(row=0, column=0, padx=10, sticky="w")

        label_cantidad_discos = ctk.CTkLabel(contenedor_almacenamiento, text=f"Almacenamiento (Discos) ({len(discos)})", font=("Arial", 12,"bold"), text_color="#203A6E",anchor="center")
        label_cantidad_discos.grid(row=0, column=1, sticky="w")

        frame_lista_discos = ctk.CTkScrollableFrame(contenedor_almacenamiento, fg_color="transparent") #FRAME CON SCROLL QUE CONTIENE LOS DISCOS
        frame_lista_discos.grid(row=1, column=0, columnspan=2, padx=2, pady=2, sticky="ewsn")
        frame_lista_discos.grid_columnconfigure(0, weight=0)



        for i, disco in enumerate(discos):
            #frame card de cada disco
            frame_disco = ctk.CTkFrame(frame_lista_discos,fg_color= "#FCFCDF", corner_radius=6, border_width=2, border_color="#FBFBBD")
            frame_disco.grid(row=(i+1), column=0, columnspan=3, padx=2, pady=2, sticky="we")
            frame_disco.grid_columnconfigure(0, weight=1)
            frame_disco.grid_columnconfigure(1, weight=1)
            frame_disco.grid_columnconfigure(2, weight=1)


            modelo = disco["modelo"]
            serial = disco["serial"]
            capacidad = disco["capacidad"]
            interfaz = disco["interfaz"]
            fallos = disco["fallos_criticos"]

            disco_logo = ctk.CTkImage(light_image=Image.open(logo_disco),size=(22, 26))
            label_discos_logo = ctk.CTkLabel(frame_disco, image=disco_logo, text="", fg_color="transparent", anchor="center")
            label_discos_logo.grid(row=0, column=0, padx=5, pady=5, rowspan=4, sticky="ns")

            label_modelo = ctk.CTkLabel(frame_disco, text="Modelo:", font=("Arial", 12,), text_color="#2C4371",anchor="s")
            label_modelo.grid(row=0, column=1, padx=5, pady=(2,0), sticky="w")

            modelo_disco = ctk.CTkLabel(frame_disco, text=modelo, font=("Arial", 12,"bold"), text_color="#2C4371",anchor="s",wraplength=180)
            modelo_disco.grid(row=0, column=2, padx=5,pady=(2,0),sticky="w")

            label_serial = ctk.CTkLabel(frame_disco, text="Serial:", font=("Arial", 12,), text_color="#2C4371")
            label_serial.grid(row=1, column=1, padx=5,sticky="w")

            serial_disco = ctk.CTkLabel(frame_disco, text=serial, font=("Arial", 12,"bold"), text_color="#2C4371",wraplength=180)
            serial_disco.grid(row=1, column=2, padx=5,sticky="w")

            label_capacidad = ctk.CTkLabel(frame_disco, text="Capacidad:", font=("Arial", 12,), text_color="#2C4371",)
            label_capacidad.grid(row=2, column=1, padx=5,sticky="w")

            capacidad_disco = ctk.CTkLabel(frame_disco, text=capacidad, font=("Arial", 12,"bold"), text_color="#2C4371")
            capacidad_disco.grid(row=2, column=2, padx=5,sticky="w")

            label_interfaz = ctk.CTkLabel(frame_disco, text="Interfaz:", font=("Arial", 12,), text_color="#2C4371")
            label_interfaz.grid(row=3, column=1, padx=5,sticky="w")

            interfaz_disco = ctk.CTkLabel(frame_disco, text=interfaz, font=("Arial", 12,"bold"), text_color="#2C4371")
            interfaz_disco.grid(row=3, column=2, padx=5,sticky="w")

            label_fallos = ctk.CTkLabel(frame_disco, text="Fallos críticos:", font=("Arial", 12,), text_color="#2C4371")
            label_fallos.grid(row=4, column=1, padx=5,pady=(0,2),sticky="w")

            fallos_disco = ctk.CTkLabel (frame_disco, text=fallos, font=("Arial", 12,"bold"), text_color="#2C4371")
            fallos_disco.grid(row=4, column=2, padx=5,pady=(0,2),sticky="w")

    def interfaz_memoria (self, memorias):

        contenedor_memorias = ctk.CTkFrame(self.frame_fila2_detalles_tecnicos,fg_color="#FAFDFF",corner_radius=6, border_width=2, border_color="#F5F5F5")
        contenedor_memorias.grid(row=0, column=1, padx=5, pady=5, sticky="ewsn")
        contenedor_memorias.grid_columnconfigure(1, weight=1)

        contenedor_memorias.grid_rowconfigure(0, weight=1)

        memorias_logo = ctk.CTkImage(light_image=Image.open(logo_memorias),size=(20, 15))
        label_memorias_logo = ctk.CTkLabel(contenedor_memorias, image=memorias_logo, text="", fg_color="transparent", anchor="center")
        label_memorias_logo.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        label_cantidad_memorias = ctk.CTkLabel(contenedor_memorias, text=f"Memorias RAM ({len(memorias)})", font=("Arial", 12,"bold"), text_color="#203A6E",anchor="center")
        label_cantidad_memorias.grid(row=0, column=1, pady=5, sticky="w")

        # contenedor con la lista de memorias
        frame_lista_memorias = ctk.CTkScrollableFrame(contenedor_memorias, fg_color="transparent",)
        frame_lista_memorias.grid(row=1, column=0, columnspan=2, padx=2, pady=2,sticky="nsew")

        for i, memoria in enumerate(memorias):

            frabricante = memoria["fabricante"]
            capacidad = memoria["capacidad"]
            serial = memoria["serial"]
            partnumber = memoria["partnumber"]
            tipo = memoria["tipo"]

            #frame card memoria
            frame_memoria = ctk.CTkFrame(frame_lista_memorias,fg_color= "#D2FBE9", corner_radius=6, border_width=2, border_color="#C4FAE3")
            frame_memoria.grid(row=i, column=0, padx=5, pady=5, sticky="nsew")

            memoria_logo = ctk.CTkImage(light_image=Image.open(logo_memoria),size=(28, 18))
            label_memoria_logo = ctk.CTkLabel(frame_memoria, image=memoria_logo, text="", fg_color="transparent", anchor="center")
            label_memoria_logo.grid(row=0, column=0, padx=5, rowspan=4, sticky="w")

            label_fabricante = ctk.CTkLabel(frame_memoria, text="Fabricante:", font=("Arial", 12,), text_color="#2C4371",)
            label_fabricante.grid(row=0, column=1, padx=5,sticky="w")
            fabricante_memoria = ctk.CTkLabel(frame_memoria, text=frabricante, font=("Arial", 12,"bold"), text_color="#2C4371",wraplength=150)
            fabricante_memoria.grid(row=0, column=2, padx=5,sticky="w")

            label_capacidad = ctk.CTkLabel(frame_memoria, text="Capacidad:", font=("Arial", 12,), text_color="#2C4371")
            label_capacidad.grid(row=1, column=1, padx=5,sticky="w")
            capacidad_memoria = ctk.CTkLabel(frame_memoria, text=f"{capacidad} GB", font=("Arial", 12,"bold"), text_color="#2C4371")
            capacidad_memoria.grid(row=1, column=2, padx=5,sticky="w")

            label_serial = ctk.CTkLabel(frame_memoria, text="Serial:", font=("Arial", 12,), text_color="#2C4371",wraplength=150)
            label_serial.grid(row=2, column=1, padx=5,sticky="w")
            serial_memoria = ctk.CTkLabel(frame_memoria, text=serial, font=("Arial", 12,"bold"), text_color="#2C4371")
            serial_memoria.grid(row=2, column=2, padx=5,sticky="w")

            label_tipo = ctk.CTkLabel(frame_memoria, text="Tipo:", font=("Arial", 12,), text_color="#2C4371")
            label_tipo.grid(row=3, column=1, padx=5,sticky="w")
            tipo_memoria = ctk.CTkLabel(frame_memoria, text=tipo, font=("Arial", 12,"bold"), text_color="#2C4371")
            tipo_memoria.grid(row=3, column=2, padx=5,sticky="w")

            label_partnum = ctk.CTkLabel(frame_memoria, text="Partnumber:", font=("Arial", 12,), text_color="#2C4371")
            label_partnum.grid(row=4, column=1, padx=5,sticky="w")
            partnum_memoria = ctk.CTkLabel(frame_memoria, text=partnumber, font=("Arial", 12,"bold"), text_color="#2C4371")
            partnum_memoria.grid(row=4, column=2, padx=5,sticky="w")

    def interfaz_adaptador_red (self,adaptadores):

        contenedor_red = ctk.CTkFrame(self.frame_fila2_detalles_tecnicos,fg_color="#FAFDFF",corner_radius=6, border_width=2, border_color="#F5F5F5")
        contenedor_red.grid(row=0, column=2, padx=2, pady=5, sticky="ewsn")
        # contenedor_red.grid_rowconfigure(0, weight=1)
        contenedor_red.grid_columnconfigure(1, weight=1)

        logo_adapt_red = ctk.CTkImage(light_image=Image.open(logo_redes),size=(20, 18))
        label_logo_adapt_red = ctk.CTkLabel(contenedor_red, image=logo_adapt_red, text="", fg_color="transparent", anchor="center")
        label_logo_adapt_red.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        label_cantidad_adaptadores = ctk.CTkLabel(contenedor_red, text=f"Red (Adaptadores) ({len(adaptadores)})", font=("Arial", 12,"bold"), text_color="#203A6E",anchor="center")
        label_cantidad_adaptadores.grid(row=0, column=1, pady=5,sticky="w")

        frame_lista_adaptadores = ctk.CTkScrollableFrame(contenedor_red, fg_color="transparent") #FRAME CON SCROLL QUE CONTIENE LOS DISCOS
        frame_lista_adaptadores.grid(row=1, column=0, columnspan=2, padx=2, pady=2, sticky="ewsn")
        frame_lista_adaptadores.grid_columnconfigure(0, weight=0)
        frame_lista_adaptadores.grid_rowconfigure(0, weight=0)

        for i, adaptador in enumerate(adaptadores):

            nombre = adaptador["nombre"]
            mac = adaptador["mac"]
            velocidad = adaptador["velocidad"]

            frame_adaptador = ctk.CTkFrame(frame_lista_adaptadores,fg_color="#DFEEFA",corner_radius=6, border_width=2, border_color="#D7ECFD")
            frame_adaptador.grid(row=i, column=0, padx=5, pady=5, sticky="nsew")

            logo_adaptador = ctk.CTkImage(light_image=Image.open(logo_red),size=(20, 25))
            label_logo_adaptador = ctk.CTkLabel(frame_adaptador, image=logo_adaptador, text="", anchor="center")
            label_logo_adaptador.grid(row=0, column=0, rowspan=3, padx=5, sticky="w")

            label_nombre_adaptador = ctk.CTkLabel(frame_adaptador, text="Nombre:", font=("Arial", 12), text_color="#203A6E")
            label_nombre_adaptador.grid(row=0, column=1, padx=5, pady=(2,0), sticky="w")

            nombre_adaptador = ctk.CTkLabel(frame_adaptador, text=nombre, font=("Arial", 12,"bold"), text_color="#203A6E")
            nombre_adaptador.grid(row=0, column=2, padx=5,pady=(2,0), sticky="w")

            label_mac_adaptador = ctk.CTkLabel(frame_adaptador, text="MAC:", font=("Arial", 12), text_color="#203A6E")
            label_mac_adaptador.grid(row=1, column=1, padx=5, sticky="w")

            mac_adaptador = ctk.CTkLabel(frame_adaptador, text=mac, font=("Arial", 12,"bold"), text_color="#203A6E")
            mac_adaptador.grid(row=1, column=2, padx=5, sticky="w")

            label_velocidad_adaptador = ctk.CTkLabel(frame_adaptador, text="Velocidad:", font=("Arial", 12), text_color="#203A6E")
            label_velocidad_adaptador.grid(row=2, column=1, padx=5, pady=(0,2), sticky="w")

            velocidad_adaptador = ctk.CTkLabel(frame_adaptador, text=velocidad, font=("Arial", 12,"bold"), text_color="#203A6E")
            velocidad_adaptador.grid(row=2, column=2, padx=5, pady=(0,2), sticky="w")

    def interfaz_GPUs(self,gpus):

        contenedor_gpu = ctk.CTkFrame(self.frame_fila2_detalles_tecnicos,fg_color="#FAFDFF",corner_radius=6, border_width=2, border_color="#F5F5F5")
        contenedor_gpu.grid(row=0, column=3, padx=(2,15), pady=5, sticky="ewsn")
        contenedor_gpu.grid_columnconfigure(1, weight=1)

        gpus_logo = ctk.CTkImage (light_image=Image.open(logo_gpus),size=(22, 18))
        label_gpus_logo = ctk.CTkLabel(contenedor_gpu, image=gpus_logo, text="", fg_color="transparent", anchor="center")
        label_gpus_logo.grid(row=0, column=0, padx=(2,15),pady=(2,0), sticky="w")
        label_gpus = ctk.CTkLabel(contenedor_gpu, text=f"Tarjetas fraficas ({len(gpus)}) ",  font=("Arial", 12,"bold"), text_color="#203A6E")
        label_gpus.grid(row=0, column=1, padx=5, pady=(2,0), sticky="w")

        frame_lista_gpus = ctk.CTkScrollableFrame(contenedor_gpu, fg_color="transparent") #FRAME CON SCROLL QUE CONTIENE LOS DISCOS
        frame_lista_gpus.grid(row=1, column=0, columnspan=2, padx=2, pady=2, sticky="ewsn")


        for i, gpu in enumerate(gpus):

            modelo = gpu["modelo"]
            fabricante = gpu["fabricante"]
            capacidad = gpu["capacidad"]

            frame_gpu = ctk.CTkFrame (frame_lista_gpus,fg_color="#FDEFFD", corner_radius=6, border_width=2, border_color="#F7D6FA")
            frame_gpu.grid(row=i, column=0, padx=5, pady=5, sticky="nsew")
            frame_gpu.grid_columnconfigure(0, weight=1)

            logo_gpu = ctk.CTkImage(light_image=Image.open(logo_grafica),size=(22, 18))
            label_logo_gpu = ctk.CTkLabel(frame_gpu, image=logo_gpu, text="")
            label_logo_gpu.grid(row=0, column=0, rowspan=3, padx=5, pady = 2, sticky="sn")

            label_modelo_gpu = ctk.CTkLabel(frame_gpu, text="Modelo:", font=("Arial", 12), text_color="#203A6E")
            label_modelo_gpu.grid(row=0, column=1, padx=5, pady=(2,0), sticky="w")

            modelo_gpu = ctk.CTkLabel(frame_gpu, text=modelo, font=("Arial", 12,"bold"), text_color="#203A6E", wraplength=120)
            modelo_gpu.grid(row=0, column=2, padx=5,pady=(2,0), sticky="w")

            label_fabricante_gpu = ctk.CTkLabel(frame_gpu, text="Fabricante:", font=("Arial", 12), text_color="#203A6E")
            label_fabricante_gpu.grid(row=1, column=1, padx=5, sticky="w")

            label_fabricante_gpu = ctk.CTkLabel(frame_gpu, text=fabricante, font=("Arial", 12,"bold"), text_color="#203A6E", wraplength=120)
            label_fabricante_gpu.grid(row=1, column=2, padx=5, sticky="w")

            label_capacidad_gpu = ctk.CTkLabel(frame_gpu, text="Capacidad:", font=("Arial", 12), text_color="#203A6E")
            label_capacidad_gpu.grid(row=2, column=1, padx=5, pady=(0,2), sticky="w")

            if capacidad.upper() == "128 MB":
                capacidad_gpu = ctk.CTkLabel(frame_gpu, text=capacidad, font=("Arial", 12,"bold"), text_color="#203A6E")
                capacidad_gpu.grid(row=2, column=2, padx=5, pady=(0,2), sticky="w")

                logo_advertencia = ctk.CTkImage(light_image=Image.open(logo_exclamacion),size=(14, 14))
                label_advertencia = ctk.CTkLabel(frame_gpu, image=logo_advertencia, text="", anchor="s")
                label_advertencia.grid(row=3, column=0, padx=5, pady=(0,2), sticky="s")

                label_advertencia_msg = ctk.CTkLabel(frame_gpu, text="Memoria Compartida con el sistema", font=("Arial", 11,"bold"), text_color="#2960CE", anchor="s")
                label_advertencia_msg.grid(row=3, column=1, columnspan=2, padx=5, sticky="ws")

                label_advertencia_descrip = ctk.CTkLabel(frame_gpu, text="La capacidad mostrada puede ser la", font=("Arial", 11), text_color="#203A6E")
                label_advertencia_descrip.grid(row=4, column=1, columnspan=2, padx=5, pady=(0,2), sticky="w")
                label_advertencia_descrip2 = ctk.CTkLabel(frame_gpu, text="reserva minima, no el total dinamico", font=("Arial", 11), text_color="#203A6E",anchor="n")
                label_advertencia_descrip2.grid(row=5, column=1, columnspan=2, padx=5, pady=(0,2), sticky="wn")

                continue

            capacidad_gpu = ctk.CTkLabel(frame_gpu, text=capacidad, font=("Arial", 12,"bold"), text_color="#203A6E")
            capacidad_gpu.grid(row=2, column=2, padx=5, pady=(0,2), sticky="w")

    def interfaz_notas (self, notas, id_equipo):
        """
        interfaz que contiene la caja de notas
        """

        self.notas = notas #Variable para controlar los cambios en las notas
        self.id_equipo_notas = id_equipo #Guardo el ID como atributo de instancia para usarlo en guardar_notas()

        contenedor_notas = ctk.CTkFrame(self.frame_fila2_detalles_tecnicos,fg_color="#FAFDFF", corner_radius=6, border_width=2, border_color="#F5F5F5")
        contenedor_notas.grid(row=1, column=0, columnspan=4, padx=15, pady=2, sticky="ewsn")
        contenedor_notas.grid_columnconfigure(1, weight=1)
        contenedor_notas.grid_rowconfigure(1, weight=1)

        logo_notas = ctk.CTkImage (light_image=Image.open(logo_registro), size=(15, 18))
        label_logo_notas = ctk.CTkLabel(contenedor_notas, image=logo_notas, text="")
        label_logo_notas.grid(row=0, column=0, padx=5, pady=2, sticky="w")

        label_notas = ctk.CTkLabel(contenedor_notas, text="Notas", font=("Arial", 12, "bold"), text_color="#203A6E")
        label_notas.grid(row=0, column=1, padx=5, pady=2, sticky="w")

        self.estado_guardar = ctk.CTkLabel(contenedor_notas, text="", font=("Arial", 11), text_color="#203A6E")
        self.estado_guardar.grid(row=0, column=2, padx=5, pady=2, sticky="e")

        guardar_logo = ctk.CTkImage (light_image=Image.open(logo_guardar), size=(13, 15))
        boton_guardar = ctk.CTkButton(contenedor_notas, image=guardar_logo, text="Guardar", fg_color="#1477E9",hover_color="#206CC2", text_color="white", width=100, height=15, compound="left", cursor="hand2",border_width=1, border_color="#BAC8D9", corner_radius=4, command=self.guardar_notas)
        boton_guardar.grid(row=0, column=3, padx=10, pady=2, sticky="e")

        self.label_caja_notas = ctk.CTkTextbox(contenedor_notas, font=("Arial", 12), fg_color="#FFFFFF", border_width=2, border_color="#D3D3D3", undo=True,maxundo=-1,autoseparators=True)
        self.label_caja_notas.grid(row=1, column=0, columnspan=4, padx=5, pady=(0,10), sticky="ewsn")
        self.label_caja_notas.insert("0.0", self.notas)
        self.label_caja_notas.edit_reset()
        self.label_caja_notas.bind("<KeyRelease>", self.deteccion_de_cambios_notas)
        self.label_caja_notas.bind("<Button-3>", self.menu_click_derecho_notas)
    
    def menu_click_derecho_notas (self, event):
        """
        METODO QUE MANEJA EL MENU DE CLICK DERECHO
        """
        menu = tk.Menu(self, tearoff=0, bg = "#ffffff")
        menu.add_command(label="Copiar", command=self.menu_copiar_notas)
        menu.add_command(label="Pegar",  command=self.menu_pegar_notas)
        menu.post(event.x_root, event.y_root)
        
    def menu_copiar_notas (self):
        """
        METODO QUE COPIA LAS NOTAS CON CLICK DERECHO
        """
        try:
            texto = self.label_caja_notas.selection_get()
            
        except:
            texto = self.label_caja_notas.get("1.0", "end-1c")
        
        self.clipboard_clear()
        self.clipboard_append(texto)
        self.update()
        
    def menu_pegar_notas (self):
        """
        METODO QUE PEGA LAS NOTAS CON CLICK DERECHO
        """
        try:
            try:
                self.label_caja_notas.delete("sel.first", "sel.last")
            except:
                pass
            texto = self.clipboard_get()
            self.label_caja_notas.insert("insert", texto)
        except:
            pass
        
    def guardar_notas (self):
        """
        METODO QUE GUARDA LAS NOTAS
        """
        notas = self.label_caja_notas.get("1.0", "end-1c")

        if self.notas == notas:
            self.estado_guardar.configure(text="No hay cambios que guardar", text_color="#203A6E")
            return

        notas_guardadas = self.db.insertar_notas (notas, self.id_equipo_notas)#si se guardo en la db devuelve True sino False
        
        if not notas_guardadas:
            self.estado_guardar.configure(text="Error al guardar las notas", text_color="red")
            return

        self.notas = notas
        self.estado_guardar.configure(text="Notas guardadas", text_color="#206E36")

    def deteccion_de_cambios_notas (self, event=None):

        notas = self.label_caja_notas.get("1.0", "end-1c")

        if self.notas != notas:
            self.estado_guardar.configure(text="Cambios sin guardar", text_color="red")

    def menu_click_derecho (self, event):
        
        """
        METODO QUE MANEJA EL MENU DE CLICK DERECHO
        """

        if self.custom_name_equipos_seleccionado:
            return
                
        widget = event.widget
        
        menu = tk.Menu(self, tearoff=0, bg = "#ffffff")
        menu.add_command(label="Editar nombre", command= lambda: self.editar_nombre_host (widget))
        menu.add_command(label="Eliminar equipo", command= lambda: self.interfaz_eliminar_equipo (widget))
        menu.post(event.x_root, event.y_root)
        
    def editar_nombre_host (self, widget):
        """
        MANEJA EL CAMBIO DE NOMBRE DEL EQUIPO, OBTIENE EL ID DEL EQUIPO Y PERMITE LA EDICION DEL NOMBRE
        """
        try:
            while not hasattr(widget, "es_frame_equipo"):
                widget = widget.master

            self.id_equipo_edicion_nombre = widget.id_equipo #obtenemos el id que guardamos en el frame del equipo
            self.nombre_custom = widget.custom_name.get()
            
            self.entry_custom_name = widget.custom_name  #obtenemos el widget que habia sido pasado como referencia a objeto custom_name del frame
            self.entry_custom_name.configure(state="normal",border_width=2)
            self.entry_custom_name.focus_set()
            self.entry_custom_name.select_range(0, "end") 
            
            self.custom_name_equipos_seleccionado = True

        except Exception as e:
            logger.error(f"Error al obtener el id del equipo lista frame: {str(e)}")
            return

    def restaura_nombre_custom_host (self, event = None):
        """
        METODO QUE RESTAURA EL NOMBRE DEL EQUIPO MODIFICADO CUANDO NO GUARDEN CON ENTER
        """
        self.custom_name_equipos_seleccionado = False
        if hasattr(self, "entry_custom_name") and self.entry_custom_name:
            self.entry_custom_name.configure (state="normal",border_width=0)
            self.entry_custom_name.delete(0, "end")
            self.entry_custom_name.insert(0, self.nombre_custom)
            self.entry_custom_name.configure(state="disabled")
            
            self.nombre_custom = None
            self.entry_custom_name = None
            self.id_equipo_edicion_nombre = None
        
    def guardar_nombre_custom_host (self, event):
        """
        METODO QUE GUARDA EL NOMBRE DEL EQUIPO MODIFICADO
        """
        if hasattr(self, "entry_custom_name") and self.entry_custom_name:
            self.custom_name_equipos_seleccionado = False
            nombre_nuevo = self.entry_custom_name.get().strip()
            
            if nombre_nuevo == self.nombre_custom or not nombre_nuevo:
                self.restaura_nombre_custom_host()
                return
            
            self.entry_custom_name.configure (state="disabled",border_width=0)
            
            nombre_actualizado =self.db.actualizar_custom_name (nombre_nuevo,self.id_equipo_edicion_nombre)
            
            if not nombre_actualizado:
                self.restaura_nombre_custom_host()
                return
            
            self.nombre_custom = None
            self.entry_custom_name = None
            
            # self.equipo_detalles_seleccionado = None
            
            self.id_equipo_edicion_nombre = None #importante reiniciar en None para evitar errores de consultas o actualizaciones en la DB por causa de un id incorrecto

    def interfaz_eliminar_equipo (self,widget):
            """
            CREA LA INTERFAZ DE CONFIRMACION DE ELIMINACION Y RECIBE EL WIDGET QUE CONTIENE LA INFORMACION DEL EQUIPO A ELIMINAR
            """
            
            while not hasattr(widget, "es_frame_equipo"):
                widget = widget.master
            
            #extraigo lla informacion de los objetos que fueron guardados en el frame en el metodo "_frame_lista_equipos"
            id_equipo = widget.id_equipo
            nombre = widget.custom_name.get()
            
            self.ventana_eliminar = ctk.CTkToplevel (self)
            ancho = 350
            alto = 300

            x = self.winfo_rootx() + (self.winfo_width() // 2) - (ancho // 2)
            y = self.winfo_rooty() + (self.winfo_height() // 2) - (alto // 2)

            self.ventana_eliminar.geometry(f"{ancho}x{alto}+{x}+{y}")
            self.ventana_eliminar.lift()
            self.ventana_eliminar.grab_set()
            self.ventana_eliminar.attributes("-topmost", True)
            self.ventana_eliminar.overrideredirect(True)
            self.ventana_eliminar.focus_set()
            self.ventana_eliminar.bind("<Escape>", lambda event: self.ventana_eliminar.destroy())

            frame_contenedor = ctk.CTkFrame(self.ventana_eliminar, fg_color="#ffffff",corner_radius=6,border_width=2,border_color="#E2E5E7")
            frame_contenedor.pack(fill="both", expand=True)
            frame_contenedor.grid_columnconfigure(0, weight=1)

            papelera_logo = ctk.CTkImage(dark_image=Image.open(logo_papelera), size=(50,50))
            label_papelera = ctk.CTkLabel(frame_contenedor, text=" Eliminar equipo", image=papelera_logo, compound="left", font=("Arial", 20, "bold"), fg_color="#ffffff", text_color="#203A6E", anchor="w")
            label_papelera.grid(row=0, column=0, padx=10, pady=5, sticky="w")

            #linea divisoria
            frame_linea = ctk.CTkFrame(frame_contenedor, fg_color="#F5F5F5", corner_radius=10, height=2)
            frame_linea.grid(row=1, column=0, padx=10, sticky="nsew")

            label_msj = ctk.CTkLabel (frame_contenedor, text=f"¿Estas seguro que deseas eliminar este equipo?", font=("Arial", 12,),text_color="#203A6E", anchor="w")
            label_msj.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

            #contenedor de informacion del equipo a eliminar
            frame_equipo_eliminar = ctk.CTkFrame(frame_contenedor, fg_color="#f5e7e7", corner_radius=6, border_width=2, border_color="#faafaf")
            frame_equipo_eliminar.grid(row=3, column=0, padx=10, pady=5)

            logo_equipo = ctk.CTkImage(light_image=Image.open(logo_computador_rojo), size=(40,38))
            label_logo_equipo = ctk.CTkLabel(frame_equipo_eliminar, image=logo_equipo, text="",anchor="center",fg_color="transparent")
            label_logo_equipo.grid(row=0, column=0, padx=(35,0), pady=35, sticky="we")

            label_nombre_equipo = ctk.CTkLabel(frame_equipo_eliminar, text=nombre, font=("Arial", 12, "bold"), text_color="#f35c5c", anchor="w")
            label_nombre_equipo.grid(row=0, column=1, padx=(10,35), pady=35, sticky="we")

            #frame linea divisora
            frame_linea2 = ctk.CTkFrame(frame_contenedor, fg_color="#F5F5F5", corner_radius=10, height=2)
            frame_linea2.grid(row=4, column=0, padx=10, sticky="nsew")
            
            #Frame de los botones
            frame_botones = ctk.CTkFrame(frame_contenedor, fg_color="transparent")
            frame_botones.grid(row=5, column=0, padx=2, pady=(5,2), sticky="nsew")
            frame_botones.grid_columnconfigure(0, weight=1)
            
            boton_cancelar = ctk.CTkButton(frame_botones, text="Cancelar", font=("Arial", 12, "bold"),fg_color="transparent",text_color="#203A6E", border_width=2, border_color="#E2E5E7", hover_color="#EEEEEE", width=80 ,command=self.ventana_eliminar.destroy)
            boton_cancelar.grid(row=0, column=0, padx=2, pady=5, sticky="e")

            logo_eliminar = ctk.CTkImage(dark_image=Image.open(logo_papelera_blanca), size=(18,19))
            self.boton_eliminar = ctk.CTkButton(frame_botones, image=logo_eliminar, compound="left", text="Eliminar equipo", font=("Arial", 12, "bold"),fg_color="#FC2B2B", hover_color="#C72B2B", text_color="#ffffff",width=100, command=lambda: self.eliminar_equipo(id_equipo, nombre))
            self.boton_eliminar.grid(row=0, column=1, padx=3, pady=5, sticky="e")
            
            #creamos el msj en caso de error pero no lo mostramos
            self.label_error_eliminar = ctk.CTkLabel(frame_contenedor, text="Error al eliminar el equipo", font=("Arial", 12, "bold"), text_color="#f35c5c")
            
    def eliminar_equipo (self, id_equipo, nombre):
        
        self.boton_eliminar.configure(state="disabled") #desactivamos el boton para evitar 2 clicks por error

        equipo_eliminado = self.db.eliminar_equipo(id_equipo, nombre)
        if not equipo_eliminado:
            self.label_error_eliminar.grid(row=6, column=0, padx=10, pady=(0,2), sticky="we") #mostraos el label del error
            return
        
        self.ventana_eliminar.destroy()
        #si los detalles del equipo estan mostrados en la interfaz los destruimos
        if hasattr(self, "frame_detalles_tecnicos") and self.frame_detalles_tecnicos.winfo_exists() and self.equipo_detalles_seleccionado == id_equipo:
            self.frame_detalles_tecnicos.destroy()
            self.frame_derecho_scanear.grid()
            self.equipo_detalles_seleccionado = None #limpiamos la variable que contiene el id del equipo seleccionado
            
        self.actualizar_interfaz_equipos_registrados()
    
    def buscar_equipos (self,event = None):
        texto_buscar = self.entry_buscar.get().strip()
        
        if not texto_buscar:
            self.focus()
            texto_buscar = None
            self._frame_lista_equipos(texto_buscar)
            n = self.db.cantidad_equipos()
            self.label_equipos_registrados.configure(text=f"Equipos registrados: {n}")
            return
        
        resultado_busqueda = self.db.buscar_equipo(texto_buscar)
        self.label_equipos_registrados.configure(text=f"Equipos encontrados: {len(resultado_busqueda)}")


        
        self.frame_lista_equipos.destroy()
        #limpio las variables que tienen las referencias de los widgets antiguos que fueron destruidos
        self.frame_equipo_seleccionado = None
        self.entry_custom_name = None
        self.nombre_custom = None
        self.custom_name_equipos_seleccionado = False
        
        
        #creo el nuevo frame con los resultados de la busquedaa
        self._frame_lista_equipos(resultado_busqueda)

    def exportar_reporte_pdf (self, id_equipo_export):

        datos_equipo = self.db.obtener_datos_equipo(id_equipo_export) #Consutamos los datos nuevamente al exportar para tenerlos actualizados
        
        ruta_guardar = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Archivos PDF", "*.pdf")])
        if not ruta_guardar:
            return

        reporte = Reporte_PDF()
        reporte.procesador_datos_reporte_individual(datos_equipo)
        reporte.generar_reporte()
        
        reporte_guardado =reporte.guardar_pdf(ruta_guardar)
        
        if not reporte_guardado:
            self._interfaz_error_exportar_pdf()
            
    def _interfaz_error_exportar_pdf (self,error = None):
        """
        Interfaz para mostrar el error al exportar el pdf
        """
        
        ventana_error = ctk.CTkToplevel(self)
        ventana_error.resizable(False, False)
        ancho = 300
        alto = 205

        x = self.winfo_rootx() + (self.winfo_width() // 2) - (ancho // 2)
        y = self.winfo_rooty() + (self.winfo_height() // 2) - (alto // 2)

        ventana_error.geometry(f"{ancho}x{alto}+{x}+{y}")
        ventana_error.lift()
        ventana_error.grab_set()
        ventana_error.overrideredirect(True)
        ventana_error.focus_set()
        ventana_error.bind("<Escape>", lambda event: ventana_error.destroy())
        
        contenedor = ctk.CTkFrame(ventana_error, fg_color="#FFFFFF",corner_radius=6,border_width=2,border_color="#E2E5E7")
        contenedor.pack(fill="both", expand=True)

        pdf_logo = ctk.CTkImage(dark_image=Image.open(logo_pdf_error), size=(50,50))
        label_logo_pdf= ctk.CTkLabel(contenedor, image=pdf_logo, text="")
        label_logo_pdf.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        label_titulo = ctk.CTkLabel(contenedor, text="No fue posible exportar el reporte", font=("Arial", 16, "bold"), text_color="#203A6E")
        label_titulo.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        
        label_error = ctk.CTkLabel (contenedor, text="Verifique que no exista un reporte con el mismo nombre abierto, que la ruta de destino sea válida y que disponga de permisos de escritura.",wraplength=300, font=("Arial", 12), text_color="#203A6E", justify="left")
        label_error.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        
        boton_cancelar = ctk.CTkButton(contenedor, text="Cerrar", font=("Arial", 12, "bold"),fg_color="transparent",text_color="#203A6E", border_width=2, border_color="#E2E5E7", hover_color="#EEEEEE", width=80 ,command=ventana_error.destroy)
        boton_cancelar.grid(row=3, column=0, padx=2, pady=5)
    
    def _interfaz_reporte_email (self,id_equipo_email):
        
        datos_equipo = self.db.obtener_datos_equipo(id_equipo_email) #Consutamos los datos nuevamente al enviar para tenerlos actualizados
        
        self.email = Email()
        email_configurado = self.email.leer_config_email()
        
        if email_configurado:
            ruta_pdf = None
            reporte_pdf = Reporte_PDF()
            reporte_pdf.procesador_datos_reporte_individual(datos_equipo)
            reporte_pdf.generar_reporte()
            reporte_generado = reporte_pdf.guardar_pdf_email() #Devuelve (ruta_pdf,nombre,tamano)
            
            self.ventana_email = ctk.CTkToplevel(self)
            self.ventana_email.resizable(False, False)
            ancho = 450
            alto = 450

            x = self.winfo_rootx() + (self.winfo_width() // 2) - (ancho // 2)
            y = self.winfo_rooty() + (self.winfo_height() // 2) - (alto // 2) 

            self.ventana_email.geometry(f"{ancho}x{alto}+{x}+{y}")
            self.ventana_email.lift()
            self.ventana_email.grab_set()
            self.ventana_email.overrideredirect(True)
            self.ventana_email.focus_set()
            self.ventana_email.bind("<Escape>", lambda event: self.ventana_email.destroy())
            
            contenedor_enviar = ctk.CTkFrame(self.ventana_email, fg_color="#FFFFFF",corner_radius=6,border_width=2,border_color="#E2E5E7")
            contenedor_enviar.pack(fill="both", expand=True)
            contenedor_enviar.grid_columnconfigure(0, weight=1)
            
            
            label_titulo = ctk.CTkLabel(contenedor_enviar, text="Enviar reporte por email", font=("Arial", 14, "bold"), text_color="#203A6E", anchor="s")
            label_titulo.grid(row=0, column=0, padx=10, pady=(5,0), sticky="ws")
            
            label_detalles = ctk.CTkLabel(contenedor_enviar, text="Complete los datos para enviar el reporte", font=("Arial", 12), text_color="#203A6E", justify="left")
            label_detalles.grid(row=1, column=0, padx=10, sticky="wn")
            
            frame_datos_email = ctk.CTkFrame (contenedor_enviar, fg_color = "transparent")
            frame_datos_email.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
            
            label_destinatario = ctk.CTkLabel (frame_datos_email, text="Para:", font=("Arial", 12), text_color="#203A6E")
            label_destinatario.grid(row=0, column=0, padx=(5,55), pady=5, sticky="w")
            self.entry_destinatario = ctk.CTkEntry(frame_datos_email, font = ("Arial", 13),width=270,fg_color="#FFFFFF")
            self.entry_destinatario.grid(row=0, column=1, padx=(0,5), sticky="ew")
            
            label_cc = ctk.CTkLabel (frame_datos_email, text="CC (opcional):", font=("Arial", 13), text_color="#203A6E")
            label_cc.grid(row=1, column=0, padx=(5,55), pady=5, sticky="w")
            self.entry_cc = ctk.CTkEntry(frame_datos_email, font = ("Arial", 13), width=270, fg_color="#FFFFFF")
            self.entry_cc.grid(row=1, column=1, padx=(0,5), sticky="ew")

            label_asunto = ctk.CTkLabel (frame_datos_email, text="Asunto:", font=("Arial", 13), text_color="#203A6E")
            label_asunto.grid(row=2, column=0, padx=(5,55), pady=5, sticky="w")
            self.entry_asunto = ctk.CTkEntry(frame_datos_email, font = ("Arial", 13), width=270,fg_color="#FFFFFF")
            self.entry_asunto.grid(row=2, column=1, padx=(0,5), sticky="ew")
            
            label_mensaje = ctk.CTkLabel (frame_datos_email, text="Mensaje:", font=("Arial", 13), text_color="#203A6E")
            label_mensaje.grid(row=3, column=0, padx=(5,55), pady=5, sticky="w")
            self.caja_mensaje = ctk.CTkTextbox(frame_datos_email, font = ("Arial", 13), width=270, height=100, border_width=2, border_color="#A7A7A7", corner_radius=6, fg_color="#FFFFFF")
            self.caja_mensaje.grid(row=3, column=1, padx=(0,5), sticky="ew")
            
            label_adjunto = ctk.CTkLabel (frame_datos_email, text="Adjunto:", font=("Arial", 13), text_color="#203A6E")
            label_adjunto.grid(row=4, column=0, padx=(5,55), pady=5, sticky="w")
            
            frame_adjunto = ctk.CTkFrame (frame_datos_email, fg_color="#FFFFFF", corner_radius=6, border_width=2, border_color="#A7A7A7")
            frame_adjunto.grid(row=4, column=1, padx=(0,5), pady=5, sticky="ew")
            
            
            # reporte_generado  = False
            if reporte_generado:
                ruta_pdf = reporte_generado[0] #actualizamos la variable ruta con el valor real
                nombre_pdf = reporte_generado[1]
                tamano_pdf = reporte_generado[2]
                frame_adjunto.configure(cursor="hand2")
                frame_adjunto.bind("<Button-1>", lambda event: self._abrir_pdf(ruta_pdf))
                
                pdf_logo = ctk.CTkImage(light_image=Image.open(logo_pdf_email),size=(25, 30))
                label_logo_pdf = ctk.CTkLabel(frame_adjunto, image=pdf_logo, text="", fg_color="transparent", anchor="center",cursor="hand2")
                label_logo_pdf.grid(row=0, column=0, padx=5, pady=5, sticky="w",rowspan=2)
                label_logo_pdf.bind("<Button-1>", lambda event: self._abrir_pdf(ruta_pdf))

                label_nombre_pdf = ctk.CTkLabel(frame_adjunto, text=f"{nombre_pdf[:26]}...", font=("Arial", 13), text_color="#203A6E", anchor="w",cursor="hand2")
                label_nombre_pdf.grid(row=0, column=1, padx=5, pady=(5,0), sticky="ws")
                label_nombre_pdf.bind("<Button-1>", lambda event: self._abrir_pdf(ruta_pdf))
                
                label_tamano_pdf = ctk.CTkLabel(frame_adjunto, text=f"{tamano_pdf:.1f} KB", font=("Arial", 13), text_color="#203A6E", anchor="w",cursor="hand2")
                label_tamano_pdf.grid(row=1, column=1, padx=5, pady=(0,5), sticky="wn")
                label_tamano_pdf.bind("<Button-1>", lambda event: self._abrir_pdf(ruta_pdf))
            
            else:
                pdf_logo = ctk.CTkImage(light_image=Image.open(logo_pdf_error),size=(28, 30))
                label_logo_pdf = ctk.CTkLabel(frame_adjunto, image=pdf_logo, text="", fg_color="transparent", anchor="center")
                label_logo_pdf.grid(row=0, column=0, padx=5, pady=5, sticky="w")
                label_no_adjunto = ctk.CTkLabel(frame_adjunto, text="Error al adjuntar el reporte", font=("Arial", 13), text_color="#203A6E", anchor="w")
                label_no_adjunto.grid(row=0, column=1, padx=5, pady=(5,0), sticky="wn")

            frame_botones = ctk.CTkFrame(contenedor_enviar, fg_color="transparent")
            frame_botones.grid(row=3, column=0, padx=10, pady=5, stick="eswn")
            frame_botones.grid_columnconfigure(0, weight=1)
            boton_cancelar = ctk.CTkButton(frame_botones, text="Cancelar", font=("Arial", 13, "bold"),fg_color="transparent",text_color="#203A6E", border_width=2, border_color="#E2E5E7", hover_color="#EEEEEE", cursor="hand2", width=90, height=35 ,command=self.ventana_email.destroy)
            boton_cancelar.grid(row=0, column=0, padx=2, pady=5, sticky="e")

            boton_enviar = ctk.CTkButton(frame_botones, text = "Enviar reporte", font=("Arial", 13,"bold" ), fg_color="#1477E9",hover_color="#1167C9", text_color="white", width=155, height=35, border_width=1, border_color="#BAC8D9", corner_radius=4,text_color_disabled="white", command= lambda:self.enviar_reporte(ruta_pdf))
            boton_enviar.grid(row=0, column=1, padx=15, pady=5, sticky="e")

        else:
            
            self.ventana_email = ctk.CTkToplevel(self)
            self.ventana_email.resizable(False, False)
            ancho = 300
            alto = 160

            x = self.winfo_rootx() + (self.winfo_width() // 2) - (ancho // 2)
            y = self.winfo_rooty() + (self.winfo_height() // 2) - (alto // 2) 

            self.ventana_email.geometry(f"{ancho}x{alto}+{x}+{y}")
            self.ventana_email.lift()
            self.ventana_email.grab_set()
            self.ventana_email.overrideredirect(True)
            self.ventana_email.focus_set()
            self.ventana_email.bind("<Escape>", lambda event: self.ventana_email.destroy())
            
            contenedor_enviar = ctk.CTkFrame(self.ventana_email, fg_color="#FFFFFF",corner_radius=6,border_width=2,border_color="#E2E5E7")
            contenedor_enviar.pack(fill="both", expand=True)
            contenedor_enviar.grid_columnconfigure(0, weight=1)
            
            label_titulo_enviar = ctk.CTkLabel(contenedor_enviar, text="Correo no configurado", font=("Arial", 14, "bold"), text_color="#203A6E")
            label_titulo_enviar.grid(row=0, column=0, padx=10, pady=10, sticky="n")
            
            frame_detalles = ctk.CTkFrame(contenedor_enviar, fg_color="transparent")
            frame_detalles.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
            
            aviso_logo = ctk.CTkImage(light_image=Image.open(logo_aviso),size=(30, 28))
            label_aviso = ctk.CTkLabel(frame_detalles, image=aviso_logo, text="", fg_color="transparent", anchor="center")
            label_aviso.grid(row=0, column=0, padx=5, pady=5, sticky="w")
            
            label_descripcion = ctk.CTkLabel(frame_detalles, text="Para enviar un reporte, debe configurar un email (SMTP).", font=("Arial", 13), text_color="#203A6E", anchor="w",justify="left",wraplength=240)
            label_descripcion.grid(row=0, column=1, padx=5, pady=(5,0), sticky="wn")
            
            frame_botones = ctk.CTkFrame(contenedor_enviar, fg_color="transparent")
            frame_botones.grid(row=2, column=0, padx=10, pady=5, stick="eswn")
            frame_botones.grid_columnconfigure(0, weight=1)
            
            boton_cancelar = ctk.CTkButton(frame_botones, text="Cancelar", font=("Arial", 13, "bold"),fg_color="transparent",text_color="#203A6E", border_width=2, border_color="#E2E5E7", hover_color="#EEEEEE", cursor="hand2", width=90, height=35 ,command=self.ventana_email.destroy)
            boton_cancelar.grid(row=0, column=0, padx=2, pady=5, sticky="e")

            boton_configurar = ctk.CTkButton(frame_botones, text = "Configurar ", font=("Arial", 13,"bold" ), fg_color="#1477E9",hover_color="#1167C9", text_color="white", width=100, height=35, border_width=1, border_color="#BAC8D9", corner_radius=4,text_color_disabled="white", command= self._interfaz_config_email)
            boton_configurar.grid(row=0, column=1, padx=(2,5), pady=5, sticky="e")
            
    def _abrir_pdf (self, ruta_pdf): #recibe solo la ruta, el evento no es necesario
        """
        Abre el PDF
        """
        os.startfile(ruta_pdf)
        
    def menu_config (self,opcion):
        """
        gestiona el llamado de la ventana de configuracion email y acerca de

        """
        self.menu_op.set("")
        if opcion == "Configurar Correo (SMTP)":
            self._interfaz_config_email()
            
        
        elif opcion == "Acerca de Ors4SysInfo":
            self._interfaz_acerca_de()
    
    def _interfaz_config_email (self):
        
        """
        Interfaz para configurar el correo SMTP
        """

        if hasattr (self, "ventana_email") and self.ventana_email.winfo_exists(): #si fue llamada desde la ventana envio de email se destruye esa ventana
            self.ventana_email.destroy()
        
        
        email = Email()
        datos_email = email.leer_config_email() #Retorna una Tupla con los datos de la base de datos
                
        ventana_config = ctk.CTkToplevel (self)
        ancho = 450
        alto = 450

        x = self.winfo_rootx() + (self.winfo_width() // 2) - (ancho // 2)
        y = self.winfo_rooty() + (self.winfo_height() // 2) - (alto // 2)

        ventana_config.geometry(f"{ancho}x{alto}+{x}+{y}")
        ventana_config.resizable(False, False)
        ventana_config.lift()
        ventana_config.grab_set()
        ventana_config.attributes("-topmost", True)
        ventana_config.focus_set()
        ventana_config.bind("<Escape>", lambda event: ventana_config.destroy())
        ventana_config.overrideredirect(True)

        contenedor = ctk.CTkFrame (ventana_config, fg_color="#FFFFFF",corner_radius=10,border_width=2,border_color="#E2E5E7")
        contenedor.pack(fill="both", expand=True)
        contenedor.grid_columnconfigure(0, weight=1)
    

        label_titulo =ctk.CTkLabel (contenedor, text="Configuración de correo (SMTP)", font=("Arial", 14, "bold"), text_color="#203A6E")
        label_titulo.grid(row=0, column=0, padx=10, pady=15, sticky="w")
        
        frame_descripcion = ctk.CTkFrame(contenedor, fg_color="transparent")
        frame_descripcion.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        logo_email = ctk.CTkImage(light_image=Image.open(logo_email_config), size=(60,60))
        label_logo_email= ctk.CTkLabel(frame_descripcion, image=logo_email, text="")
        label_logo_email.grid(row=0, column=0, rowspan=2, padx=10, pady=5)

        label_descripcion = ctk.CTkLabel(frame_descripcion, text="Ingrese los datos de su servidor de email.", font=("Arial", 13), text_color="#203A6E",)
        label_descripcion.grid(row=0, column=1, padx=10, pady=(5,0),stick="ws")

        label_descripcioin1 = ctk.CTkLabel(frame_descripcion, text="Estos datos se usaran para enviar los reportes por email.", font=("Arial", 13), text_color="#203A6E", anchor="n")
        label_descripcioin1.grid(row=1, column=1, padx=10, stick="wn" )

        frame_datos_email = ctk.CTkFrame(contenedor,fg_color="transparent")
        frame_datos_email.grid(row=2, column=0, padx=10, pady=5, stick = "eswn")

        label_smtp = ctk.CTkLabel(frame_datos_email, text="Servidor SMTP:", font=("Arial", 13), text_color="#203A6E",)
        label_smtp.grid(row=0, column=0, padx=(5,55), stick="w")
        self.entry_smtp = ctk.CTkEntry(frame_datos_email, placeholder_text="smtp.tudominio.com", font = ("Arial", 13), width=270)
        self.entry_smtp.grid(row=0, column=1, padx=(0,5), stick="ew")

        label_puerto = ctk.CTkLabel(frame_datos_email, text="Puerto:", font=("Arial", 13), text_color="#203A6E",)
        label_puerto.grid(row=1, column=0, padx=(5,55), stick="w")
        self.entry_puerto = ctk.CTkEntry(frame_datos_email, placeholder_text="Ej: 587 / 465 u otro", font = ("Arial", 13), width=270)
        self.entry_puerto.grid(row=1, column=1, padx=(0,5), stick="ew")

        label_seguridad = ctk.CTkLabel(frame_datos_email, text="Seguridad:", font=("Arial", 13), text_color="#203A6E",)
        label_seguridad.grid(row=2, column=0, padx=(5,55), stick="w")

        frame_opcion_seguridad = ctk.CTkFrame(frame_datos_email, border_width=2,fg_color = "#F7F7F7")
        frame_opcion_seguridad.grid(row=2, column=1, padx=(0,5), stick="ew", pady=1)

        seguri_default = "Tipo de seguridad"
        self.opcion_seguridad = ctk.CTkOptionMenu(frame_opcion_seguridad, values=["STARTTLS", "SSL/TLS"], font=("Arial", 13), width=270,fg_color="#F7F7F7", height=23, dropdown_fg_color="#F7F7F7", dropdown_hover_color="#F7F7F7", text_color="#272727", button_color="#F7F7F7",button_hover_color="#F7F7F7")
        self.opcion_seguridad.set(seguri_default)
        self.opcion_seguridad.grid(row=2, column=1, padx=3, pady =3, stick="ew")

        label_remitente = ctk.CTkLabel(frame_datos_email, text="Email remitente:", font=("Arial", 13), text_color="#203A6E",)
        label_remitente.grid(row=3, column=0, padx=(5,2), pady=2, stick="w")
        self.entry_remitente = ctk.CTkEntry(frame_datos_email, placeholder_text="ejemplo@dominio.com", width=270, font=("Arial", 13))
        self.entry_remitente.grid(row=3, column=1, padx=(2,5), pady=2, stick="ew")

        label_usuario = ctk.CTkLabel(frame_datos_email, text="Usuario:", font=("Arial", 13), text_color="#203A6E",)
        label_usuario.grid(row=4, column=0, padx=(5,2), pady=2, stick="w")
        self.entry_usuario = ctk.CTkEntry(frame_datos_email, placeholder_text="usuario@dominio.com", width=270, font=("Arial", 13))
        self.entry_usuario.grid(row=4, column=1, padx=(2,5), pady=2, stick="ew")

        label_contrasena = ctk.CTkLabel (frame_datos_email, text="Contraseña:", font=("Arial", 13), text_color="#203A6E",)
        label_contrasena.grid(row=5, column=0, padx=(5,2), pady=2, stick="w")
        self.entry_contrasena = ctk.CTkEntry(frame_datos_email, placeholder_text="●●●●●●", show="●", width=270, font=("Arial", 13))
        self.entry_contrasena.grid(row=5, column=1, padx=(2,5), pady=2, stick="ew")

        frame_test = ctk.CTkFrame(contenedor, fg_color="transparent")
        frame_test.grid(row=3, column=0, padx=10, pady=5, stick = "eswn" )

        self.boton_test_conexion = ctk.CTkButton(frame_test, text="Probar Conexión",font=("Arial", 13, "bold"), fg_color="transparent",text_color="#5689EF", border_width=2, border_color="#5689EF", hover_color="#FEFAFA", width=140, height=35, cursor = "hand2", command=self.teste_conexion)
        self.boton_test_conexion.grid(row=0, column=0, padx=5, pady=5)

        self.label_msg_test = ctk.CTkLabel(frame_test, text="", font=("Arial", 12), fg_color="#FFFFFF")
        self.label_msg_test.grid(row=0, column=1, padx=5, pady=5)

        frame_botones = ctk.CTkFrame(contenedor, fg_color="transparent")
        frame_botones.grid(row=4, column=0, padx=10, pady=5, stick="eswn")
        frame_botones.grid_columnconfigure(0, weight=1)


        boton_cancelar = ctk.CTkButton(frame_botones, text="Cancelar", font=("Arial", 13, "bold"),fg_color="transparent",text_color="#203A6E", border_width=2, border_color="#E2E5E7", hover_color="#EEEEEE", cursor="hand2", width=90, height=35 ,command=ventana_config.destroy)
        boton_cancelar.grid(row=0, column=0, padx=2, pady=5, sticky="e")

        self.boton_guardar = ctk.CTkButton(frame_botones, text = "Guardar configuracion", font=("Arial", 13,"bold" ), fg_color="#BAC8D9",hover_color="#257ADC", text_color="white", width=155, height=35, border_width=1, border_color="#BAC8D9", corner_radius=4,state="disabled",text_color_disabled="white", command=self.guardar_config_email)
        self.boton_guardar.grid(row=0, column=1, padx=5, pady=5, sticky="e")

        if datos_email:
            self.entry_smtp.insert(0,datos_email[0])
            self.entry_puerto.insert(0,datos_email[1])
            seguri_default = datos_email[2]
            self.opcion_seguridad.set(seguri_default)
            self.entry_remitente.insert(0,datos_email[3])
            
            self.entry_usuario.insert(0,datos_email[4])
            self.entry_contrasena.insert(0,datos_email[5])

    def teste_conexion (self):
        """
        Inicia las configuraciones para testar la conexion
        """
        self.label_msg_test.configure(text="Probando conexión, espera unos segundos...", text_color="#5689EF", font=("Arial", 13, "bold"))
        self.boton_test_conexion.configure(text_color_disabled="white",text_color="white",fg_color="#BAC8D9", border_color="#BAC8D9",state="disabled")
        self.boton_guardar.configure(text_color_disabled="white",text_color="white",fg_color="#BAC8D9",state="disabled")
        smtp = self.entry_smtp.get()
        puerto = self.entry_puerto.get()
        seguridad = self.opcion_seguridad.get()
        remitente = self.entry_remitente.get()
        usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()

        self.email = Email(smtp, puerto, seguridad, remitente,usuario, contrasena)#pasamos los datos obtenidos para testar
        threading.Thread(target=self._iniciar_sesion).start() #iniciamos el proceso de inicio de sesion en otro hilo
        
    def _iniciar_sesion (self):
        #Ejecuta el proceso de inicio de sesion en un hilo 
        status_login =self.email.enviar_teste()
        self.after(200, lambda:self._status_login (status_login)) #despues de 0.2sg ejecutamos el metodo
        
    def _status_login (self, status_login):
        """
        Muestra el resultado del test de inicio de sesion
        """
        if status_login :
            self.label_msg_test.configure(text="✓ Conexion Exitosa", text_color="#17D66A", font=("Arial", 13, "bold"))
            self.boton_guardar.configure(fg_color="#1477E9",state="normal")
        else:
            self.boton_guardar.configure(state="normal")
            self.label_msg_test.configure(text="Error al iniciar sesion", text_color="red", font=("Arial", 13, "bold"))
            self.boton_guardar.configure(text_color_disabled="white",text_color="white",fg_color="#BAC8D9",state="disabled")
        
        self.boton_test_conexion.configure(state="normal",fg_color="transparent",text_color="#5689EF",border_color="#5689EF", hover_color="#FEFAFA")
        
    def guardar_config_email (self):
        """
        Metodo que guarda la configuracion del email en la base de datos
        """
        guardar = self.email.guardar_config_email()
        
        #se guarda la configuracion con los datos pasados al inicio solo si el test fue exitoso
        if guardar:
            self.label_msg_test.configure(text="✓ Configuracion Guardada", text_color="#17D66A", font=("Arial", 13, "bold"))
            self.boton_guardar.configure(text_color_disabled="white",text_color="white",fg_color="#BAC8D9",state="disabled")
            return
        
        self.label_msg_test.configure(text="Error al guardar la configuracion", text_color="red", font=("Arial", 13, "bold"))
        self.boton_guardar.configure(text_color_disabled="white",text_color="white",fg_color="#BAC8D9",state="disabled")
        
    def enviar_reporte (self, ruta):
        """
        inicia el proceso de envio de reporte
        """
        if ruta:
            destinatarios = self.entry_destinatario.get().strip().replace(";", ",")
            cc = self.entry_cc.get().strip().replace(";", ",")
            asunto = self.entry_asunto.get()
            msj = self.caja_mensaje.get("1.0", "end-1c")
            adjunto = ruta
            email_enviado = self.email.enviar_reporte(destinatarios, cc, asunto, msj, adjunto)

            self.ventana_email.destroy()
            
            ventana_confirmacion = ctk.CTkToplevel(self)
            ventana_confirmacion.resizable(False, False)
            ancho = 270
            alto = 120
            
            x = self.winfo_rootx() + (self.winfo_width() // 2) - (ancho // 2)
            y = self.winfo_rooty() + (self.winfo_height() // 2) - (alto // 2)

            ventana_confirmacion.geometry(f"{ancho}x{alto}+{x}+{y}")
            
            ventana_confirmacion.lift()
            ventana_confirmacion.grab_set()
            ventana_confirmacion.overrideredirect(True)
            ventana_confirmacion.focus_set()
            ventana_confirmacion.bind("<Escape>", lambda event: ventana_confirmacion.destroy())
            
            contenedor = ctk.CTkFrame(ventana_confirmacion, fg_color="#EDF4F0",corner_radius=6,border_width=2,border_color="#ABD1BF")
            contenedor.pack(fill="both", expand=True)
            
            if email_enviado:
                label_titulo = ctk.CTkLabel(contenedor, text="Reporte Enviado", font=("Arial", 12, "bold"), text_color="#203A6E")
                label_titulo.grid(row=0, column=0, padx=10, pady=5, sticky="w")
                
                check_logo = ctk.CTkImage(light_image=Image.open(logo_check), size=(30,30))
                label_mensaje = ctk.CTkLabel(contenedor, image=check_logo, text="    El reporte ha sido enviado con exito", font=("Arial", 11,"bold" ), text_color="#5FA37D", compound="left")
                label_mensaje.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
                

            else:
                label_titulo = ctk.CTkLabel(contenedor, text="Error al enviar el reporte", font=("Arial", 12, "bold"), text_color="#203A6E")
                label_titulo.grid(row=0, column=0, padx=10, pady=5, sticky="w")
                
                check_logo = ctk.CTkImage(light_image=Image.open(logo_error), size=(30,30))
                label_mensaje = ctk.CTkLabel(contenedor, image=check_logo, text="    Ocurrio un error al enviar el reporte", font=("Arial", 11,"bold" ), text_color="#E74A3B", compound="left")
                label_mensaje.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
                
            boton_aceptar = ctk.CTkButton(contenedor, text="Aceptar", command=lambda:ventana_confirmacion.destroy(), fg_color="#FFFFFF", text_color="#203A6E", border_width=2, border_color="#E2E5E7", hover_color="#F5F5F5", cursor="hand2")
            boton_aceptar.grid(row=2, column=0, padx=10, pady=5, sticky="e")

    def menu_copia_seguridad (self, opcion):
        """
        inicia el proceso de copia de seguridad
        """
        self.copia_seguridad.set("Copia de seguridad")
        
        if opcion == "Exportar":
            ruta = filedialog.asksaveasfilename(defaultextension=".db", filetypes=[("Base de datos", "*.db")])
            
            if not ruta:
                return
            
            copia =self.db.copia_seguridad(ruta)
            
            if copia:
                
                ventana_backup = ctk.CTkToplevel(self)
                ventana_backup.resizable(False, False)
                ancho = 285
                alto = 120
                
                x = self.winfo_rootx() + (self.winfo_width() // 2) - (ancho // 2)
                y = self.winfo_rooty() + (self.winfo_height() // 2) - (alto // 2)

                ventana_backup.geometry(f"{ancho}x{alto}+{x}+{y}")
                
                ventana_backup.lift()
                ventana_backup.grab_set()
                ventana_backup.overrideredirect(True)
                ventana_backup.focus_set()
                ventana_backup.bind("<Escape>", lambda event: ventana_backup.destroy())
                
                contenedor = ctk.CTkFrame(ventana_backup, fg_color="#FFFFFF",corner_radius=6,border_width=2,border_color="#EBEBEB")
                contenedor.pack(fill="both", expand=True)
                
                label_titulo = ctk.CTkLabel(contenedor, text="Exportacion completada", font=("Arial", 13, "bold"), text_color="#203A6E")
                label_titulo.grid(row=0, column=0, padx=10, pady=5, sticky="w")
                
                check_logo = ctk.CTkImage(light_image=Image.open(logo_check), size=(30,30))
                label_mensaje = ctk.CTkLabel(contenedor, image=check_logo, text="    Copia de seguridad exportada con exito", font=("Arial", 12,"bold" ), text_color="#5FA37D", compound="left")
                label_mensaje.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
            
            else:
                
                ventana_backup = ctk.CTkToplevel(self)
                ventana_backup.resizable(False, False)
                ancho = 285
                alto = 120
                
                x = self.winfo_rootx() + (self.winfo_width() // 2) - (ancho // 2)
                y = self.winfo_rooty() + (self.winfo_height() // 2) - (alto // 2)

                ventana_backup.geometry(f"{ancho}x{alto}+{x}+{y}")
                
                ventana_backup.lift()
                ventana_backup.grab_set()
                ventana_backup.overrideredirect(True)
                ventana_backup.focus_set()
                ventana_backup.bind("<Escape>", lambda event: ventana_backup.destroy())
                
                contenedor = ctk.CTkFrame(ventana_backup, fg_color="#FFFFFF",corner_radius=6,border_width=2,border_color="#EBEBEB")
                contenedor.pack(fill="both", expand=True)
                
                label_titulo = ctk.CTkLabel(contenedor, text="Error de copia de seguridad", font=("Arial", 13, "bold"), text_color="#203A6E")
                label_titulo.grid(row=0, column=0, padx=10, pady=5, sticky="w")
                
                check_logo = ctk.CTkImage(light_image=Image.open(logo_error), size=(30,30))
                label_mensaje = ctk.CTkLabel(contenedor, image=check_logo, text="    Ocurrio un error al realizar la copia", font=("Arial", 12,"bold" ), text_color="#E74A3B", compound="left")
                label_mensaje.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
            
            
                
        elif opcion == "Importar":
            ruta = filedialog.askopenfilename(defaultextension=".db", filetypes=[("Base de datos", "*.db")])
            
            if not ruta:
                return
            
            db_importada = self.db.importar_db (ruta)
            
            
            if db_importada:
                
                ventana_backup = ctk.CTkToplevel(self)
                ventana_backup.resizable(False, False)
                ancho = 285
                alto = 120
                
                x = self.winfo_rootx() + (self.winfo_width() // 2) - (ancho // 2)
                y = self.winfo_rooty() + (self.winfo_height() // 2) - (alto // 2)

                ventana_backup.geometry(f"{ancho}x{alto}+{x}+{y}")
                
                ventana_backup.lift()
                ventana_backup.grab_set()
                ventana_backup.overrideredirect(True)
                ventana_backup.focus_set()
                ventana_backup.bind("<Escape>", lambda event: ventana_backup.destroy())
                
                contenedor = ctk.CTkFrame(ventana_backup, fg_color="#FFFFFF",corner_radius=6,border_width=2,border_color="#EBEBEB")
                contenedor.pack(fill="both", expand=True)
                
                label_titulo = ctk.CTkLabel(contenedor, text="Datos importados con exito", font=("Arial", 13, "bold"), text_color="#203A6E")
                label_titulo.grid(row=0, column=0, padx=10, pady=5, sticky="w")
                
                check_logo = ctk.CTkImage(light_image=Image.open(logo_check), size=(30,30))
                label_mensaje = ctk.CTkLabel(contenedor, image=check_logo, text="    Cierre y abra nuevamente la aplicacion", font=("Arial", 12,"bold" ), text_color="#5FA37D", compound="left")
                label_mensaje.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
            
            else: 
                
                ventana_backup = ctk.CTkToplevel(self)
                ventana_backup.resizable(False, False)
                ancho = 285
                alto = 120
                
                x = self.winfo_rootx() + (self.winfo_width() // 2) - (ancho // 2)
                y = self.winfo_rooty() + (self.winfo_height() // 2) - (alto // 2)

                ventana_backup.geometry(f"{ancho}x{alto}+{x}+{y}")
                
                ventana_backup.lift()
                ventana_backup.grab_set()
                ventana_backup.overrideredirect(True)
                ventana_backup.focus_set()
                ventana_backup.bind("<Escape>", lambda event: ventana_backup.destroy())
                
                contenedor = ctk.CTkFrame(ventana_backup, fg_color="#FFFFFF",corner_radius=6,border_width=2,border_color="#EBEBEB")
                contenedor.pack(fill="both", expand=True)
                
                label_titulo = ctk.CTkLabel(contenedor, text="Importacion fallida", font=("Arial", 13, "bold"), text_color="#203A6E")
                label_titulo.grid(row=0, column=0, padx=10, pady=5, sticky="w")
                
                check_logo = ctk.CTkImage(light_image=Image.open(logo_error), size=(30,30))
                label_mensaje = ctk.CTkLabel(contenedor, image=check_logo, text="    Ocurrio un error al importar los datos", font=("Arial", 12,"bold" ), text_color="#E74A3B", compound="left")
                label_mensaje.grid(row=1, column=0, padx=10, pady=5, sticky="ew")


        boton_aceptar = ctk.CTkButton(contenedor, text="Aceptar", command=lambda:ventana_backup.destroy(), fg_color="#FFFFFF", text_color="#203A6E", border_width=2, border_color="#E2E5E7", hover_color="#F5F5F5", cursor="hand2")
        boton_aceptar.grid(row=2, column=0, padx=10, pady=5, sticky="e")

    def _interfaz_error_cargar_lista_equipos (self):
        """
        muestra msj de error en caso de que no se cargue la lista de equipos en el metodo _frame_lista_equipos
        """

        ventana_error = ctk.CTkToplevel(self)
        ventana_error.resizable(False, False)
        ancho = 315
        alto = 120
        
        x = self.winfo_rootx() + (self.winfo_width() // 2) - (ancho // 2)
        y = self.winfo_rooty() + (self.winfo_height() // 2) - (alto // 2)

        ventana_error.geometry(f"{ancho}x{alto}+{x}+{y}")
        
        ventana_error.lift()
        ventana_error.grab_set()
        ventana_error.overrideredirect(True)
        ventana_error.focus_set()
        ventana_error.bind("<Escape>", lambda event: ventana_error.destroy())
        
        contenedor = ctk.CTkFrame(ventana_error, fg_color="#FFFFFF",corner_radius=6,border_width=2,border_color="#EBEBEB")
        contenedor.pack(fill="both", expand=True)
        
        label_titulo = ctk.CTkLabel(contenedor, text="Error de base de datos", font=("Arial", 13, "bold"), text_color="#203A6E")
        label_titulo.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        check_logo = ctk.CTkImage(light_image=Image.open(logo_error), size=(30,30))
        label_mensaje = ctk.CTkLabel(contenedor, image=check_logo, text="    Ocurrio un error interno en la base de datos", font=("Arial", 12,"bold" ), text_color="#E74A3B", compound="left")
        label_mensaje.grid(row=1, column=0, padx=10, pady=5, sticky="ew")


        boton_aceptar = ctk.CTkButton(contenedor, text="Aceptar", command=lambda:ventana_error.destroy(), fg_color="#FFFFFF", text_color="#203A6E", border_width=2, border_color="#E2E5E7", hover_color="#F5F5F5", cursor="hand2")
        boton_aceptar.grid(row=2, column=0, padx=10, pady=5, sticky="e")

    def _interfaz_acerca_de (self):
        
        ventana_acerca_de = ctk.CTkToplevel(self)
        ventana_acerca_de.resizable(False, False)
        ancho = 380
        alto = 620
        
        x = self.winfo_rootx() + (self.winfo_width() // 2) - (ancho // 2)
        y = self.winfo_rooty() + (self.winfo_height() // 2) - (alto // 2)

        ventana_acerca_de.geometry(f"{ancho}x{alto}+{x}+{y}")
        
        ventana_acerca_de.lift()
        ventana_acerca_de.grab_set()
        ventana_acerca_de.overrideredirect(True)
        ventana_acerca_de.focus_set()
        ventana_acerca_de.bind("<Escape>", lambda event: ventana_acerca_de.destroy())
        
        contenedor = ctk.CTkFrame(ventana_acerca_de, fg_color="#FFFFFF",corner_radius=6,border_width=2,border_color="#EBEBEB")
        contenedor.pack(fill="both", expand=True)
        
        frame_titulo= ctk.CTkFrame(contenedor, fg_color="transparent")
        frame_titulo.pack(fill="x", pady=10, padx=10)
        frame_titulo.grid_columnconfigure(0, weight=1)
        titulo = ctk.CTkLabel(frame_titulo, text="Acerca de ORS4SysInfo", font=("Arial", 13, "bold"), text_color="#203A6E")
        titulo.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        cerrar_logo = ctk.CTkImage(light_image=Image.open(logo_cerrar), size=(15,15))
        label_cerrar = ctk.CTkLabel(frame_titulo, image=cerrar_logo, text="", cursor="hand2", anchor="e")
        label_cerrar.grid(row=0, column=1, padx=10, pady=5, sticky="e")
        label_cerrar.bind("<Button-1>", lambda event: ventana_acerca_de.destroy())
        
        logo = ctk.CTkImage(light_image=Image.open(ruta_logo), size=(150,135))
        label_logo = ctk.CTkLabel(contenedor, image=logo, text="", cursor="hand2")
        label_logo.pack(pady=(10,0))
        
        label_titulo = ctk.CTkLabel(contenedor, text="ORS4SysInfo", font=("Arial", 24, "bold"), text_color="#203A6E")
        label_titulo.pack(pady=5)
        label_subtitulo = ctk.CTkLabel(contenedor, text="Inventario tecnico de equipos", font=("Arial", 14), text_color="#203A6E")
        label_subtitulo.pack(pady=5)
        
        frame_version = ctk.CTkFrame(contenedor, fg_color="#B3CDE3")
        frame_version.pack( pady=10, padx=10)
        label_version = ctk.CTkLabel(frame_version, text=" Versión: 1.1.0 ", font=("Arial", 12,"bold"),)
        label_version.pack(padx=5)
        
        label_descripcion = ctk.CTkLabel(contenedor, text="Herramienta orientada a soporte técnico e infraestructuras IT, capaz de recopilar información del sistema, almacenar registros en una base de datos local y generar reportes automatizados.", font=("Arial", 13), text_color="#203A6E", wraplength=350)
        label_descripcion.pack(pady=2)
        
        frame_linea1 = ctk.CTkFrame(contenedor, fg_color="#C5C7C8",height=2)
        frame_linea1.pack(fill="x",pady=10)

        frame_desarrollado = ctk.CTkFrame(contenedor, fg_color="transparent")
        frame_desarrollado.pack()
        label_desarrollado = ctk.CTkLabel (frame_desarrollado, text="Desarrollado por:", font=("Arial", 13,), text_color="#203A6E")
        label_desarrollado.grid(row=0, column=0, )
        label_nelson = ctk.CTkLabel (frame_desarrollado, text="Nelson Arteaga", font=("Arial", 13,"bold"), text_color="#203A6E")
        label_nelson.grid(row=0, column=1,padx=2)

        frame_recursos = ctk.CTkFrame(frame_desarrollado, fg_color="transparent")
        frame_recursos.grid(row=1, column=0, columnspan=2,pady=10)
        frame_recursos.grid_columnconfigure(0, weight=1)
        frame_recursos.grid_columnconfigure(1, weight=1)
        
        github =ctk.CTkImage(light_image=Image.open(logo_github), size=(30,30))
        label_github = ctk.CTkLabel (frame_recursos, image=github, text="", cursor="hand2")
        label_github.grid(row=0, column=0, padx=10,pady=5, )
        label_github.bind("<Button-1>", lambda event: webbrowser.open("https://github.com/n0rs4rt"))

        instagran =ctk.CTkImage(light_image=Image.open(logo_instagran), size=(30,30))
        label_instagran = ctk.CTkLabel (frame_recursos, image=instagran, text="", cursor="hand2")
        label_instagran.grid(row=0, column=1, padx=10,pady=5, )
        label_instagran.bind("<Button-1>", lambda event: webbrowser.open("https://www.instagram.com/ors4tech"))
        
        youtube = ctk.CTkImage(light_image=Image.open(logo_youtube), size=(42,30))
        label_youtube = ctk.CTkLabel (frame_recursos, image=youtube, text="", cursor="hand2")
        label_youtube.grid(row=0, column=2, padx=10,pady=5, )
        label_youtube.bind("<Button-1>", lambda event: webbrowser.open("https://www.youtube.com/@ors4tech"))
        
        documentacion = ctk.CTkImage(light_image=Image.open(logo_registro), size=(25,30))
        label_documentacion = ctk.CTkLabel (frame_recursos, image=documentacion, text="", cursor="hand2")
        label_documentacion.grid(row=0, column=3, padx=10,pady=5,)
        label_documentacion.bind("<Button-1>", lambda event: webbrowser.open("https://github.com/n0rs4rt/ORS4SysInfo"))

        frame_linea2 = ctk.CTkFrame(contenedor, fg_color="#C5C7C8",height=2)
        frame_linea2.pack(fill="x",pady=10)
    
        label_copyright = ctk.CTkLabel (contenedor, text="© 2026 ORS4TECH - Licenciado bajo MIT License. Proyecto Open Source para la comunidad IT. ", font=("Arial", 13,), wraplength=250, text_color="#203A6E")
        label_copyright.pack(pady=10)
        
        
interfaz = Interfaz()
interfaz.mainloop()