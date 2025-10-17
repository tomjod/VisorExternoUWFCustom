#!/bin/bash
# Script para configurar puertos serie virtuales en Linux usando socat
# Uso: ./setup_virtual_ports.sh

echo "=========================================="
echo "🔧 Configurador de Puertos Virtuales"
echo "=========================================="

# Verificar si socat está instalado
if ! command -v socat &> /dev/null; then
    echo "❌ socat no está instalado"
    echo ""
    echo "Para instalar en Debian/Ubuntu:"
    echo "  sudo apt-get install socat"
    echo ""
    echo "Para instalar en Fedora/RHEL:"
    echo "  sudo dnf install socat"
    echo ""
    echo "Para instalar en macOS:"
    echo "  brew install socat"
    exit 1
fi

echo "✅ socat está instalado"
echo ""
echo "Creando puertos virtuales COM3 y COM4..."
echo ""

# Crear dos puertos virtuales conectados entre sí
# COM3 será usado por el simulador (escritura)
# COM4 será usado por la aplicación principal (lectura)
socat -d -d pty,raw,echo=0,link=/tmp/COM3 pty,raw,echo=0,link=/tmp/COM4 &

SOCAT_PID=$!
echo ""
echo "✅ Puertos virtuales creados:"
echo "   - /tmp/COM3 (Simulador - escritura)"
echo "   - /tmp/COM4 (Aplicación - lectura)"
echo ""
echo "PID del proceso socat: $SOCAT_PID"
echo ""
echo "Para detener los puertos virtuales, ejecuta:"
echo "  kill $SOCAT_PID"
echo ""
echo "Presiona Ctrl+C para terminar..."

wait $SOCAT_PID

