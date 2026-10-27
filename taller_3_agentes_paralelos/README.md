# Taller 3 · Tres agentes especializados

Proyecto corto de Python para dar una tarea común a uno, dos y tres agentes con estilos diferentes. Todos reciben una herramienta común y cada agente tiene una herramienta propia. Los tres usan el mismo modelo de OpenAI.

## Archivos

- `agentes_paralelos.py`: programa único con los pasos 1, 2 y 3, tools y campos de personalización señalados.
- `agentes_gui.py`: interfaz gráfica opcional para elegir el modo, cambiar la tarea y ver los logs en vivo.
- `MANUAL_DE_CLASE.md`: guía del docente para una lección de 45 minutos, con preparación, tiempos, explicación del ciclo de tools y pruebas.
- `.env.example`: plantilla para configurar la API key sin escribirla en el código.

## Preparación rápida

Abre esta carpeta en Visual Studio Code. Desde la terminal, crea y activa un entorno virtual, e instala las dependencias:

```bash
python -m venv .venv
```

En macOS o Linux:

```bash
source .venv/bin/activate
```

En Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Luego, en cualquier sistema:

```bash
python -m pip install -r requirements.txt
```

Copia `.env.example` como `.env` y escribe tu API key después de `OPENAI_API_KEY=`. El archivo `.env` está excluido de Git.

## Ejecutar

Abre `agentes_paralelos.py`. Empieza con `MODO = 1`; después cambia a `MODO = 2` y finalmente a `MODO = 3`. Guarda y ejecuta el programa cada vez:

```bash
python agentes_paralelos.py
```

La terminal muestra cuándo cada agente solicita una tool, qué resultado devuelve y cuál es su respuesta final. Los campos que se pueden personalizar están al principio del archivo, debajo de `# PERSONALIZA AQUÍ`.

### Interfaz gráfica opcional

Desde esta carpeta, ejecuta:

```bash
python agentes_gui.py
```

La ventana permite elegir 1, 2 o 3 agentes, editar la tarea y ver en vivo los logs de cada agente. También imprime esos logs en la terminal desde la que se inició. Tkinter viene con muchas instalaciones de Python; si no está disponible, usa el modo de terminal.

Cada agente usa `consultar_reto_comun` y su propia herramienta especial. La salida muestra cuáles herramientas usó cada agente y qué devolvió cada una.

Consulta [MANUAL_DE_CLASE.md](MANUAL_DE_CLASE.md) para seguir la lección de 45 minutos.
