# ORS4SysInfo


<p align="center">
  <img src="https://github.com/n0rs4rt/ORS4SysInfo/blob/685b5af870dea869c6e13e22faa48e24b87dd8f7/assets/portada.png" alt="ORS4SysInfo - Portada" width="900">
</p>

ORS4SysInfo es una herramienta desarrollada en Python para el inventario técnico de equipos Windows.
Permite escanear un computador, recopilar información interna del sistema, registrar los datos en una base de datos local, generar reportes técnicos en PDF y enviar dichos reportes por email.

El objetivo principal del proyecto es facilitar tareas de soporte técnico, administración de sistemas e infraestructuras IT, reduciendo el trabajo manual al momento de documentar equipos, consultar información técnica o mantener un inventario organizado.

---

## Estado del proyecto

ORS4SysInfo se encuentra en una versión funcional y finalizada.
El proyecto puede recibir mejoras, ajustes o correcciones en futuras versiones según pruebas, uso real o reportes de errores.
Si encuentras algún fallo o tienes una sugerencia, puedes reportarlo a través del repositorio o por los canales oficiales de ORS4TECH.

---

## Características principales

* Escaneo técnico de equipos Windows.
* Registro automático de cada equipo escaneado.
* Almacenamiento de información en una base de datos local.
* Búsqueda de equipos por nombre, hostname, número de serie o nombre personalizado.
* Edición de nombre personalizado para identificar equipos más fácilmente.
* Eliminación individual de equipos registrados.
* Apartado de notas por equipo.
* Conservación de notas al reescanear el mismo equipo.
* Generación de reportes técnicos en PDF.
* Envío de reportes por email.
* Vista previa o apertura del PDF generado antes de enviarlo por email.
* Exportación e importación de la base de datos.
* Interfaz gráfica para consulta y gestión de registros.

---

## Información recopilada

ORS4SysInfo recopila información técnica interna del equipo, entre ellas:

<p align="center">
  <img src="https://github.com/n0rs4rt/ORS4SysInfo/blob/eecd09e696c9b9522e285d334b35d6891b3de19c/assets/escaneo.png" alt="ORS4SysInfo - Portada" width="900">
</p>

* Nombre del equipo.
* Modelo del computador.
* Sistema operativo.
* Idioma configurado.
* Zona horaria.
* Dominio o grupo de trabajo.
* Últimos caracteres de la licencia de Windows.
* Fabricante y versión de BIOS.
* Serial de BIOS.
* Modelo, serial y versión de la placa base.
* Procesador.
* Memorias RAM instaladas:

  * Fabricante.
  * Capacidad.
  * Serial.
  * Tipo.
  * Part number.
* Discos de almacenamiento:

  * Modelo.
  * Serial.
  * Capacidad.
  * Interfaz.
  * Estado de fallos críticos.
* Adaptadores de red:

  * Nombre.
  * Dirección MAC.
  * Velocidad de enlace.
* Tarjetas gráficas:

  * Modelo.
  * Fabricante.
  * Capacidad detectada.
* Usuarios registrados en el equipo:

  * Nombre de usuario.
  * Tipo de cuenta.

---

## Interfaz principal

<p align="center">
  <img src="https://github.com/n0rs4rt/ORS4SysInfo/blob/0f2914af37a645b8e53d6ef9c16d741b024a2b83/assets/sin_registros.png" alt="ORS4SysInfo - Portada" width="900">
</p>


La interfaz permite visualizar los equipos registrados, buscar registros, consultar detalles técnicos del equipo seleccionado y acceder a las opciones de reportes, email, notas y copias de seguridad.

Cada equipo escaneado queda registrado automáticamente en la base de datos local.

---

## Búsqueda y gestión de equipos

<!-- TODO: Colocar aquí una captura del panel lateral con equipos registrados y buscador -->

<!-- Ejemplo: -->

<!-- ![Búsqueda de equipos](docs/images/busqueda-equipos.png) -->

Los registros pueden buscarse de forma parcial utilizando:

* Nombre personalizado.
* Hostname.
* Número de serie.

También es posible asignar un nombre personalizado a cada equipo para facilitar su identificación.
Por ejemplo:

* PC de oficina.
* Portátil personal.
* Equipo de recepción.
* Máquina virtual de pruebas.

<p align="center">
  <img src="https://github.com/n0rs4rt/ORS4SysInfo/blob/39884a04537b5742fb5e87bbb440316f99294a6f/assets/busqueda.png" alt="ORS4SysInfo - Portada" width="900">
</p>


El nombre personalizado puede editarse desde el menú contextual del equipo y guardarse presionando Enter.

---

## Notas por equipo

<p align="center">
  <img src="https://github.com/n0rs4rt/ORS4SysInfo/blob/250c12b31cf1cf3b7a57c1f6777f0b0206f737b0/assets/Notas.png" alt="ORS4SysInfo - Portada" width="900">
</p>


Cada equipo cuenta con un apartado de notas donde se puede guardar información adicional, observaciones o detalles útiles.

Ejemplo de uso:

* Estado del equipo.
* Ubicación física.
* Responsable.
* Observaciones técnicas.
* Historial de intervención.
* Detalles pendientes.

Si un equipo ya registrado se vuelve a escanear, la información técnica se actualiza, pero las notas guardadas se mantienen.

---

## Reportes PDF

<p align="center">
  <img src="https://github.com/n0rs4rt/ORS4SysInfo/blob/2178553bbefae780e9c795cb87e6a55fed19c652/assets/PDF.png" alt="ORS4SysInfo - Portada" width="900">
</p>

ORS4SysInfo permite generar un reporte técnico en PDF para cada equipo registrado.

El reporte puede incluir información general del sistema, BIOS, placa base, procesador, discos, memorias RAM, adaptadores de red, tarjetas gráficas, usuarios registrados y notas asociadas.

Los reportes están pensados para documentación técnica, soporte, auditorías internas o entrega de información a otros técnicos.

---

## Configuración SMTP para envío de email

Para utilizar la función de envío de reportes por email es necesario configurar previamente una cuenta SMTP.

Por seguridad, ORS4SysInfo solo permite configuraciones SMTP con conexión segura, como SSL o TLS. No se recomienda ni se permite el uso de configuraciones sin cifrado para el envío de correos.

En servicios como Gmail, Outlook, Microsoft 365 u otros proveedores similares, puede ser necesario generar una contraseña de aplicación para poder utilizar SMTP. Esto depende de las políticas de seguridad del proveedor, especialmente cuando la cuenta tiene autenticación en dos pasos o restricciones para aplicaciones externas.

<p align="center">
  <img src="https://github.com/n0rs4rt/ORS4SysInfo/blob/4d685456bf87b5e22a9e5234741c7e092ed3a56c/assets/config_email.png" alt="ORS4SysInfo - Portada" width="400">
</p>

En servidores de correo propios o corporativos, este requisito casi siempre no es necesario sin embargo puede variar según la configuración del servidor SMTP.

Las credenciales SMTP se guardan localmente en el equipo y son cifradas por la propia aplicación. La contraseña no se almacena en texto plano. ORS4SysInfo cifra y descifra la información únicamente cuando es necesario para realizar el envío del reporte.

La aplicación no envía, almacena ni comparte estas credenciales en servicios externos.

---
## Envío de reportes por email

La aplicación permite generar un reporte PDF y enviarlo por email directamente desde la interfaz (Para enviarlo a mas de un destinatario sera necesario separar los email por , o ; ).

La ventana de envío permite indicar:

* Destinatario.
* CC opcional.
* Asunto.
* Mensaje.
* Archivo PDF adjunto.

El reporte se genera automáticamente y se adjunta al mensaje (Si se realiza click sobre el reporte es posible visualizarlo antes de enviarlo).

<p align="center">
  <img src="https://github.com/n0rs4rt/ORS4SysInfo/blob/2178553bbefae780e9c795cb87e6a55fed19c652/assets/email.png" alt="ORS4SysInfo - Portada" width="400">
</p>


---

## Copias de seguridad

ORS4SysInfo permite exportar e importar la base de datos local.

Esto permite:

* Crear copias de seguridad.
* Restaurar registros.
* Mover información entre instalaciones.
* Conservar inventarios técnicos.
* Recuperar datos en caso de pérdida o reinstalación.

Antes de importar una base de datos, se recomienda realizar una copia de seguridad de la base actual.
Despues de importar una base de datos es necesario reiniciar la aplicacion para que dichos datos carguen

---

## Consideraciones importantes

### Seriales de discos NVMe, M.2 y externos

En algunos discos NVMe, M.2 o discos conectados mediante adaptadores externos, el número de serie obtenido puede no coincidir exactamente con el mostrado por herramientas como CrystalDiskInfo, Hard Disk Sentinel u otras utilidades de analisis avanzados de discos.

Esto puede ocurrir porque la información se obtiene mediante WMI y depende de cómo Windows, el controlador del dispositivo, el firmware del disco o el adaptador USB/SATA/NVMe expongan los datos al sistema.

En discos HDD o SSD SATA internos, normalmente el serial suele obtenerse de forma más directa, confiable y consistente.

En discos externos, algunos adaptadores pueden interferir y mostrar datos del puente USB o del controlador en lugar del serial real del disco.

<p align="center">
  <img src="https://github.com/n0rs4rt/ORS4SysInfo/blob/1183e20a735c275641d389205a5254377dd9a3b0/assets/serial%20discos.png" alt="ORS4SysInfo - Portada" width="900">
</p>

---

### Fallos críticos de disco

El estado de fallos críticos no equivale a un análisis SMART completo.

Esta información indica si se detecta un estado crítico o fallo grave reportado por el dispositivo.
No debe interpretarse como una revisión completa de sectores dañados, desgaste, temperatura, vida útil o salud detallada del disco.

Para un diagnóstico profundo del disco se recomienda utilizar herramientas especializadas.

---

### BIOS y placa base

La información de BIOS y placa base depende de los datos expuestos por el fabricante y por WMI.

Algunos campos pueden no estar disponibles, aparecer como desconocidos o no aplicables, especialmente en:

* Máquinas virtuales.
* Equipos antiguos.
* Equipos con BIOS limitada.
* Fabricantes que no exponen correctamente la información.

---

### Adaptadores de red

La velocidad mostrada para los adaptadores de red corresponde a la velocidad reportada por Windows en el momento de la consulta.

La velocidad depende de que el adaptador esté conectado a una red activa.
Si el adaptador está desconectado, deshabilitado o sin enlace, la velocidad no sera mostrada.

---

<p align="center">
  <img src="https://github.com/n0rs4rt/ORS4SysInfo/blob/eecd09e696c9b9522e285d334b35d6891b3de19c/assets/graficas.png" alt="ORS4SysInfo - Portada" width="900">
</p>


### Tarjetas gráficas

La aplicación puede detectar tanto tarjetas gráficas dedicadas como integradas, siempre que Windows y los drivers correspondientes expongan correctamente la información.

En algunos casos, una GPU integrada puede aparecer con una capacidad de 128 MB.
Esto suele representar una reserva mínima de memoria compartida con el sistema y no necesariamente la memoria total disponible dinámicamente.

Para la detección es necesario tener instalados los drivers gráficos correctos.

---

### Licencia de Windows

Por seguridad, ORS4SysInfo no muestra la licencia completa de Windows.
Cuando la información está disponible, solo se muestran los últimos caracteres.

En algunos equipos puede no obtenerse esta información. Esto puede depender del tipo de activación, licencia digital, licencia OEM, activación por volumen, o datos disponibles mediante WMI.

Que no se muestre una licencia no significa necesariamente que Windows no esté activado.

---

## Requisitos recomendados

* Windows 10 22H2 o Windows 11.
* Resolución mínima: 1500x800.
* Permisos de administrador para consultar información del sistema.
* Drivers instalados correctamente para una mejor detección de hardware.
* Conexión de red activa si se desea obtener velocidad real de adaptadores conectados.
* Configuración SMTP válida si se desea enviar reportes por email.

---

## Compatibilidad

ORS4SysInfo está pensado principalmente para equipos Windows recientes.

Puede funcionar en equipos más antiguos, pero algunos datos podrían no obtenerse correctamente debido a limitaciones del sistema, controladores, firmware o información expuesta por WMI.

El proyecto ha sido probado en equipos con Windows 8, Windows 10 y Windows 11, aunque se recomienda utilizar versiones recientes de Windows 10 o Windows 11 para obtener mejores resultados.

---

## Uso general

1. Ejecutar la aplicación.
2. Seleccionar la opción de escaneo.
3. Esperar a que ORS4SysInfo recopile la información técnica del equipo.
4. El equipo quedará registrado automáticamente en la base de datos local.
5. Consultar el registro desde el panel lateral.
6. Agregar notas si es necesario.
7. Exportar el reporte en PDF o enviarlo por email.
8. Crear copias de seguridad de la base de datos cuando sea necesario.

---

## Seguridad y privacidad

ORS4SysInfo está diseñado para recopilar información técnica útil para inventario y soporte.

La aplicación no debe utilizarse en equipos sin autorización.
La información obtenida puede incluir datos técnicos sensibles como seriales, identificadores de hardware, nombres de usuarios locales, direcciones MAC y datos parciales de licencia.

Se recomienda utilizar la herramienta únicamente en entornos propios, corporativos o donde exista autorización explícita.

---

## Licencia

<p align="center">
  <img src="https://github.com/n0rs4rt/ORS4SysInfo/blob/93516f6acc63ff0c263cfdba7bca4c3d704eb853/assets/acerca_de.png" alt="ORS4SysInfo - Portada" width="300">
</p>

Este proyecto está licenciado bajo MIT License.

Esto permite usar, estudiar, modificar y distribuir el código, manteniendo los créditos correspondientes del autor original.

Consultar el archivo LICENSE para más información.

Desarrollado por Nelson Arteaga.

ORS4TECH
GitHub oficial: https://github.com/n0rs4rt

---

## Aviso

La información mostrada por la aplicación depende de los datos expuestos por Windows, WMI, drivers, firmware y fabricantes de hardware.

Algunos valores pueden aparecer como desconocidos, no aplicables o variar respecto a herramientas especializadas.
ORS4SysInfo está orientado al inventario técnico y documentación general, no reemplaza herramientas avanzadas de diagnóstico de hardware.
