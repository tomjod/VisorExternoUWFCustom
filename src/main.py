import threading
import time
from tkinter import messagebox

import serial

from gui.root_windows import RootWindow

# --- Constantes del Protocolo ---
STX = b"\x02"  # Start of Text
ETX = b"\x03"  # End of Text
PAYLOAD_LENGTH = 27  # Longitud esperada del payload en caracteres


# --- Clase para manejar el contador acumulativo ---
# Esta clase resuelve el problema del reinicio del contador de piezas
class CumulativeCounter:
    """
    Gestiona un contador que se reinicia (ej. 9999 -> 0) para
    mantener un total acumulado. Detecta reinicio basándose en:
    1. Salto hacia atrás significativo en piezas (desbordamiento)
    2. Reinicio manual (piezas vuelven a 0 o muy bajo)
    """

    def __init__(self):
        self.total_pieces = 0
        self.offset = 0
        self.last_reading = {"piezas": 0, "monto": 0}
        self.max_counter_value = 10000  # Valor máximo
        self.overflow_threshold = (
            self.max_counter_value * 0.5
        )  # 5000 para detectar desbordamiento

    def update(self, new_reading: dict[str, int]):
        """
        Actualiza el contador total detectando desbordamiento vs reinicio manual.

        DESBORDAMIENTO: Piezas bajan mucho (>5000) pero monto sigue igual/sube
                        Ej: 9980 piezas → 25 piezas, monto sigue igual

        REINICIO MANUAL: Piezas bajan mucho Y monto también baja/es 0
                         Ej: 5000 piezas → 0 piezas, monto 0 → 0
        """
        piezas_actual = new_reading["piezas"]
        piezas_anterior = self.last_reading["piezas"]
        monto_actual = new_reading["monto"]
        monto_anterior = self.last_reading["monto"]

        diferencia_piezas = piezas_anterior - piezas_actual
        diferencia_monto = monto_anterior - monto_actual

        # Caso 1: Salto hacia atrás significativo en piezas
        if (
            piezas_actual < piezas_anterior
            and diferencia_piezas > self.overflow_threshold
        ):
            # Distinguir entre DESBORDAMIENTO y REINICIO MANUAL
            # Si el monto también bajó significativamente → REINICIO MANUAL
            if monto_actual < monto_anterior and diferencia_monto > 0:
                self.offset = 0
                print(
                    f"🔄 REINICIO MANUAL detectado! "
                    f"Piezas: {piezas_anterior} → {piezas_actual}, "
                    f"Monto: {monto_anterior} → {monto_actual}. "
                    f"Offset reseteado a 0"
                )
            elif piezas_actual == 0 and monto_actual == 0:
                self.offset = 0
                print(
                    f"🔄 REINICIO MANUAL detectado! "
                    f"Piezas: {piezas_anterior} → {piezas_actual}, "
                    f"Monto: {monto_anterior} → {monto_actual}. "
                    f"Offset reseteado a 0"
                )
            # Si el monto se mantiene igual o sube → DESBORDAMIENTO
            else:
                self.offset += self.max_counter_value
                print(
                    f"⚠️  DESBORDAMIENTO detectado! "
                    f"Piezas: {piezas_anterior} → {piezas_actual}, "
                    f"Monto: {monto_anterior} → {monto_actual}. "
                    f"Nuevo offset: {self.offset}"
                )

        # Caso 2: Reinicio suave (piezas a 0 sin gran salto)
        # Esto ocurre cuando se resetea desde un valor bajo
        elif piezas_actual < 100 and piezas_anterior > 100:
            self.offset = 0
            print(
                f"🔄 Reinicio suave detectado! "
                f"Piezas: {piezas_anterior} → {piezas_actual}. "
                f"Offset reseteado a 0"
            )

        # Caso 3: Solo cambio en monto (informativo)
        elif (
            monto_actual < monto_anterior
            and monto_anterior > 0
            and piezas_actual >= piezas_anterior
        ):
            print(
                f"ℹ️  Cambio en monto detectado: {monto_anterior} → {monto_actual} "
                f"(piezas sin cambio: {piezas_actual})"
            )

        self.total_pieces = self.offset + piezas_actual
        self.last_reading["piezas"] = piezas_actual
        self.last_reading["monto"] = monto_actual
        return self.total_pieces


# --- Funciones para la GUI ---
def show_serial_error(self, error_message):
    """
    Función que muestra la ventana de error en el hilo principal de Tkinter.
    """
    messagebox.showerror(
        title="Error de Conexión",
        message=f"No se pudo abrir el puerto serie.\n\n{error_message}\n\nAsegúrate de que el dispositivo esté conectado y el puerto no esté en uso.",
    )
    self.quit()


def parse_payload(payload: bytearray):
    """
    Extrae los datos relevantes del payload.
    """

    payload_str = payload.decode("ascii")
    print(payload_str)

    return {
        "monto": int(payload_str[7:20]),
        "piezas": int(payload_str[23:27]),
        "status": True if payload_str[2] != "0" else False,
        "rechazo_sensor": True if payload_str[5] == "1" else False,
    }


def update_gui(gui_vars, data):
    """
    Actualiza las variables de la GUI con los datos recibidos.
    """
    gui_vars["monto"].set(f"{data['monto']:,}".replace(",", "."))
    gui_vars["piezas"].set(f"{data['piezas']:,}".replace(",", "."))
    # gui_vars["status"].set(f"{'Activo' if data['status'] else 'Inactivo'}")
    # gui_vars["rechazo_sensor"].set(f"{'Activo' if data['rechazo_sensor'] else 'Inactivo'}")


# --- Función Principal para Leer el Puerto Serie ---
def serial_reader(gui: RootWindow, counter):
    """
    Se ejecuta en un hilo separado para leer y procesar datos del puerto serie
    sin bloquear la interfaz gráfica.
    """
    try:
        # Configuración y apertura del puerto serie
        ser = serial.Serial(
            port="/tmp/COM4",
            baudrate=19200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1,  # Tiempo de espera para la lectura
        )
        print("Puerto COM3 abierto con éxito.")
    except serial.SerialException as e:
        print(f"Error al abrir el puerto serie: {e}")
        gui.after(100, gui.show_serial_error, str(e))
        return

    # Máquina de estados para la lectura de datos
    state = "WAITING_FOR_STX"
    payload_buffer = bytearray()

    while True:
        try:
            byte = ser.read(1)
            if not byte:
                continue  # Si no hay datos, vuelve a intentar

            # Lógica de la máquina de estados
            if state == "WAITING_FOR_STX":
                if byte == STX:
                    payload_buffer.clear()
                    state = "READING_PAYLOAD"

            elif state == "READING_PAYLOAD":
                if byte == ETX:
                    # Paquete recibido, ahora se procesa
                    if len(payload_buffer) == PAYLOAD_LENGTH:
                        # Extraer checksum (los últimos 2 bytes del buffer original no son parte del payload)
                        # No es necesario leerlo aparte ya que lo descartamos.

                        data = parse_payload(payload_buffer)

                        # Actualizar el contador acumulativo
                        piezas_acumuladas = counter.update(data)

                        data["piezas"] = piezas_acumuladas

                        # Actualizar las variables de la GUI
                        gui.update_labels(data)

                    # Volver al estado inicial para el próximo paquete
                    state = "WAITING_FOR_STX"
                else:
                    payload_buffer.append(ord(byte))

        except serial.SerialException:
            print("Error de lectura o puerto desconectado.")
            gui.gui_vars["monto"].set("Error de Conexión")
            gui.gui_vars["piezas"].set("Reconectar")
            ser.close()
            time.sleep(2)  # Esperar antes de intentar reabrir
            try:
                ser.open()
                print("Puerto reabierto.")
            except serial.SerialException:
                print("Fallo al reabrir el puerto.")
                time.sleep(2)
        except Exception as e:
            print(f"Error inesperado: {e}")
            state = "WAITING_FOR_STX"


# --- Inicio del Programa ---
if __name__ == "__main__":
    # Crear una instancia del contador acumulativo
    piece_counter = CumulativeCounter()
    root_window = RootWindow()

    # Crear e iniciar el hilo para la lectura serie
    # El 'daemon=True' asegura que el hilo se cierre cuando la ventana principal se cierre
    serial_thread = threading.Thread(
        target=serial_reader, args=(root_window, piece_counter), daemon=True
    )
    serial_thread.start()

    # Iniciar el bucle principal de la GUI
    root_window.mainloop()
