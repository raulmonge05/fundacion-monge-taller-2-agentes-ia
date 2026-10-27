# Manual de clase · Agentes con tools en 45 minutos

## Propósito

El grupo continúa desde los talleres anteriores: en el taller 1 armó un agente visual en n8n y en el taller 2 reconstruyó un agente en Python. Ahora dará la misma tarea a uno, dos y tres agentes especializados. Todos comparten una herramienta y cada agente tiene una herramienta distinta.

Al terminar, cada estudiante podrá:

1. Explicar qué es una tool y cómo se conecta con una función de Python.
2. Ejecutar una tarea con uno, dos y tres agentes.
3. Identificar la herramienta común y la herramienta particular de cada agente.
4. Cambiar instrucciones o resultados de tools y observar el efecto.
5. Reconocer que en los modos 2 y 3 los agentes trabajan en paralelo.

## Preparación del docente

Completa estos pasos antes de iniciar los 45 minutos:

1. Confirma que cada computadora tiene Python y Visual Studio Code.
2. Abre la carpeta `taller_3_agentes_paralelos` en Visual Studio Code.
3. Crea el entorno e instala las dependencias siguiendo el `README.md`.
4. Copia `.env.example` como `.env` y configura la API key autorizada para la clase. No la pongas en el código ni la compartas en una captura o repositorio.
5. Ejecuta el programa una vez en modo 1 para confirmar que el entorno está listo.
6. Si vas a mostrar la ventana gráfica, confirma que esta instalación de Python incluye Tkinter.
7. Ten preparada la tarea de ejemplo y una alternativa.

Si las computadoras comparten una misma cuenta de API, organiza las ejecuciones del modo 3 por grupos para distribuir las solicitudes.

## Materiales

- Computadora con Visual Studio Code y Python.
- Carpeta del proyecto descargada o compartida localmente.
- Acceso autorizado a la API de OpenAI.
- Proyector para mostrar las instrucciones y comparar resultados.

## Guion de 45 minutos

| Minutos | Actividad | Guía para enseñar |
|---|---|---|
| 0–4 | Conectar con los talleres anteriores | Pregunta: “¿Qué hacía que el agente del taller 2 respondiera como el alter ego?” Recupera prompt y contexto. Presenta la tool como una función de Python que el agente puede pedir. |
| 4–9 | Paso 1: un agente | Deja `MODO = 1` y ejecuta. Observa la respuesta del poeta y el nombre y resultado de sus dos herramientas. |
| 9–15 | Seguir una tool | Explica el ciclo: el modelo pide una función; Python la ejecuta; Python devuelve el resultado; el modelo redacta con ese resultado. |
| 15–20 | Paso 2: dos agentes | Cambia a `MODO = 2`. Compara el poeta y el comediante: comparten una tool y cada uno recibe una herramienta especial. |
| 20–25 | Paso 3: tres agentes | Cambia a `MODO = 3`. Compara los tres resultados. `ThreadPoolExecutor` ejecuta las secuencias de los agentes en paralelo. |
| 25–31 | Ver los logs en la interfaz | Ejecuta `python agentes_gui.py`. Elige un modo, edita la tarea si quieres y muestra cómo aparecen el agente, cada tool, el resultado devuelto y la respuesta final. |
| 31–38 | Personalizar | Cambia un estilo o el texto que devuelve una función. Ejecuta el modo 3 y observa qué cambió. |
| 38–43 | Pruebas rápidas | Prueba una tarea nueva o cambia el contexto común. Identifica qué herramienta aportó una idea útil a cada respuesta. |
| 43–45 | Cierre | Pide compartir un cambio y su resultado. Cierra con la idea: la herramienta devuelve información o una idea; el agente la usa siguiendo sus instrucciones. |

## Paso a paso del programa

### Paso 1: ejecutar un agente

En `agentes_paralelos.py`, deja:

```python
MODO = 1
```

En la terminal de VS Code, ejecuta:

```bash
python agentes_paralelos.py
```

La terminal va mostrando los eventos con hora: inicio, solicitud de cada tool, resultado que devuelve Python y respuesta final del agente.

El poeta recibe la tarea, consulta la herramienta común y luego la herramienta especial `proponer_metafora`. Al final aparecen las herramientas, sus resultados y la respuesta final.

### Paso 2: conocer las herramientas

El programa ofrece estas funciones de Python como tools:

| Agente | Herramienta común | Herramienta especial |
|---|---|---|
| Poeta | `consultar_reto_comun`: devuelve el contexto ficticio del reto comunitario. | `proponer_metafora`: aporta una metáfora para la historia. |
| Comediante | `consultar_reto_comun`: devuelve el mismo contexto. | `proponer_broma_amable`: aporta una idea graciosa sin burlarse de nadie. |
| Narrador | `consultar_reto_comun`: devuelve el mismo contexto. | `crear_esquema_de_historia`: aporta inicio, problema y solución. |

El contexto es ficticio: el parque del barrio tiene poca sombra y estudiantes proponen un jardín de plantas nativas con asientos reutilizados.

En este ejemplo, el modelo no ejecuta Python. El modelo solicita una herramienta; el programa encuentra y ejecuta la función; después envía el resultado al modelo. El resultado queda vinculado a la llamada con su `call_id`. Por agente, el código hace tres solicitudes a la API: una para solicitar la herramienta común, otra para solicitar la herramienta especial y una final para redactar.

### Paso 3: ejecutar dos agentes

Cambia el modo:

```python
MODO = 2
```

Guarda y vuelve a ejecutar. El poeta y el comediante reciben la misma tarea y contexto. Cada uno usa una herramienta especial diferente.

### Paso 4: ejecutar tres agentes en paralelo

Cambia el modo:

```python
MODO = 3
```

Guarda y ejecuta otra vez. `ThreadPoolExecutor` coordina las secuencias de los tres agentes al mismo tiempo. Dentro de cada agente, las dos tools se ejecutan en orden antes de la respuesta final. El resultado muestra el nombre de cada agente, los resultados de sus tools y su respuesta.

## Personalización sencilla

Los campos principales están bajo `# PERSONALIZA AQUÍ` y en cada elemento de `AGENTES`:

- `nombre`: nombre mostrado en el resultado.
- `rol`: función o personalidad del agente.
- `estilo`: cómo debe sonar.
- `reglas`: formato o límites para su respuesta.
- `TAREA`: solicitud que reciben todos.
- `MODELO`: modelo compartido.
- `tool_especial`: nombre de su función particular.
- `descripcion_tool`: explica al modelo qué aporta esa tool.

El contexto común está en la función `consultar_reto_comun`. Cada resultado especial está en `proponer_metafora`, `proponer_broma_amable` o `crear_esquema_de_historia`. Para una primera prueba, cambia solo el texto de retorno de `proponer_metafora` y vuelve a ejecutar `MODO = 3`.

Si se cambia el nombre de una herramienta en `tool_especial`, también hay que actualizar ese nombre en `FUNCIONES_PYTHON`. Para la primera clase, se recomienda cambiar las descripciones y resultados; deja los nombres tal como están.

## Interfaz gráfica opcional

Desde la terminal, ejecuta:

```bash
python agentes_gui.py
```

En la ventana puedes elegir el número de agentes, editar la tarea común y pulsar **Ejecutar**. El panel **Actividad** muestra el progreso en vivo: qué agente solicita cada tool, el resultado de la función de Python y la respuesta final. Los mismos eventos también aparecen en la terminal. La ventana corre las solicitudes en segundo plano para mantenerse activa mientras esperan las respuestas.

La interfaz usa Tkinter, incluido en la biblioteca estándar de Python cuando la instalación lo ofrece. No se agrega una dependencia al archivo `requirements.txt`. Si aparece el mensaje de que Tkinter no está disponible, ejecuta `python agentes_paralelos.py` desde la terminal.

## Pruebas para la lección

Prueba una modificación a la vez:

1. Ejecuta `MODO = 1` y apunta qué aportó el contexto y la metáfora.
2. Ejecuta `MODO = 2` y compara la metáfora con la broma amable.
3. Ejecuta `MODO = 3` y observa qué añade el esquema del narrador.
4. Cambia el texto de `consultar_reto_comun`; ejecuta modo 3 y confirma que el nuevo contexto aparece en las tres respuestas.
5. Cambia una instrucción de estilo y compara de nuevo.

Ideas de tareas:

- “Explica qué es la inteligencia artificial con una comparación sencilla.”
- “Escribe un mensaje para invitar a cuidar un parque del barrio.”
- “Cuenta una historia corta sobre una idea que ayuda a la comunidad.”

Preguntas para conversar:

- ¿Qué información compartieron los tres agentes?
- ¿Qué idea aportó la herramienta exclusiva de cada agente?
- ¿Cuál siguió mejor su estilo y sus reglas?
- ¿Qué cambio pequeño haría más útil una tool?

## Problemas comunes

- **El programa dice que falta `OPENAI_API_KEY`:** confirma que `.env` está en esta carpeta y contiene `OPENAI_API_KEY=...`.
- **No encuentra `openai` o `dotenv`:** activa el entorno virtual de esta carpeta y ejecuta `python -m pip install -r requirements.txt`.
- **Error de autenticación o acceso:** pide al docente revisar que la key sea válida y tenga acceso al modelo.
- **La ventana informa que Tkinter no está disponible:** usa el programa de terminal o instala una distribución de Python que incluya Tkinter.
- **Error de nombre de herramienta:** si se modifica `tool_especial`, el nombre debe coincidir con una función registrada en `FUNCIONES_PYTHON`.
- **El resultado no parece cambiar:** guarda el archivo, cambia una sola instrucción o tool y vuelve a ejecutar el modo 3.
- **Se configura otro modo:** `MODO` acepta `1`, `2` o `3`.

## Cuidado de la API key y los datos

La API key es un secreto: se guarda en `.env`, nunca en el código. El proyecto excluye `.env` de Git. Usa tareas ficticias y no incluyas contraseñas, direcciones, datos médicos, información bancaria ni información privada de estudiantes.

## Referencias técnicas

- [Guía oficial de OpenAI: SDKs y CLI](https://developers.openai.com/api/docs/libraries): instalación del SDK de Python y uso de `client.responses.create`.
- [Guía oficial de function calling](https://developers.openai.com/api/docs/guides/function-calling): definición de tools, ejecución en la aplicación, `tool_choice` y devolución de resultados vinculados con `call_id`.
- [Referencia oficial de Responses API](https://developers.openai.com/api/reference/python/resources/responses/methods/create): parámetros `instructions`, `input`, `tools`, `tool_choice` y `store`.
- [Catálogo oficial de modelos](https://developers.openai.com/api/docs/models): el ejemplo usa `gpt-6-luna`; el nombre del modelo se puede cambiar en `MODELO`.
