#!/usr/bin/env python3
"""
Simulador de datos de conteo para la UWF (Visor Externo)
Lee datos del archivo de log y los envía a través de un puerto serie virtual.
"""

import os
import sys
import time
from pathlib import Path
import serial

# Configuración
LOG_FILE_1 = Path(__file__).parent.parent / "data" / "conteo_real_solo_piezas.txt"
LOG_FILE_2 = Path(__file__).parent.parent / "data" / "conteo_real_desbordamiento.txt"

SERIAL_PORT = (
    "/dev/ttyS0"  
)
BAUDRATE = 19200
DELAY_BETWEEN_PACKETS = 0.1  # Segundos entre paquetes

# Detectar sistema operativo
IS_LINUX = sys.platform.startswith("linux")
IS_MACOS = sys.platform == "darwin"
IS_WINDOWS = sys.platform == "win32"


def parse_hex_line(line):
    """
    Extrae los bytes hexadecimales de una línea del archivo de log.
    Formato esperado: "02 30 30 ... 03 XX"
    """
    # Tomar solo la parte hexadecimal (antes del punto)
    hex_part = line.split(".")[0].strip()

    # Dividir por espacios y convertir a bytes
    hex_values = hex_part.split()

    try:
        packet = bytes([int(h, 16) for h in hex_values])

        # Validar que el paquete tenga la estructura correcta
        # STX (02) ... ETX (03) ... CHECKSUM
        if len(packet) >= 3 and packet[0] == 0x02 and packet[-2] == 0x03:
            return packet
        else:
            return None
    except ValueError:
        return None


def read_log_file(filepath):
    """
    Lee el archivo de log y extrae todos los paquetes.
    """
    packets = []

    try:
        with open(filepath, "r") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue

                packet = parse_hex_line(line)
                if packet:
                    packets.append(packet)
                else:
                    print(f"⚠️  Línea {line_num}: No se pudo parsear")

    except FileNotFoundError:
        print(f"❌ Archivo no encontrado: {filepath}")
        return None

    return packets


def send_packets(
    packets, port=SERIAL_PORT, baudrate=BAUDRATE, delay=DELAY_BETWEEN_PACKETS
):
    """
    Envía los paquetes a través del puerto serie.
    """
    try:
        ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1,
        )
        print(f"✅ Puerto {port} abierto correctamente")
        print(f"📊 Enviando {len(packets)} paquetes...\n")

        for i, packet in enumerate(packets, 1):
            try:
                ser.write(packet)
                print(f"[{i:3d}/{len(packets)}] Enviado: {packet.hex().upper()}")
                time.sleep(delay)
            except Exception as e:
                print(f" Error al enviar paquete {i}: {e}")

        print(f"\n✅ Simulación completada. {len(packets)} paquetes enviados.")
        ser.close()

    except serial.SerialException as e:
        print(f" Error al abrir puerto serie: {e}")
        print("\n💡 Soluciones:")
        print("   - En Windows: Asegúrate de que COM3 existe")
        print(
            "   - En Linux: Usa 'socat -d -d pty,raw,echo=0 pty,raw,echo=0' para crear puertos virtuales"
        )
        print("   - O modifica SERIAL_PORT en este script")
        return False

    return True


def get_serial_port():
    """
    Detecta el puerto serie a usar según el SO.
    """
    port = SERIAL_PORT

    if IS_LINUX or IS_MACOS:
        # En Linux/macOS, intentar usar puertos virtuales primero
        if os.path.exists("/tmp/COM3"):
            port = "/tmp/COM3"
        elif os.path.exists("/dev/ttyS0"):
            port = "/dev/ttyS0"

    return port


def main():
    """
    Función principal.
    """
    print("=" * 60)
    print("🔄 SIMULADOR DE CONTEO - UWF (Visor Externo)")
    print("=" * 60)
    print(f"📁 Archivo de log: {LOG_FILE_2}")

    # Detectar puerto
    port = get_serial_port()
    print(f"🔌 Puerto serie: {port}")
    print(f"⚙️  Baudrate: {BAUDRATE}")
    print(f"⏱️  Delay entre paquetes: {DELAY_BETWEEN_PACKETS}s")
    print("=" * 60 + "\n")

    # Leer archivo de log
    packets = read_log_file(LOG_FILE_2)

    if not packets:
        print("No se pudieron cargar los paquetes")
        return False

    print(f"✅ Se cargaron {len(packets)} paquetes\n")

    # Enviar paquetes
    # input("Presiona ENTER para comenzar la simulación...")
    return send_packets(packets, port=port)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
