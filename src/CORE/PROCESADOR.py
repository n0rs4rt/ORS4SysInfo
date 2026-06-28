import wmi, logging

logger = logging.getLogger("logs")

#Clase para obtener datos de hardware

class Procesador:
    def __init__(self):
        self.win =  wmi.WMI()
    def datos_procesador(self):
        procesador = {"procesador": "Desconocido"}
        try:
            for proc in self.win.Win32_Processor():
                modelo = proc.Name
                try:
                    velocidad = float (proc.MaxClockSpeed) /1000
                except Exception as e:
                    velocidad = 0.0

            procesador["procesador"] =f"{modelo} {velocidad}GHz"
            return procesador
        except Exception as e:
            logger.error(f"Error al obtener los datos del procesador: {str(e)}")
            return procesador

