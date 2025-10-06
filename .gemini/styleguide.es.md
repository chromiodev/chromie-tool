# Guía de Estilo


## Introducción

Este documento establece las convenciones de codificación y las guías de estilo a tener en cuenta.
El objetivo es mantener un código limpio, legible y consistente en todo el proyecto.
La adhesión a estas reglas es obligatoria para todos los contribuidores.


## Herramientas de Calidad de Código

La consistencia se logra principalmente a través de herramientas automáticas.
Antes de confirmar cualquier cambio, hay que asegurarse de que el código no presente errores con las siguientes herramientas:

- **`Ruff`**: Para formateo de código y linting.

- **`Pyright`**: Para el análisis y chequeo de tipos estáticos.

La configuración de estas herramientas se encuentra en los archivos **.ruff.toml**, **ruff.format.toml** y **pyrightconfig.json**.


## Formato de Código

- **Formateador automático**: Todo el código **Python** debe ser formateado usando el comando **`ruff format`**.

- **Longitud de línea**: Se establece un máximo de 90 caracteres por línea.

- **Indentación**: Usar 2 espacios por nivel de indentación.


## Convenciones de Nomenclatura

- **Clases**: Usar **PascalCase** (ej. *`ChromieArgParser`*, *`CollExporter`*).

- **Funciones, Métodos y Variables**: Usar `snake_case` (ej. `parse_args_and_run()`, `file_path()`).

- **Módulos y Miembros "Privados"**: Prefijar con un guion bajo (`_`) los módulos, funciones o variables que no están destinados a ser utilizados fuera de su ámbito directo (ej. `_client.py`).

- **Constantes**: Usar `UPPER_SNAKE_CASE` para constantes a nivel de módulo (ej. `DEFAULT_TIMEOUT = 60`).


## Tipado Estático (*static typing*)

- **Obligatorio**: Todo el código nuevo debe incluir sugerencias de tipo.

- **Claridad**: Utiliza los tipos más específicos posibles (ej. `list[str]` en lugar de `list`).
  Para uniones, se usará el formato `int | None` en vez de `Optional[int]`.

- **Verificación**: El código debe pasar la verificación de **pyright** sin errores.


## Documentación (*docstrings*)

- **Formato**:
  Las cadenas de documentación deben seguir un estilo similar al de **Google**.
  Deben ser claras y concisas.

- **Estructura**:

    01. Un resumen de una línea que describe el propósito de la función o clase.

    02. Un párrafo más detallado si fuera necesario.

    03. Una sección **Args:** para describir los argumentos.

    04. Una sección **Returns:** para describir el valor de retorno.

    05. Una sección **Raises:** para describir las excepciones propagadas.

- **Ejemplo**:

  ```python
    async def export(
    self,
    coll: AsyncCollection,
    file: Path,
    limit: int | None = None,
    metafilter: dict | None = None,
  ) -> CollExportRpt:
    """Exports a collection to a file.

    Args:
      coll: Collection to export.
      file: File path where to save the export.
      limit: Maximum number of records to export.
      metafilter: Filter by metadata.

    Returns:
      An export report.
    """
  ```


## Pruebas

- **Framework**:
  Se utiliza **pytest** para *todas* las pruebas automatizadas.

- **Ubicación**:

    - **tests/unit**: Para las pruebas unitarias.

    - **tests/integration**: Para las pruebas de integración.

    - **tests/functional**: Para las  pruebas funcionales.

- **Nomenclatura de las pruebas**:
  Los nombres de los archivos de prueba deben seguir el patrón **\*_test.py**.
  Para evitar conflictos de nombres, los archivos de las pruebas de integración deben llevar el prefijo **itg_** y las funcionales **fn_**.
  A las unitarias no hay que aplicar ningún afijo en especial.
  
  Las funciones de prueba deben comenzar con **test_**.

- **Estructura de las pruebas**: Sigue el patrón **AAA(C)** (*arrange, act, assessment, cleanup*).
  Cada bloque precederse con un comentario que lo identifique.
  Ejemplo:

  ```python
  async def test_server_client(mocker: MockerFixture) -> None:
    """Check that client() returns a asynchronous client."""

    # (1) arrange
    AsyncHttpClient = mocker.patch(
      "chromio.client._client.AsyncHttpClient", new_callable=mocker.AsyncMock
    )

    # (2) act
    out = await client(ChromioUri.server())

    # (3) assessment
    assert isinstance(out, AsyncMockType)
    assert AsyncHttpClient.await_count == 1
  ```

- **Fixtures**:
  Se recomienda el uso de *fixtures* de **pytest** para las secciones de preparación (*arrange*) y limpieza (*cleanup*).

- **Mocks**:
  Para la creación de dobles de prueba (*mocks*, *stubs*, etc.), se debe utilizar el componente **pytest-mock**.
  No está permitido el uso directo de **`unittest.mock`**.

- **Datos de prueba**:
  Los datos sintéticos se generarán con el complemento de **pytest** integrado en **Faker**.

- **Marcadores personalizados**:
  
  - ***`pytest.mark.readonly`*** para identificar pruebas de integración y funcionales de sólo lectura.
    Las pruebas de que no presenten esta marca se consideran de L/E.

  - ***`pytest.mark.attr(id="FT-componente-número")`*** para vincular una prueba funcional con su identificador en el documento de especificación.


## Importaciones

- **Orden**: Las importaciones deben ser agrupadas en el siguiente orden, separadas por una línea en blanco:

  01. Librerías estándar de **Python** (ej. ***`asyncio`***, ***`json`***, etc.).

  02. Librerías de terceros (ej. ***`pytest`***, ***`chromadb`***...).

  03. Módulos de la aplicación (***`chromie`***, ***`chromio`***).

- **Estilo**:
  Se recomiendan las importaciones directas (***`from module import name`***) en lugar de importar el módulo completo (***`import module`***).


## Mensajes de confirmación de Git

Para mantener un historial de confirmaciones limpio y navegable, se sugiere seguir la especificación de [Conventional Commits](https://www.conventionalcommits.org/):

```
tipo(componente o ámbito): descripción
```
