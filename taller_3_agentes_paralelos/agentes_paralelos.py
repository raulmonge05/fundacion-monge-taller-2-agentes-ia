"""Demo paso a paso: una tarea, hasta tres agentes especializados."""

import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI


# PASO A: cambia este número y ejecuta el archivo otra vez: 1, luego 2 y luego 3.
MODO = 3

# PERSONALIZA AQUÍ: puedes cambiar la tarea, el modelo y los campos de cada agente.
TAREA = "Escribe una historia breve sobre estudiantes que crean una idea para mejorar su comunidad."
MODELO = "gpt-6-luna"

AGENTES = [
    {
        "nombre": "Poeta",
        "rol": "Eres una persona poeta que transforma ideas en imágenes y metáforas.",
        "estilo": "Usa un tono creativo y musical.",
        "reglas": "Escribe entre 3 y 5 frases. No uses palabras difíciles.",
        "tool_especial": "proponer_metafora",
        "descripcion_tool": "Propone una metáfora breve para la historia.",
    },
    {
        "nombre": "Comediante",
        "rol": "Eres una persona comediante que encuentra el lado divertido de las situaciones.",
        "estilo": "Usa humor amable y una sorpresa graciosa.",
        "reglas": "Escribe entre 3 y 5 frases. No te burles de ninguna persona o grupo.",
        "tool_especial": "proponer_broma_amable",
        "descripcion_tool": "Propone una idea graciosa y amable para la historia.",
    },
    {
        "nombre": "Narrador",
        "rol": "Eres una persona narradora que cuenta historias fáciles de imaginar.",
        "estilo": "Usa un tono aventurero y describe una acción concreta.",
        "reglas": "Escribe entre 3 y 5 frases. Incluye un final claro.",
        "tool_especial": "crear_esquema_de_historia",
        "descripcion_tool": "Propone un esquema corto de inicio, problema y solución.",
    },
]


def crear_definicion_tool(nombre, descripcion):
    """Describe una función de Python que el modelo puede solicitar."""
    return {
        "type": "function",
        "name": nombre,
        "description": descripcion,
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
        "strict": True,
    }


# Tool común: todos los agentes reciben el mismo escenario ficticio.
TOOL_COMUN = crear_definicion_tool(
    "consultar_reto_comun",
    "Devuelve el contexto ficticio del reto comunitario que compartirán los agentes.",
)

# Resultados simples para enseñar que Python ejecuta las tools y devuelve su resultado.
def consultar_reto_comun():
    return (
        "El parque del barrio tiene poca sombra. Un grupo de estudiantes propone "
        "crear un jardín de plantas nativas y asientos hechos con materiales reutilizados."
    )


def proponer_metafora():
    return "El jardín puede ser un corazón verde donde el barrio se reúne."


def proponer_broma_amable():
    return "Un asiento reciclado puede escuchar historias mejor que las palomas del parque."


def crear_esquema_de_historia():
    return (
        "Inicio: estudiantes visitan el parque. Problema: falta sombra. "
        "Solución: crean un jardín y asientos para que las personas se reúnan."
    )


FUNCIONES_PYTHON = {
    "consultar_reto_comun": consultar_reto_comun,
    "proponer_metafora": proponer_metafora,
    "proponer_broma_amable": proponer_broma_amable,
    "crear_esquema_de_historia": crear_esquema_de_historia,
}


def crear_cliente():
    """Carga la API key desde .env y crea el cliente de OpenAI."""
    load_dotenv()

    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit(
            "Falta OPENAI_API_KEY. Copia .env.example como .env y agrega tu API key."
        )

    return OpenAI()


def crear_instrucciones(agente):
    """Une los campos editables y explica cuándo usar las dos tools."""
    return (
        f"Tu nombre es {agente['nombre']}. "
        f"{agente['rol']} "
        f"Estilo: {agente['estilo']} "
        f"Reglas: {agente['reglas']} "
        "Usa los resultados de las dos herramientas que recibirás: la herramienta "
        "común y la herramienta especial de tu agente. Incluye esas ideas en la historia. "
        "Responde siempre en español."
    )


def crear_tool_especial(agente):
    """Crea la descripción de la tool particular de este agente."""
    return crear_definicion_tool(agente["tool_especial"], agente["descripcion_tool"])


def registrar_evento(mensaje, log_callback=None):
    """Escribe el evento en la terminal y, si existe, también en la interfaz."""
    mensaje_con_hora = f"[{datetime.now():%H:%M:%S}] {mensaje}"
    print(mensaje_con_hora, flush=True)
    if log_callback is not None:
        log_callback(mensaje_con_hora)


def pedir_y_ejecutar_tool(cliente, agente, tool, instrucciones, entrada, log_callback=None):
    """Pide una tool específica, la ejecuta en Python y devuelve su resultado al modelo."""
    registrar_evento(
        f"[{agente['nombre']}] Solicitando tool: {tool['name']}", log_callback
    )
    respuesta = cliente.responses.create(
        model=MODELO,
        instructions=instrucciones,
        input=entrada,
        tools=[tool],
        tool_choice={"type": "function", "name": tool["name"]},
        store=False,
    )

    llamada = next(
        (
            item
            for item in respuesta.output
            if item.type == "function_call" and item.name == tool["name"]
        ),
        None,
    )
    if llamada is None:
        raise RuntimeError(
            f"{agente['nombre']} no solicitó la herramienta {tool['name']}."
        )

    entrada.extend(respuesta.output)
    resultado_tool = FUNCIONES_PYTHON[llamada.name]()
    entrada.append(
        {
            "type": "function_call_output",
            "call_id": llamada.call_id,
            "output": resultado_tool,
        }
    )
    registrar_evento(
        f"[{agente['nombre']}] Resultado de {llamada.name}: {resultado_tool}",
        log_callback,
    )
    return llamada.name, resultado_tool


def consultar_agente(agente, tarea, cliente, log_callback=None):
    """Usa la tool común y la especial, y luego pide la respuesta final."""
    instrucciones = crear_instrucciones(agente)
    entrada = [{"role": "user", "content": tarea}]
    tool_especial = crear_tool_especial(agente)

    try:
        # PASO DE TOOLS: Python ejecuta cada función y devuelve su resultado al modelo.
        resultados_tools = [
            pedir_y_ejecutar_tool(
                cliente, agente, TOOL_COMUN, instrucciones, entrada, log_callback
            ),
            pedir_y_ejecutar_tool(
                cliente, agente, tool_especial, instrucciones, entrada, log_callback
            ),
        ]

        registrar_evento(f"[{agente['nombre']}] Generando respuesta final.", log_callback)
        respuesta = cliente.responses.create(
            model=MODELO,
            instructions=instrucciones,
            input=entrada,
            max_output_tokens=180,
            store=False,
        )
        registrar_evento(
            f"[{agente['nombre']}] Respuesta final: {respuesta.output_text}",
            log_callback,
        )
        return agente["nombre"], respuesta.output_text, resultados_tools
    except Exception as error:
        registrar_evento(f"[{agente['nombre']}] Error: {error}", log_callback)
        raise


def ejecutar(modo, tarea=None, log_callback=None):
    """Ejecuta el modo elegido y devuelve las respuestas de los agentes."""
    if modo not in (1, 2, 3):
        raise ValueError("El modo debe ser 1, 2 o 3.")

    tarea_actual = TAREA if tarea is None else tarea
    cliente = crear_cliente()
    agentes_seleccionados = AGENTES[:modo]

    registrar_evento(
        f"[Inicio] Modo {modo}: {len(agentes_seleccionados)} agente(s). "
        f"Tarea: {tarea_actual}",
        log_callback,
    )

    if modo == 1:
        # PASO 1: un agente permite enfocarse en tarea, instrucciones y tools.
        resultados = [
            consultar_agente(
                agentes_seleccionados[0], tarea_actual, cliente, log_callback
            )
        ]
    else:
        # PASOS 2 y 3: las secuencias de los agentes se ejecutan al mismo tiempo.
        with ThreadPoolExecutor(max_workers=modo) as grupo:
            resultados = list(
                grupo.map(
                    lambda agente: consultar_agente(
                        agente, tarea_actual, cliente, log_callback
                    ),
                    agentes_seleccionados,
                )
            )

    registrar_evento("[Fin] Todos los agentes terminaron.", log_callback)
    return resultados


if __name__ == "__main__":
    try:
        ejecutar(MODO)
    except ValueError as error:
        raise SystemExit(str(error)) from error
