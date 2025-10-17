#!/usr/bin/env python3
"""
Script de prueba para verificar que el simulador funciona correctamente.
Verifica:
- Que el archivo de log existe
- Que se pueden parsear los paquetes
- Que la estructura de datos es correcta
"""

import sys
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent))

from simulator.simulator import parse_hex_line, read_log_file


def test_parse_hex_line():
    """Prueba la función de parseo de líneas hexadecimales."""
    print("🧪 Prueba 1: Parseo de líneas hexadecimales")
    print("-" * 60)
    
    # Línea de ejemplo del archivo de log
    test_line = "02 30 30 30 31 30 31 30 30 30 30 30 30 30 35 36 32 34 30 30 30 30 30 30 30 37 30 37 03 36        .000101000000056240000000707.6"
    
    packet = parse_hex_line(test_line)
    
    if packet is None:
        print("❌ Error: No se pudo parsear la línea")
        return False
    
    print(f"✅ Línea parseada correctamente")
    print(f"   Bytes: {packet.hex().upper()}")
    print(f"   Longitud: {len(packet)} bytes")
    
    # Verificar estructura
    if packet[0] != 0x02:
        print("❌ Error: STX incorrecto")
        return False
    
    if packet[-2] != 0x03:
        print("❌ Error: ETX incorrecto")
        return False
    
    print("✅ Estructura correcta (STX y ETX presentes)")
    print()
    return True


def test_read_log_file():
    """Prueba la lectura del archivo de log."""
    print("🧪 Prueba 2: Lectura del archivo de log")
    print("-" * 60)
    
    log_file = Path(__file__).parent.parent / "logs_uwf_protocol" / "conteo hasta 10000_2.txt"
    
    if not log_file.exists():
        print(f"❌ Error: Archivo no encontrado: {log_file}")
        return False
    
    print(f"✅ Archivo encontrado: {log_file}")
    
    packets = read_log_file(log_file)
    
    if packets is None:
        print("❌ Error: No se pudieron leer los paquetes")
        return False
    
    print(f"✅ Se leyeron {len(packets)} paquetes")
    print()
    return True


def test_packet_structure():
    """Prueba la estructura de los paquetes."""
    print("🧪 Prueba 3: Estructura de los paquetes")
    print("-" * 60)
    
    log_file = Path(__file__).parent.parent / "logs_uwf_protocol" / "conteo hasta 10000_2.txt"
    packets = read_log_file(log_file)
    
    if not packets:
        print("❌ Error: No hay paquetes para probar")
        return False
    
    # Verificar el primer paquete
    first_packet = packets[0]
    
    print(f"Primer paquete: {first_packet.hex().upper()}")
    print(f"Longitud: {len(first_packet)} bytes")
    
    # Estructura esperada:
    # Byte 0: STX (0x02)
    # Bytes 1-6: Header
    # Bytes 7-20: Monto (14 dígitos ASCII)
    # Bytes 21-22: Unknown
    # Bytes 23-26: Piezas (4 dígitos ASCII)
    # Byte 27: ETX (0x03)
    # Byte 28: Checksum
    
    if first_packet[0] != 0x02:
        print("❌ Error: STX incorrecto")
        return False
    
    if first_packet[-2] != 0x03:
        print("❌ Error: ETX incorrecto")
        return False
    
    if len(first_packet) != 29:
        print(f"⚠️  Advertencia: Longitud inesperada ({len(first_packet)} bytes, esperado 29)")
    
    # Extraer datos
    try:
        monto_str = first_packet[7:21].decode('ascii')
        piezas_str = first_packet[23:27].decode('ascii')
        
        print(f"✅ Monto: {monto_str}")
        print(f"✅ Piezas: {piezas_str}")
    except Exception as e:
        print(f"❌ Error al decodificar: {e}")
        return False
    
    print()
    return True


def test_all_packets():
    """Prueba todos los paquetes."""
    print("🧪 Prueba 4: Validación de todos los paquetes")
    print("-" * 60)
    
    log_file = Path(__file__).parent.parent / "logs_uwf_protocol" / "conteo hasta 10000_2.txt"
    packets = read_log_file(log_file)
    
    if not packets:
        print("❌ Error: No hay paquetes para probar")
        return False
    
    errors = 0
    
    for i, packet in enumerate(packets, 1):
        if packet[0] != 0x02:
            print(f"❌ Paquete {i}: STX incorrecto")
            errors += 1
        
        if packet[-2] != 0x03:
            print(f"❌ Paquete {i}: ETX incorrecto")
            errors += 1
        
        if len(packet) != 29:
            print(f"⚠️  Paquete {i}: Longitud inesperada ({len(packet)} bytes)")
    
    if errors == 0:
        print(f"✅ Todos los {len(packets)} paquetes son válidos")
    else:
        print(f"❌ Se encontraron {errors} errores")
    
    print()
    return errors == 0


def main():
    """Función principal."""
    print("\n" + "=" * 60)
    print("🧪 PRUEBAS DEL SIMULADOR")
    print("=" * 60 + "\n")
    
    tests = [
        test_parse_hex_line,
        test_read_log_file,
        test_packet_structure,
        test_all_packets,
    ]
    
    results = []
    
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Error en prueba: {e}\n")
            results.append(False)
    
    # Resumen
    print("=" * 60)
    print("📊 RESUMEN")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Pruebas pasadas: {passed}/{total}")
    
    if passed == total:
        print("\n✅ ¡Todas las pruebas pasaron!")
        print("\nPuedes ejecutar el simulador con:")
        print("  python src/simulator.py")
        return True
    else:
        print("\n❌ Algunas pruebas fallaron")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

