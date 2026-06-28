import wmi, logging, subprocess, xmltodict, json
from CORE.RUTAS import *

logger = logging.getLogger("logs")

class Grafica():
    def __init__(self):
        self.graficas = []
        self.total_graficas = None
        self.win = wmi.WMI()
    
    def analizar_gpu(self):
        contenido_xml = None
        capacidad = "Desconocido"
        fabricante = "Desconocido"
        datos_gpu = "Desconocido"
        lista_gpus = []
        xml_datos_gpu_dic = "Desconocido"
        self.ruta_tmp = ruta_tmp / "GPU.xml"
        comando = ["dxdiag","/x",self.ruta_tmp]
        try:
            subprocess.run (comando , capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            with open (self.ruta_tmp, "r", encoding= "utf-8") as gpu_xml:
                contenido_xml = gpu_xml.read()
                xml_datos_gpu_dic = xmltodict.parse (contenido_xml)
            
            #Estas lineas son para generar el Json y analizar bien los datos de la grafica para el codigo y realizar los calculos    
            # with open (ruta_tmp / "GPU.json", "w", encoding= "utf-8") as diccionario:
            #     json.dump(self.datos_gpu,diccionario, indent=4, ensure_ascii=False)

            for i in xml_datos_gpu_dic["DxDiag"]["DisplayDevices"]["DisplayDevice"]:                    
                nombre =i["CardName"]
                fabricante = i["Manufacturer"]     
                capacidad = i["DedicatedMemory"]

                datos_gpu = {"nombre" : nombre, "fabricante": fabricante, "capacidad": capacidad}
                lista_gpus.append(datos_gpu)
        
            for gpu in lista_gpus:
                #Filtramos las graficas repetidas porque aveces da resultados repetidos
                if gpu not in self.graficas:
                    self.graficas.append(gpu)
        
        except Exception as e:
            logger.error(f"Primer analisis de la grafica fallo, iniciando metodo alternativo de analisis {e}")

            for i in self.win.Win32_VideoController():
                try:
                    nombre = i.Name
                except Exception as e:
                    logger.error (f"error al obtener el nombre {e}")
                try:
                    fabricante = i.AdapterCompatibility
                except  Exception as e:
                    logger.error (f"error al obtener el fabricante")

                datos_gpu = {"nombre" : nombre, "fabricante":fabricante, "capacidad" : capacidad }
                self.graficas.append(datos_gpu)
            
        return self.graficas
