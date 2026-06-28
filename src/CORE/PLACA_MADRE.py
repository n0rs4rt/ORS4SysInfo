import wmi, logging

logger = logging.getLogger("logs")

class Placa_madre():
    def __init__(self):
        self.win = wmi.WMI()

        #posibles valores invalidos que podrian ser retornados si no es detectado la info de la placa madre
        self.valores_invalidos = {"","unknown","None",None,"null","n/a","na","not available","not specified","to be filled by o.e.m.","to be filled by oem","default string","system serial number","base board serial number","baseboard serial number","00000000","0"}


    def datos_motherboard(self):
        placa_madre = {"fabricante":"Desconocido","modelo":"Desconocido", "serial":"Desconocido", "version":"Desconocido"}

        try:
            for i in self.win.Win32_BaseBoard():
                # print(i)
                if not i.Manufacturer in self.valores_invalidos:
                    placa_madre["fabricante"] = i.Manufacturer
                if not i.Product in self.valores_invalidos:
                    placa_madre["modelo"] = i.Product
                if not i.SerialNumber in self.valores_invalidos:
                    placa_madre["serial"] = i.SerialNumber
                if not i.Version in self.valores_invalidos:
                    placa_madre["version"] = i.Version


            return placa_madre

        except Exception as e:
            logger.error(f"Error al obtener los datos de la placa madre: {str(e)}")
            return placa_madre

