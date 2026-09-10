import urllib.request, json

def comprobar_actualizacion ():
    try:
        url = "https://api.github.com/repos/n0rs4rt/ORS4SysInfo/releases/latest"
        version_actual = "1.2.0"
        with urllib.request.urlopen(url) as response:
            contenido = response.read().decode("utf-8")
            contenido = json.loads(contenido)
            
            version = contenido["tag_name"]
            
            if version != version_actual:
                return True
            else:
                return False
    except:
        return
        