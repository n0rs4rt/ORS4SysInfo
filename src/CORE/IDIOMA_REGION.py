import wmi, logging

logger = logging.getLogger("logs")

class Region:
    def __init__(self):
        self.zona_horaria = "No detectada"
        self.idioma = "No detectado"
        self.win = wmi.WMI()
        
    def region_idioma (self):
        for i in self.win.Win32_TimeZone():
            try:
                self.zona_horaria = i.Caption
            except Exception as e:
                logger.error(f"Error al obtener zona horaria: {str(e)}")
        
        #Lista de algunos idiomas
        idiomas = {
                    # Inglés (Variaciones)
                    1033: "Inglés - Estados Unidos",
                    2057: "Inglés - Reino Unido",
                    4105: "Inglés - Canadá",
                    3081: "Inglés - Australia",
                    10249: "Inglés - Sudáfrica",
                    7177: "Inglés - Nueva Zelanda",
                    11273: "Inglés - Irlanda",
                    
                    # Español (Variaciones)
                    1034: "Español - España",
                    3082: "Español - Latinoamérica",
                    11274: "Español - Argentina",
                    2058: "Español - México",
                    19466: "Español - Venezuela",
                    13322: "Español - Colombia",
                    9226: "Español - Perú",
                    5130: "Español - Chile",
                    10250: "Español - Ecuador",
                    4106: "Español - Guatemala",
                    7178: "Español - Paraguay",
                    20490: "Español - Uruguay",
                    6154: "Español - Panamá",
                    15370: "Español - Costa Rica",
                    10282: "Español - Bolivia",
                    14346: "Español - República Dominicana",
                    16394: "Español - El Salvador",
                    17418: "Español - Honduras",
                    58378: "Español - Nicaragua",
                    22538: "Español - Puerto Rico",
                    
                    # Francés (Variaciones)
                    1036: "Francés - Francia",
                    3084: "Francés - Canadá",
                    12300: "Francés - Suiza",
                    5132: "Francés - Bélgica",
                    6156: "Francés - Luxemburgo",
                    
                    # Italiano (Variaciones)
                    1040: "Italiano - Italia",
                    2064: "Italiano - Suiza",
                    
                    # Alemán (Variaciones)
                    1031: "Alemán - Alemania",
                    3079: "Alemán - Austria",
                    4103: "Alemán - Suiza",
                    5127: "Alemán - Liechtenstein",
                    
                    # Portugués (Variaciones)
                    2070: "Portugués - Portugal",
                    1046: "Portugués - Brasil",
                    5166: "Portugués - Mozambique",
                    1049: "Portugués - Angola",
                    16385: "Portugués - Guinea-Bissau",
                    2074: "Portugués - Timor Oriental",
                    
                    # Neerlandés (Variaciones)
                    1043: "Neerlandés - Países Bajos",
                    2067: "Neerlandés - Bélgica",
                    
                    # Otros idiomas comunes en Europa y globales
                    1053: "Sueco - Suecia",
                    1044: "Noruego - Noruega",
                    1045: "Polaco - Polonia",
                    1049: "Ruso - Rusia",
                    1057: "Indonesio - Indonesia",
                    2052: "Chino (Simplificado) - China",
                    1028: "Chino (Tradicional) - Taiwán",
                    1041: "Japonés - Japón",
                    1042: "Coreano - Corea del Sur",
                    1081: "Hindi - India",
                }
        
        for i in self.win.Win32_OperatingSystem():
            try:
                self.idioma = idiomas[i.OSLanguage]
            except Exception as e:
                logger.error(f"Error al obtener el idioma: {str(e)}")
    
    def resultado (self):
        datos = {"zona_horaria" : self.zona_horaria,
                "idioma" : self.idioma}
        
        return datos
    