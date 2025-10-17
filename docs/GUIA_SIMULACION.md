# 📖 Guía de Simulación - Visor Contadora Glory

## ¿Qué es la Simulación?

La simulación permite probar la aplicación del Visor Contadora Glory usando datos reales capturados de una máquina contadora UWF. El simulador lee estos datos y los envía a través de un puerto serie virtual, permitiendo probar la aplicación sin necesidad de una máquina real.

## 🚀 Inicio Rápido (3 pasos)

### Paso 1: Abre una terminal y ejecuta el menú interactivo
```bash
python src/quick_start.py
```

### Paso 2: Selecciona una opción
- **Opción 1:** Solo la aplicación (necesitas enviar datos manualmente)
- **Opción 2:** Solo el simulador (necesitas ejecutar la app en otra terminal)
- **Opción 3:** Ambos automáticamente (Linux/macOS con socat)

### Paso 3: Observa los datos en tiempo real
La aplicación mostrará:
- **Monto Total Contado:** Aumentando en verde
- **Piezas Contadas (Acumulado):** Aumentando en amarillo

## 💻 Instalación de Dependencias

### Todos los Sistemas
```bash
pip install -r src/requirements.txt
```

### Linux/macOS (para simulación automática)
```bash
# Ubuntu/Debian
sudo apt-get install socat

# Fedora/RHEL
sudo dnf install socat

# macOS
brew install socat
```

## 🎯 Métodos de Ejecución

### Método 1: Menú Interactivo (Recomendado)
```bash
python src/quick_start.py
```
Interfaz amigable con opciones claras.

### Método 2: Ejecución Manual (Windows)
**Terminal 1:**
```bash
python src/main.py
```

**Terminal 2:**
```bash
python src/simulator.py
```

### Método 3: Ejecución Automática (Linux/macOS)
```bash
python src/run_simulation.py
```
Crea puertos virtuales automáticamente.

### Método 4: Ejecución Manual (Linux/macOS)
**Terminal 1:**
```bash
socat -d -d pty,raw,echo=0,link=/tmp/COM3 pty,raw,echo=0,link=/tmp/COM4
```

**Terminal 2:**
```bash
python src/main.py
```

**Terminal 3:**
```bash
python src/simulator.py
```

## 🧪 Verificación

Para verificar que todo funciona correctamente:

```bash
python src/test_simulator.py
```

Deberías ver:
```
✅ Línea parseada correctamente
✅ Archivo encontrado
✅ Se leyeron 384 paquetes
✅ Monto: 00000005624000
✅ Piezas: 0070
```

## 📊 Datos de Prueba

**Archivo:** `logs_uwf_protocol/conteo hasta 10000_2.txt`
- **Paquetes:** 384 válidos
- **Rango de conteo:** 0 a 10,000 piezas
- **Rango de monto:** 0 a 390,440 unidades

## 🔧 Configuración

Edita `src/config.py` para cambiar:

```python
# Puerto serie
SERIAL_PORT = "COM3"  # Windows
SERIAL_PORT = "/tmp/COM3"  # Linux/macOS

# Velocidad
BAUDRATE = 19200

# Delay entre paquetes
DELAY_BETWEEN_PACKETS = 0.1  # segundos

# Archivo de log
LOG_FILE = LOG_FILE_3  # Cambiar a LOG_FILE_1 o LOG_FILE_2
```

## 🐛 Solución de Problemas

### "Puerto serie no encontrado"
**Windows:**
- Verifica que COM3 existe en Administrador de dispositivos
- O instala "Virtual Serial Port Driver"

**Linux:**
- Ejecuta: `python src/run_simulation.py`
- O instala socat: `sudo apt-get install socat`

### "Permiso denegado" (Linux)
```bash
# Opción 1: Ejecutar con sudo
sudo python src/simulator.py

# Opción 2: Agregar usuario al grupo dialout
sudo usermod -a -G dialout $USER
# Luego cierra sesión y vuelve a iniciar
```

### "La aplicación no recibe datos"
1. Verifica que ambos programas usan el mismo puerto
2. Asegúrate de que el puerto está disponible
3. Comprueba la velocidad en baudios (debe ser 19200)
4. En Linux/macOS, verifica que socat está ejecutándose

## 📁 Estructura de Archivos

```
VisorExternoUWFCustom/
├── src/
│   ├── main.py                 # Aplicación principal
│   ├── simulator.py            # Simulador
│   ├── quick_start.py          # Menú interactivo
│   ├── run_simulation.py       # Ejecución automática
│   ├── config.py               # Configuración
│   ├── test_simulator.py       # Pruebas
│   └── requirements.txt        # Dependencias
├── logs_uwf_protocol/
│   └── conteo hasta 10000_2.txt # Datos de prueba
├── reverse_eng_protocol.md     # Documentación del protocolo
├── SIMULACION_README.md        # Documentación completa
└── GUIA_SIMULACION.md          # Esta guía
```

## 📚 Documentación Adicional

- **`reverse_eng_protocol.md`** - Detalles técnicos del protocolo UWF
- **`SIMULACION_README.md`** - Documentación completa
- **`src/SIMULATOR_README.md`** - Documentación del simulador

## 🎓 Conceptos Clave

### Protocolo UWF
- **Velocidad:** 19200 bps
- **Estructura:** STX + HEADER + DATOS + ETX + CHECKSUM
- **Datos:** Monto (14 dígitos) + Piezas (4 dígitos)

### Contador Acumulativo
- Detecta cuando el contador se reinicia (9999 → 0)
- Mantiene un total acumulado correcto
- Implementado en la clase `CumulativeCounter`

### Máquina de Estados
- **WAITING_FOR_STX:** Esperando inicio de paquete
- **READING_PAYLOAD:** Leyendo datos del paquete
- Procesa datos en tiempo real sin bloquear la GUI

## ✅ Checklist de Verificación

- [ ] Python 3.7+ instalado
- [ ] `pyserial` instalado (`pip install pyserial`)
- [ ] `socat` instalado (Linux/macOS)
- [ ] Archivo de datos existe: `logs_uwf_protocol/conteo hasta 10000_2.txt`
- [ ] Pruebas pasan: `python src/test_simulator.py`
- [ ] Aplicación se inicia: `python src/main.py`
- [ ] Simulador se inicia: `python src/simulator.py`
- [ ] Datos se reciben en tiempo real

## 📞 Soporte

Para más información:
1. Consulta `reverse_eng_protocol.md` para detalles del protocolo
2. Revisa `SIMULACION_README.md` para documentación completa
3. Ejecuta `python src/test_simulator.py` para verificar la instalación

---

**Última actualización:** 2025-10-16
**Versión:** 1.0

