#!/usr/bin/env python3
"""
Script para ejecutar la simulación completa en Linux/macOS.
Crea puertos virtuales automáticamente y ejecuta el simulador.
"""

import os
import signal
import subprocess
import sys
import time
from pathlib import Path

# Configuración
SCRIPT_DIR = Path(__file__).parent.parent
SIMULATOR_SCRIPT = SCRIPT_DIR / "simulator/simulator.py"
MAIN_SCRIPT = SCRIPT_DIR / "main.py"

# Puertos virtuales
VIRTUAL_PORT_1 = "/tmp/COM3"
VIRTUAL_PORT_2 = "/tmp/COM4"

# Procesos
socat_process = None
main_process = None
simulator_process = None


def cleanup(signum=None, frame=None):
    """Limpia los procesos al salir."""
    global socat_process, main_process, simulator_process

    print("\n\n🛑 Deteniendo procesos...")

    if simulator_process:
        try:
            simulator_process.terminate()
            simulator_process.wait(timeout=2)
        except:
            simulator_process.kill()

    if main_process:
        try:
            main_process.terminate()
            main_process.wait(timeout=2)
        except:
            main_process.kill()

    if socat_process:
        try:
            socat_process.terminate()
            socat_process.wait(timeout=2)
        except:
            socat_process.kill()

    print("✅ Procesos detenidos")
    sys.exit(0)


def check_socat():
    """Verifica si socat está instalado."""
    try:
        subprocess.run(["which", "socat"], capture_output=True, check=True)
        return True
    except:
        return False


def create_virtual_ports():
    """Crea puertos virtuales usando socat."""
    global socat_process

    print("🔧 Creando puertos virtuales...")

    try:
        socat_process = subprocess.Popen(
            [
                "socat",
                "-d",
                "-d",
                f"pty,raw,echo=0,link={VIRTUAL_PORT_1}",
                f"pty,raw,echo=0,link={VIRTUAL_PORT_2}",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Esperar a que se creen los puertos
        time.sleep(1)

        if os.path.exists(VIRTUAL_PORT_1) and os.path.exists(VIRTUAL_PORT_2):
            print("✅ Puertos virtuales creados:")
            print(f"   - {VIRTUAL_PORT_1}")
            print(f"   - {VIRTUAL_PORT_2}")
            return True
        else:
            print("❌ No se pudieron crear los puertos virtuales")
            return False

    except FileNotFoundError:
        print("❌ socat no está instalado")
        return False
    except Exception as e:
        print(f"❌ Error al crear puertos virtuales: {e}")
        return False


def run_main_app():
    """Ejecuta la aplicación principal."""
    global main_process

    print("\n🚀 Iniciando aplicación principal...")

    try:
        main_process = subprocess.Popen(
            [sys.executable, str(MAIN_SCRIPT)], cwd=str(SCRIPT_DIR)
        )
        print("✅ Aplicación principal iniciada")
        return True
    except Exception as e:
        print(f"❌ Error al iniciar aplicación principal: {e}")
        return False


def run_simulator():
    """Ejecuta el simulador."""
    global simulator_process

    print("\n🔄 Iniciando simulador...")

    try:
        simulator_process = subprocess.Popen(
            [sys.executable, str(SIMULATOR_SCRIPT)], cwd=str(SCRIPT_DIR)
        )
        print("✅ Simulador iniciado")
        return True
    except Exception as e:
        print(f"❌ Error al iniciar simulador: {e}")
        return False


def main():
    """Función principal."""
    print("=" * 60)
    print("🎯 EJECUTOR DE SIMULACIÓN - UWF (Visor Externo)")
    print("=" * 60)
    print()

    # Registrar manejador de señales
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    # Verificar socat
    if not check_socat():
        print("❌ socat no está instalado")
        print("\nPara instalar:")
        print("  Ubuntu/Debian: sudo apt-get install socat")
        print("  Fedora/RHEL:   sudo dnf install socat")
        print("  macOS:         brew install socat")
        return False

    print("✅ socat está disponible\n")

    # Crear puertos virtuales
    if not create_virtual_ports():
        return False

    # Ejecutar aplicación principal
    if not run_main_app():
        cleanup()
        return False

    # Esperar un poco para que la aplicación se inicie
    time.sleep(2)

    # Ejecutar simulador
    if not run_simulator():
        cleanup()
        return False

    print("\n" + "=" * 60)
    print("✅ Simulación en ejecución")
    print("=" * 60)
    print("\nPresiona Ctrl+C para detener...\n")

    # Esperar a que terminen los procesos
    try:
        if simulator_process:
            simulator_process.wait()
        if main_process:
            main_process.wait()
    except KeyboardInterrupt:
        cleanup()

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
