"""
Configuración centralizada para la aplicación y simulador.
"""

import sys
from pathlib import Path

# Directorios
PROJECT_ROOT = Path(__file__).parent.parent
SRC_DIR = Path(__file__).parent
LOGS_DIR = PROJECT_ROOT / "logs_uwf_protocol"

# Archivos de log - Originales
LOG_FILE_ORIGINAL_1 = LOGS_DIR / "contadora en 0 enviando datos.txt"
LOG_FILE_ORIGINAL_2 = LOGS_DIR / "conteo hasta 10000.txt"
LOG_FILE_ORIGINAL_3 = LOGS_DIR / "conteo hasta 10000_2.txt"

# Archivos de log - Generados (con desbordamiento y conteos altos)
LOG_FILE_1 = LOGS_DIR / "conteo_desbordamiento_simple.txt"  # 9995 → 10005 piezas
LOG_FILE_2 = LOGS_DIR / "conteo_desbordamiento_multiple.txt"  # 0 → 30,000 piezas
LOG_FILE_3 = LOGS_DIR / "conteo_20mil_piezas.txt"  # 0 → 20,000 piezas
LOG_FILE_4 = LOGS_DIR / "conteo_50mil_piezas.txt"  # 0 → 50,000 piezas
LOG_FILE_5 = LOGS_DIR / "conteo_desbordamiento_rapido.txt"  # Conteo acelerado
LOG_FILE_6 = LOGS_DIR / "conteo_realista.txt"  # 0 → 25,000 piezas realista

# Alias para compatibilidad
LOG_FILE_ORIGINAL = LOG_FILE_ORIGINAL_3

# Configuración del puerto serie
SERIAL_CONFIG = {
    "baudrate": 19200,
    "bytesize": 8,
    "parity": "N",
    "stopbits": 1,
    "timeout": 1,
}

# Configuración del simulador
SIMULATOR_CONFIG = {
    "delay_between_packets": 0.1,  # segundos
    "log_file": LOG_FILE_3,  # Archivo de log a usar
}

# Configuración de la GUI
GUI_CONFIG = {
    "title": "Visor Contadora Glory",
    "width": 450,
    "height": 250,
    "bg_color": "#2E3B4E",
    "text_color": "white",
    "monto_color": "#4CAF50",
    "piezas_color": "#FFC107",
}

# Protocolo
PROTOCOL_CONFIG = {
    "STX": b"\x02",
    "ETX": b"\x03",
    "PAYLOAD_LENGTH": 27,
}

# Detectar sistema operativo
IS_LINUX = sys.platform.startswith("linux")
IS_MACOS = sys.platform == "darwin"
IS_WINDOWS = sys.platform == "win32"


def get_serial_port():
    """
    Detecta el puerto serie a usar según el SO.
    """
    if IS_WINDOWS:
        return "COM3"
    elif IS_LINUX or IS_MACOS:
        # Intentar puertos virtuales primero
        import os

        if os.path.exists("/tmp/COM3"):
            return "/tmp/COM3"
        elif os.path.exists("/tmp/COM4"):
            return "/tmp/COM4"
        elif os.path.exists("/dev/ttyS0"):
            return "/dev/ttyS0"
        else:
            return "/dev/ttyUSB0"  # Fallback para puertos USB

    return "COM3"  # Default


def get_simulator_port():
    """
    Detecta el puerto serie para el simulador.
    """
    if IS_WINDOWS:
        return "COM3"
    elif IS_LINUX or IS_MACOS:
        import os

        if os.path.exists("/tmp/COM3"):
            return "/tmp/COM3"
        else:
            return "/tmp/COM3"  # Será creado por socat

    return "COM3"


# Configuración final
MAIN_SERIAL_PORT = get_serial_port()
SIMULATOR_SERIAL_PORT = get_simulator_port()

# Actualizar configuración del simulador
SIMULATOR_CONFIG["serial_port"] = SIMULATOR_SERIAL_PORT

print(
    f"[CONFIG] Sistema: {'Windows' if IS_WINDOWS else 'Linux' if IS_LINUX else 'macOS'}"
)
print(f"[CONFIG] Puerto principal: {MAIN_SERIAL_PORT}")
print(f"[CONFIG] Puerto simulador: {SIMULATOR_SERIAL_PORT}")
