# Lines Counter

- Versión recomendada de Python: 3.11

## Instalar el entorno (Antes de ejecutar el programa):

1. Crear el entorno de desarrollo:

```bash
python3 -m venv env
```

2. Activar el entorno de desarrollo:

En `Windows`:

```bash
env\Scripts\activate
```

En `Unix/Linux` o `MacOS`:

```bash
source env/bin/activate
```

3. Instalar las dependencias:

```bash
pip install -r requirements.txt

pre-commit install
```

4. Copiar el contenido del archivo `example.env` a un archivo `.env` y rellenar las variables necesarias para correr el proyecto.

```bash
cp example.env .env
```

## Correr los tests del sistema:

Para ejecutar los tests unitarios y de integración basta con ejecutar:

```bash
python -m unittest discover -s tests -p "*_tests.py"
```

## Generar el ejecutable - Solo para windows
Para generar el ejecutable, basta con ejecutar:

```bash
pyinstaller --onefile --name LinesCounter run_app.py
```
El ejecutable podras visualizarlo dentro del directorio `dist` generado por el comando

## Correr el sistema en modo user-friendly:

Para ejecutar el sistema en modo prompt basta con ejecutar:

```bash
python -m src.main
```

## Instalar como librería:

Es posible descargar el programa como librería para utilizarla en otros programas, para ello, basta con ejecutar:

```bash
pip install lines-counter
```

Importar las funciones necesarias en tu proyecto:

```py
from lines_counter import count_logical_lines_from_project
from lines_counter import count_physical_lines_from_project
from lines_counter import count_changes_from_project
from lines_counter import format_files_from_project
```
