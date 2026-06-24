# ORS4SysInfo



<!-- ![ORS4SysInfo - Portada](https://github.com/n0rs4rt/ORS4SysInfo/blob/685b5af870dea869c6e13e22faa48e24b87dd8f7/assets/portada.png) -->

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

<!-- TODO: Colocar aquí una captura general de la interfaz principal -->

<!-- Ejemplo: -->

<!-- ![Interfaz principal](docs/images/interfaz-principal.png) -->

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

El nombre personalizado puede editarse desde el menú contextual del equipo y guardarse presionando Enter.

---

## Notas por equipo

<!-- TODO: Colocar aquí una captura del apartado de notas -->

<!-- Ejemplo: -->

<!-- ![Notas por equipo](docs/images/notas-equipo.png) -->

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

<!-- TODO: Colocar aquí una captura del botón de exportar PDF o ejemplo de reporte -->

<!-- Ejemplo: -->

<!-- ![Reporte PDF](docs/images/reporte-pdf.png) -->

ORS4SysInfo permite generar un reporte técnico en PDF para cada equipo registrado.

El reporte puede incluir información general del sistema, BIOS, placa base, procesador, discos, memorias RAM, adaptadores de red, tarjetas gráficas, usuarios registrados y notas asociadas.

Los reportes están pensados para documentación técnica, soporte, auditorías internas o entrega de información a otros técnicos.

---

## Envío de reportes por email

<!-- TODO: Colocar aquí una captura de la ventana de envío por email -->

<!-- Ejemplo: -->

<!-- ![Enviar reporte por email](docs/images/enviar-email.png) -->

La aplicación permite generar un reporte PDF y enviarlo por email directamente desde la interfaz.

La ventana de envío permite indicar:

* Destinatario.
* CC opcional.
* Asunto.
* Mensaje.
* Archivo PDF adjunto.

El reporte se genera automáticamente y se adjunta al mensaje.

---

## Copias de seguridad

<!-- TODO: Colocar aquí una captura de exportación/importación de base de datos -->

<!-- Ejemplo: -->

<!-- ![Copias de seguridad](docs/images/copias-seguridad.png) -->

ORS4SysInfo permite exportar e importar la base de datos local.

Esto permite:

* Crear copias de seguridad.
* Restaurar registros.
* Mover información entre instalaciones.
* Conservar inventarios técnicos.
* Recuperar datos en caso de pérdida o reinstalación.

Antes de importar una base de datos, se recomienda realizar una copia de seguridad de la base actual.

---

## Consideraciones importantes

### Seriales de discos NVMe, M.2 y externos

En algunos discos NVMe, M.2 o discos conectados mediante adaptadores externos, el número de serie obtenido puede no coincidir exactamente con el mostrado por herramientas como CrystalDiskInfo, Hard Disk Sentinel u otras utilidades de analisis avanzados de discos.

Esto puede ocurrir porque la información se obtiene mediante WMI y depende de cómo Windows, el controlador del dispositivo, el firmware del disco o el adaptador USB/SATA/NVMe expongan los datos al sistema.

En discos HDD o SSD SATA internos, normalmente el serial suele obtenerse de forma más directa, confiable y consistente.

En discos externos, algunos adaptadores pueden interferir y mostrar datos del puente USB o del controlador en lugar del serial real del disco.

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

## Imágenes del proyecto

<!-- TODO: Colocar aquí una galería de capturas del programa -->

<!-- Captura 1: Portada o pantalla inicial -->

<!-- ![Pantalla inicial](docs/images/pantalla-inicial.png) -->

<!-- Captura 2: Interfaz principal con equipo seleccionado -->

<!-- ![Equipo seleccionado](docs/images/equipo-seleccionado.png) -->

<!-- Captura 3: Ventana de envío por email -->

<!-- ![Enviar reporte por email](docs/images/enviar-email.png) -->

<!-- Captura 4: Ventana Acerca de -->

<!-- ![Acerca de](docs/images/acerca-de.png) -->

<!-- Captura 5: Reporte PDF generado -->

<!-- ![Reporte PDF](docs/images/reporte-pdf.png) -->

---

## Seguridad y privacidad

ORS4SysInfo está diseñado para recopilar información técnica útil para inventario y soporte.

La aplicación no debe utilizarse en equipos sin autorización.
La información obtenida puede incluir datos técnicos sensibles como seriales, identificadores de hardware, nombres de usuarios locales, direcciones MAC y datos parciales de licencia.

Se recomienda utilizar la herramienta únicamente en entornos propios, corporativos o donde exista autorización explícita.

---

## Licencia

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
