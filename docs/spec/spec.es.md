# Especificación del proyecto *Chromie*


## Introducción

**Chroma** se está consolidando como un sistema de gestión de bases de datos vectoriales de referencia por su simplicidad y potencia.
Sin embargo, se ha identificado una carencia en las herramientas de importación y exportación de datos.
La interfaz de línea de comandos (CLI) actual de **Chroma** no permite el almacenamiento de datos en archivos portables, limitando su uso a la migración entre instancias.

El presente documento detalla el diseño y los requisitos del proyecto **Chromie** (*Chroma Import/Export*), una herramienta CLI de código abierto concebida para abordar esta necesidad.
Su propósito es proporcionar una interfaz intuitiva para importar y exportar registros de colecciones de **Chroma** a archivos **JSON** estandarizados, tanto para instancias locales como remotas y **Chroma Cloud**.

El propósito de este documento es servir como punto de referencia central para entender el proyecto, su alcance y sus requisitos.


## Visión del proyecto

Una aplicación de línea de comandos diseñada para importar y exportar colecciones de **Chroma** a un formato de archivo **JSON** estándar, facilitando la portabilidad y el respaldo de los datos.

### Audiencia

- Desarrolladores

- DBAs

- MLOps

### Licencia

El proyecto se publica bajo la licencia **GNU General Public License v3.0** (**GPLv3**), garantizando así que cualquier trabajo derivado permanezca como software de código abierto (**OSS**).


## Requisitos funcionales

La aplicación expone su funcionalidad a través de una interfaz de línea de comandos (CLI) que permite a los usuarios interactuar con bases de datos **Chroma**.

### Casos de uso

[use-cases.md](use-cases.es.md)

### Variables de entorno soportadas

Las siguientes variables de entorno se utilizan para configurar la conexión a la base de datos:

Variable | Descripción
:--: | :--
CHROMA_HOST | Servidor al que conectar.
CHROMA_PORT | Puerto del servidor al que conectar.
CHROMA_API_KEY | Clave de API a usar con Chroma Cloud.
CHROMA_TENANT | Identificador del tenedor de la BD.
CHROMA_DATABASE | Nombre de la BD.

### Esquema de datos

El formato de archivo de importación y exportación se adhiere al esquema, escrito con **JSON Schema**, disponible en el archivo [schema.json](schema.json).

### Formato de las cadenas de conexión

Las cadenas de conexión de la URI se definen de la siguiente manera:

Tipo | URI
:--: | :--
Local | path:///ruta/al/directorio/persistente
Servidor | server://nombre:puerto/tenedor/bd/colección
Chroma Cloud | cloud:///tenedor/bd/colección


## Requisitos no funcionales

Estos requisitos establecen los atributos de calidad, las restricciones y las dependencias técnicas del proyecto:

Requisito | Descripción
:--: | :--
IDE | VS Code
Modelado | UML (con Mermaid)
Plataforma | Python 3.13+
Concurrencia | asyncio
Sistemas operativos | Linux, Windows, macOS
Gestión de paquetes | Poetry
Linter | Ruff
Formateo | Ruff
Comprobación de tipos | Pyright
Pruebas | pytest
Cobertura | 100% con pytest-cov
Documentación de este documento | Español, inglés
CI/CD | GitHub Actions
Chroma | chromadb


## Gestión del proyecto

Para mantener un proyecto saludable y fomentar una comunidad activa, se han definido las siguientes pautas de gestión.

### Roles

- **Mantenedor**: Rol asumido por el equipo inicial de desarrollo.
  Es responsable de la dirección a largo plazo del proyecto.
  Un mantenedor revisa los *pull requests*, aprueba el código, gestiona el triaje de incidencias y es el contacto principal para la comunidad.

- **Colaborador**: Cualquier persona que envía una contribución al proyecto, ya sea un informe de error, una corrección de código o una mejora en la documentación.

- **Colaborador Principal**: Un colaborador que ha demostrado un compromiso constante y ha realizado contribuciones significativas y de alta calidad.
  Es posible que obtengan permisos adicionales para ayudar con la revisión de código o la gestión del triaje.

### Etiquetas de *GitHub*

Las etiquetas de **GitHub** se utilizarán para clasificar y organizar las incidencias y solicitudes de cambio.
Esto facilitará la búsqueda y el seguimiento de las tareas tanto para los colaboradores existentes como para los nuevos.
Estas serán:

- **Estado**: *pending triage*, *in progress*, *on hold*, *duplicate*.

- **Tipo**: *bug*, *feature* (para nuevas funcionalidades), *doc* (para mejoras en la documentación).

- **Prioridad**: *p:low*, *p:medium*, *p:high*, *p:critical*.

- **Esfuerzo**: *s:xs*, *s:s*, *s:m*, *s:l*, *s:xl*.

### Proceso de aceptación de incidencias

Se seguirá un proceso claro para la aceptación de incidencias con el objetivo de optimizar el flujo de trabajo:

01. **Revisión/triaje**: Un **mantenedor** revisará y validará las nuevas incidencias.
    Consiste en:

    - **Validar**: Comprobar que la información es clara y completa.
      Si es un *bug*, verificar que se puede reproducir.
      Si no es así, se pedirá al autor más información.

    - **Identificar duplicados**: Revisar si el problema ya ha sido reportado en otra incidencia.
      Si es el caso, se cierra la nueva incidencia (marcándose como *duplicate*) y se enlaza a la original.

    - **Clarificar**: Actuar como punto de contacto principal para aclarar dudas o solicitar información adicional del autor antes de que la incidencia sea asignada.

02. **Etiquetado**: Una vez validada, un **mantenedor** aplicará las etiquetas adecuadas para categorizar la incidencia.
    El objetivo es que cualquier colaborador pueda, de un vistazo, entender la naturaleza, prioridad y dificultad de la tarea.

03. **Asignación**: Tras el etiquetado, la incidencia está lista para ser atendida.
    Un **mantenedor** la asignará a un colaborador interesado o a sí mismo, dándole el pistoletazo de salida para su implementación.

Este proceso asegura que las contribuciones sean eficientes y que los colaboradores sepan en todo momento el estado de las tareas.


## Proceso de creación de un nuevo comando a *chromie*

A continuación, se describe el proceso para la añadidura de un nuevo comando a **chromie**:

01. Añadir los casos de uso correspondientes en el documento [use-cases.es.md](use-cases.es.md).

02. Modificar el documento de diseño [design.es.md](design.es.md).

03. Modificar el documento de esquema [schema.json](schema.json) si fuera necesario.

04. Añadir las pruebas de integración si fueran necesarias a [tests/integration.es.md](tests/integration.es.md).

05. Añadir las pruebas funcionales [tests/functional.es.md](tests/functional.es.md).


## *Gemini* y *Gemini Code Assist*

Este proyecto utiliza **Gemini** y **Gemini Code Assist** para apoyarse en su desarrollo y la traducción a distintos idiomas de los documentos del directorio **docs/spec/**.
La configuración específica de **Gemini Code Assist** se encuentra en el directorio **.gemini** del proyecto y es un buen punto de partida, junto a este y otros documentos, para nuevos colaboradores.
También podemos encontrar configuración en **vscode/settings.json**.


## Otros documentos

- **Guía de estilo**, [../styleguide.es.md](../styleguide.es.md).

- **Documento de diseño: Chromie**, [design.es.md](design.es.md).

- **Pruebas de integración**, [tests/integration.es.md](tests/integration.es.md).

- **Pruebas funcionales**, [tests/functional.es.md](tests/functional.es.md).
