# Taller 2 · Agente conversacional con memoria y tools

Este material conserva la dinámica del notebook guiado y añade tres piezas:

- una base de datos local SQLite para guardar historial y recuerdos;
- tools propias que el modelo puede solicitar y que Python ejecuta;
- una tool de clima actual conectada a Open-Meteo, sin API key;
- una interfaz gráfica Gradio que se abre en el navegador desde la última celda.

## Preparación en macOS

Desde esta carpeta ejecuta:

    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    python -m ipykernel install --user --name taller-2-agente --display-name "Python (Taller 2 Agente)"

Luego copia .env.example como .env y coloca una API key válida:

    cp .env.example .env

No compartas .env ni la API key.

Abre taller_2_agente_grafico_memoria_tools_v3.ipynb, selecciona el kernel
Python (Taller 2 Agente) y ejecuta las celdas en orden. La última celda
abre el chat gráfico en el navegador.

La versión v3 divide la construcción del agente en pruebas progresivas:
agente sin memoria, memoria temporal, memoria SQLite sin tools, tools de
guardar y leer recuerdos, hora local, clima con Open-Meteo y chat gráfico.
La versión v2 se conserva como referencia compacta.

La base alter_ego_memory.db se crea automáticamente junto al notebook y
puede inspeccionarse con las celdas de diagnóstico. Para reiniciar los
recuerdos desde la interfaz se usa el botón Borrar memoria.
