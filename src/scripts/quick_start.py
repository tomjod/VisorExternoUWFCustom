#!/usr/bin/env python3
"""
Script de inicio rápido para la simulación.
Proporciona un menú interactivo para elegir cómo ejecutar la simulación.
"""

import subprocess
import sys
import os
from pathlib import Path

# Configuración
SRC_DIR = Path(__file__).parent
MAIN_SCRIPT = SRC_DIR / "main.py"
SIMULATOR_SCRIPT = SRC_DIR / "simulator.py"
RUN_SIMULATION_SCRIPT = SRC_DIR / "run_simulation.py"

# Detectar SO
IS_LINUX = sys.platform.startswith("linux")
IS_MACOS = sys.platform == "darwin"
IS_WINDOWS = sys.platform == "win32"


def print_header():
    """Imprime el encabezado."""
    print("\n" + "=" * 60)
    print("🎯 VISOR CONTADORA GLORY - SIMULADOR")
    print("=" * 60 + "\n")


def print_menu():
    """Imprime el menú de opciones."""
    print("Selecciona una opción:\n")
    print("1. 🚀 Ejecutar solo la aplicación principal")
    print("2. 🔄 Ejecutar solo el simulador")
    print("3. 🎯 Ejecutar ambos (requiere puertos virtuales)")
    print("4. 📖 Ver instrucciones")
    print("5. ❌ Salir\n")


def run_main_app():
    """Ejecuta la aplicación principal."""
    print("\n🚀 Iniciando aplicación principal...\n")
    try:
        subprocess.run([sys.executable, str(MAIN_SCRIPT)], cwd=str(SRC_DIR))
    except KeyboardInterrupt:
        print("\n\n⏹️  Aplicación detenida por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")


def run_simulator():
    """Ejecuta el simulador."""
    print("\n🔄 Iniciando simulador...\n")
    try:
        subprocess.run([sys.executable, str(SIMULATOR_SCRIPT)], cwd=str(SRC_DIR))
    except KeyboardInterrupt:
        print("\n\n⏹️  Simulador detenido por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")


def run_both():
    """Ejecuta ambos programas."""
    if IS_WINDOWS:
        print("\n⚠️  En Windows, debes ejecutar ambos en terminales separadas:")
        print("   Terminal 1: python src/main.py")
        print("   Terminal 2: python src/simulator.py")
        print("\n💡 Asegúrate de que COM3 está disponible\n")
        return
    
    print("\n🎯 Ejecutando simulación completa...\n")
    try:
        subprocess.run([sys.executable, str(RUN_SIMULATION_SCRIPT)], cwd=str(SRC_DIR))
    except KeyboardInterrupt:
        print("\n\n⏹️  Simulación detenida por el usuario")
    except FileNotFoundError:
        print("\n❌ Script de simulación no encontrado")
        print("   Ejecuta ambos programas en terminales separadas:")
        print("   Terminal 1: python src/main.py")
        print("   Terminal 2: python src/simulator.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")


def show_instructions():
    """Muestra las instrucciones."""
    print("\n" + "=" * 60)
    print("📖 INSTRUCCIONES")
    print("=" * 60 + "\n")
    
    if IS_WINDOWS:
        print("WINDOWS:")
        print("-" * 60)
        print("1. Asegúrate de que COM3 está disponible")
        print("2. Abre dos terminales")
        print("3. En la terminal 1, ejecuta: python src/main.py")
        print("4. En la terminal 2, ejecuta: python src/simulator.py")
        print("5. El simulador enviará los datos a la aplicación\n")
    
    elif IS_LINUX or IS_MACOS:
        print("LINUX/macOS:")
        print("-" * 60)
        print("Opción 1: Puertos virtuales automáticos")
        print("  1. Instala socat: sudo apt-get install socat (Linux)")
        print("  2. Ejecuta: python src/quick_start.py")
        print("  3. Selecciona opción 3\n")
        
        print("Opción 2: Ejecución manual")
        print("  Terminal 1: socat -d -d pty,raw,echo=0,link=/tmp/COM3 pty,raw,echo=0,link=/tmp/COM4")
        print("  Terminal 2: python src/main.py")
        print("  Terminal 3: python src/simulator.py\n")
    
    print("=" * 60 + "\n")


def main():
    """Función principal."""
    print_header()
    
    while True:
        print_menu()
        choice = input("Opción: ").strip()
        
        if choice == "1":
            run_main_app()
        elif choice == "2":
            run_simulator()
        elif choice == "3":
            run_both()
        elif choice == "4":
            show_instructions()
        elif choice == "5":
            print("\n👋 ¡Hasta luego!\n")
            break
        else:
            print("\n❌ Opción no válida\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego!\n")
        sys.exit(0)

