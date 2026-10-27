"""Interfaz opcional para ejecutar agentes y ver sus logs."""

import queue
import threading

try:
    import tkinter as tk
    from tkinter import ttk
except ImportError as error:
    raise SystemExit(
        "Tkinter no está disponible en esta instalación de Python. "
        "Puedes usar agentes_paralelos.py desde la terminal."
    ) from error

from agentes_paralelos import MODO, TAREA, ejecutar


class VentanaAgentes:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Taller 3 · Agentes con tools")
        self.ventana.geometry("900x680")
        self.ventana.columnconfigure(0, weight=1)
        self.ventana.rowconfigure(3, weight=1)

        self.cola_logs = queue.Queue()
        self.modo = tk.IntVar(value=MODO)
        self.estado = tk.StringVar(value="Listo")

        ttk.Label(
            ventana,
            text="Elige cuántos agentes ejecutas",
            font=("TkDefaultFont", 14, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(16, 4))

        modos = ttk.Frame(ventana)
        modos.grid(row=1, column=0, sticky="w", padx=12, pady=4)
        for valor, etiqueta in (
            (1, "1 · Poeta"),
            (2, "2 · Poeta y comediante"),
            (3, "3 · Los tres"),
        ):
            ttk.Radiobutton(
                modos, text=etiqueta, value=valor, variable=self.modo
            ).pack(side="left", padx=6)

        ttk.Label(ventana, text="Tarea común:").grid(
            row=2, column=0, sticky="w", padx=16, pady=(8, 2)
        )
        self.campo_tarea = tk.Text(ventana, height=3, wrap="word")
        self.campo_tarea.grid(row=3, column=0, sticky="ew", padx=16, pady=(0, 8))
        self.campo_tarea.insert("1.0", TAREA)

        controles = ttk.Frame(ventana)
        controles.grid(row=4, column=0, sticky="ew", padx=16, pady=4)
        self.boton_ejecutar = ttk.Button(
            controles, text="Ejecutar", command=self.iniciar_ejecucion
        )
        self.boton_ejecutar.pack(side="left")
        ttk.Label(controles, textvariable=self.estado).pack(side="left", padx=12)

        ttk.Label(ventana, text="Actividad: llamadas, tools y respuestas").grid(
            row=5, column=0, sticky="w", padx=16, pady=(8, 2)
        )
        panel_logs = ttk.Frame(ventana)
        panel_logs.grid(row=6, column=0, sticky="nsew", padx=16, pady=(0, 16))
        panel_logs.columnconfigure(0, weight=1)
        panel_logs.rowconfigure(0, weight=1)
        ventana.rowconfigure(6, weight=1)

        self.registro = tk.Text(panel_logs, wrap="word", state="disabled")
        self.registro.grid(row=0, column=0, sticky="nsew")
        barra = ttk.Scrollbar(panel_logs, command=self.registro.yview)
        barra.grid(row=0, column=1, sticky="ns")
        self.registro.configure(yscrollcommand=barra.set)

        self.ventana.after(100, self.leer_cola)

    def iniciar_ejecucion(self):
        tarea = self.campo_tarea.get("1.0", "end").strip()
        if not tarea:
            self.estado.set("Escribe una tarea antes de ejecutar.")
            return

        self.boton_ejecutar.configure(state="disabled")
        self.estado.set("Ejecutando…")
        self.registro.configure(state="normal")
        self.registro.delete("1.0", "end")
        self.registro.configure(state="disabled")

        hilo = threading.Thread(
            target=self.ejecutar_en_fondo,
            args=(self.modo.get(), tarea),
            daemon=True,
        )
        hilo.start()

    def ejecutar_en_fondo(self, modo, tarea):
        try:
            ejecutar(modo, tarea, log_callback=self.cola_logs.put)
        except SystemExit as error:
            self.cola_logs.put(f"[Error] {error}")
        except Exception as error:
            self.cola_logs.put(f"[Error] {error}")
        finally:
            self.cola_logs.put(None)

    def leer_cola(self):
        while True:
            try:
                mensaje = self.cola_logs.get_nowait()
            except queue.Empty:
                break

            if mensaje is None:
                self.boton_ejecutar.configure(state="normal")
                self.estado.set("Listo")
                continue

            self.registro.configure(state="normal")
            self.registro.insert("end", mensaje + "\n\n")
            self.registro.see("end")
            self.registro.configure(state="disabled")

        self.ventana.after(100, self.leer_cola)


if __name__ == "__main__":
    ventana = tk.Tk()
    VentanaAgentes(ventana)
    ventana.mainloop()
