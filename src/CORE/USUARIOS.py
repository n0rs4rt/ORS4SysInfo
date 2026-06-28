import wmi, logging

logger = logging.getLogger("logs")

class User:
    def __init__(self):
        self.usuarios = []
        self.win = wmi.WMI()
        
    def usuario(self):
        
        nombre = "Desconocido"
        tipo = "Desconocido"
        user = None
        try:
            for i in self.win.Win32_UserAccount():
                if not i.Disabled:
                    nombre = i.Name
                    if i.LocalAccount:
                        tipo = "Local"
                    else:
                        tipo = "Dominio"

                    user = {"nombre" : nombre,"tipo" : tipo}
                    self.usuarios.append(user)
            return self.usuarios
        except Exception as e:
            logger.error(f"No fue posible obtener datos del usuario {e}")
            user = {"nombre" : nombre,
                    "tipo" : tipo}
            self.usuario.append(user)

        