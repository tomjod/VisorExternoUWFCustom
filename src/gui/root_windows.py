import tkinter as tk
from tkinter import messagebox


class RootWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Visor Contadora Glory")
        self.geometry("500x250")
        self.configure(bg="#2E3B4E")
        self.gui_vars = {
            "monto": tk.StringVar(value="Esperando datos..."),
            "piezas": tk.StringVar(value="0"),
            "status": tk.StringVar(value=""),
            "rechazo_sensor": tk.StringVar(value="Desconectado"),
        }

        # Crear y estilizar las etiquetas y los valores
        tk.Label(
            self,
            text="Piezas Contadas (Acumulado)",
            font=("Helvetica", 18),
            fg="white",
            bg="#2E3B4E",
        ).pack(pady=(20, 0))
        tk.Label(
            self,
            textvariable=self.gui_vars["piezas"],
            font=("Consolas", 32, "bold"),
            fg="#FFC107",
            bg="#2E3B4E",
        ).pack()
        tk.Label(
            self,
            text="Monto Total Contado",
            font=("Helvetica", 18),
            fg="white",
            bg="#2E3B4E",
        ).pack(pady=(20, 0))
        tk.Label(
            self,
            textvariable=self.gui_vars["monto"],
            font=("Consolas", 32, "bold"),
            fg="#4CAF50",
            bg="#2E3B4E",
        ).pack()

        # Frame para los labels de status y rechazo en la esquina inferior izquierda
        bottom_frame = tk.Frame(self, bg="#2E3B4E")
        bottom_frame.pack(side="bottom", anchor="sw", padx=(10, 0), pady=(0, 10))

        tk.Label(
            bottom_frame,
            textvariable=self.gui_vars["status"],
            font=("Consolas", 12, "bold"),
            fg="#4CAF50",
            bg="#2E3B4E",
        ).pack(side="left", padx=(0, 10))

        tk.Label(
            bottom_frame,
            textvariable=self.gui_vars["rechazo_sensor"],
            font=("Consolas", 12, "bold"),
            fg="#B8120C",
            bg="#2E3B4E",
        ).pack(side="left", padx=(0, 0))

    def show_serial_error(self, message):
        """
        Función que muestra la ventana de error en el hilo principal de Tkinter.
        """

        messagebox.showerror(
            title="Error de Conexión",
            message=f"No se pudo abrir el puerto serie.\n\n{message}\n\nAsegúrate de que el dispositivo esté conectado y el puerto no esté en uso.",
        )
        self.quit()

    def update_labels(self, data):
        # Actualizar las variables de la GUI
        self.gui_vars["monto"].set(f"{data['monto']:,}".replace(",", "."))
        self.gui_vars["piezas"].set(f"{data['piezas']:,}".replace(",", "."))
        self.gui_vars["status"].set(f"{'🟢' if data['status'] else ''}")
        self.gui_vars["rechazo_sensor"].set(f"{'🔴​' if data['rechazo_sensor'] else ''}")
