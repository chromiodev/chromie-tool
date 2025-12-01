# Guía para el asistente de IA (Gemini)

Este documento proporciona el contexto técnico esencial para que el asistente de IA colabore eficazmente en el proyecto **Chromie**.


## Descripción general del proyecto

**Chromie** es una herramienta de línea de comandos (CLI) para facilitar la importación y exportación de datos desde y hacia una base de datos vectorial **Chroma**.

El proyecto está diseñado con una clara separación de responsabilidades:

- **chromie/**:
  Contiene la aplicación CLI que el usuario final ejecuta.
  Se encarga de analizar los argumentos de la línea de comandos y de orquestar las operaciones.
  Utiliza la librería **chromio**.

- **chromio/**:
  Contiene la librería principal con toda la lógica de negocio.
  Puede ser utilizada de forma independiente en otros proyectos.
  Se encarga de la interacción con **Chroma**, la lógica de importación/exportación, el manejo de URIs, etc.


## Pila tecnológica

- **Lenguaje**: Python 3.14+

- **Gestor de dependencias y entorno**: Poetry

- **Framework CLI**: parseargs

- **Formateo y linting**: Ruff

- **Chequeo de tipos estáticos**: Pyright

- **Pruebas automatizadas**: pytest

- **Base de datos principal**: Chroma


## Estructura del proyecto

```
.
├── chromie/         # Aplicación CLI (puntos de entrada y comandos)
│   ├── app.py       # Punto de entrada principal de la CLI
│   └── cmds/        # Módulos para cada comando (ej: list, exp)
│
├── chromio/         # Librería principal con la lógica de negocio
│   ├── client/      # Lógica para crear y gestionar clientes de Chroma
│   ├── ie/          # Lógica de importación/exportación (Import/Export)
│   └── uri/         # Utilidades para analizar URIs de conexión a Chroma
│
├── tests/
│   ├── functional/  # Pruebas funcionales end-to-end de la CLI
│   └── unit/        # Pruebas unitarias de la librería chromio
│
├── .gemini/         # Contexto y guías para el asistente de IA
├── pyproject.toml   # Definición del proyecto, dependencias y configuración de herramientas
└── ...
```


## Flujo de Trabajo para Contribuciones

01. **Crea una rama**:
    Empieza desde **main** y crea una nueva rama descriptiva.

    ```bash
    git checkout -b desarrollador/feat/nombre-de-la-funcionalidad
    ```

02. **Implementa los cambios**:
    Realiza las modificaciones necesarias en el código.

03. **Añade o actualiza las pruebas**:
    Asegúrate de que los cambios están cubiertos por pruebas unitarias, integrales o funcionales en el directorio **tests/**.

04.  **Verifica la calidad del código**:
    Antes de hacer la confirmación, ejecuta las herramientas de calidad.

    ```bash
    ruff format .
    ruff check .
    pyright
    ```

05. **Ejecuta todas las pruebas**: Confirma que tus cambios no han roto ninguna funcionalidad existente.

    ```bash
    pytest
    ```

06. **Realiza la confirmación**:
    Escribe un mensaje de commit claro y conciso.


## Guía de estilo

El proyecto tiene una guía de estilo a seguir en todas las contribuciones.
Se encuentra disponible en el archivo **docs/styleguide.es.md**.
