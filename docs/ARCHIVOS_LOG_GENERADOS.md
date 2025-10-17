# 📊 Archivos de Log Generados - Simulación de Conteo

## 📝 Descripción General

Se han generado 6 archivos de log adicionales con diferentes escenarios de conteo para probar la aplicación con:
- **Desbordamientos de contador** (9999 → 0)
- **Conteos altos** (hasta 50,000 piezas)
- **Diferentes patrones** de incremento

## 📁 Archivos Generados

### 1. `conteo_desbordamiento_simple.txt`
**Propósito:** Probar desbordamiento simple

- **Paquetes:** 115
- **Rango de piezas:** 0 → 9999 → 0 → 9
- **Rango de monto:** 0 → 1,000,900
- **Desbordamientos:** 1 (en paquete 105)
- **Caso de uso:** Verificar que el contador acumulativo detecta el desbordamiento

**Primeros paquetes:**
```
Paquete 1: Monto=0, Piezas=0
Paquete 2: Monto=10,000, Piezas=100
Paquete 3: Monto=20,000, Piezas=200
```

**Últimos paquetes:**
```
Paquete 113: Monto=1,000,700, Piezas=7
Paquete 114: Monto=1,000,800, Piezas=8
Paquete 115: Monto=1,000,900, Piezas=9
```

---

### 2. `conteo_desbordamiento_multiple.txt`
**Propósito:** Probar múltiples desbordamientos

- **Paquetes:** 601
- **Rango de piezas:** 0 → 30,000 (con 3 desbordamientos)
- **Rango de monto:** 0 → 3,000,000
- **Desbordamientos:** 3 (en paquetes 200, 400, 600)
- **Caso de uso:** Verificar que el contador acumulativo maneja múltiples ciclos

**Primeros paquetes:**
```
Paquete 1: Monto=0, Piezas=0
Paquete 2: Monto=5,000, Piezas=50
Paquete 3: Monto=10,000, Piezas=100
```

**Últimos paquetes:**
```
Paquete 599: Monto=2,990,000, Piezas=9900
Paquete 600: Monto=2,995,000, Piezas=9950
Paquete 601: Monto=3,000,000, Piezas=0
```

---

### 3. `conteo_20mil_piezas.txt`
**Propósito:** Conteo hasta 20,000 piezas

- **Paquetes:** 801
- **Rango de piezas:** 0 → 20,000 (con 2 desbordamientos)
- **Rango de monto:** 0 → 3,000,000
- **Desbordamientos:** 2 (en paquetes 400, 800)
- **Caso de uso:** Prueba de conteo prolongado

**Primeros paquetes:**
```
Paquete 1: Monto=0, Piezas=0
Paquete 2: Monto=3,750, Piezas=25
Paquete 3: Monto=7,500, Piezas=50
```

**Últimos paquetes:**
```
Paquete 799: Monto=2,992,500, Piezas=9950
Paquete 800: Monto=2,996,250, Piezas=9975
Paquete 801: Monto=3,000,000, Piezas=0
```

---

### 4. `conteo_50mil_piezas.txt`
**Propósito:** Conteo hasta 50,000 piezas

- **Paquetes:** 501
- **Rango de piezas:** 0 → 50,000 (con 5 desbordamientos)
- **Rango de monto:** 0 → 10,000,000
- **Desbordamientos:** 5 (en paquetes 100, 200, 300, 400, 500)
- **Caso de uso:** Prueba de conteo muy prolongado

**Primeros paquetes:**
```
Paquete 1: Monto=0, Piezas=0
Paquete 2: Monto=20,000, Piezas=100
Paquete 3: Monto=40,000, Piezas=200
```

**Últimos paquetes:**
```
Paquete 499: Monto=9,960,000, Piezas=9800
Paquete 500: Monto=9,980,000, Piezas=9900
Paquete 501: Monto=10,000,000, Piezas=0
```

---

### 5. `conteo_desbordamiento_rapido.txt`
**Propósito:** Conteo acelerado con desbordamiento

- **Paquetes:** 1500
- **Rango de piezas:** 0 → 15,000 (con 1 desbordamiento)
- **Rango de monto:** 0 → 749,500
- **Desbordamientos:** 1 (en paquete 1000)
- **Caso de uso:** Simular conteo rápido de la máquina

**Primeros paquetes:**
```
Paquete 1: Monto=0, Piezas=0
Paquete 2: Monto=500, Piezas=10
Paquete 3: Monto=1,000, Piezas=20
```

---

### 6. `conteo_realista.txt`
**Propósito:** Conteo realista con variaciones

- **Paquetes:** 3449
- **Rango de piezas:** 0 → 25,000
- **Rango de monto:** Variable según incrementos
- **Desbordamientos:** Múltiples
- **Caso de uso:** Simular comportamiento real de la máquina

---

## 🚀 Cómo Usar Estos Archivos

### Opción 1: Cambiar en `src/config.py`

```python
# Edita la línea:
SIMULATOR_CONFIG["log_file"] = LOG_FILE_3  # Cambiar a LOG_FILE_1, 2, 4, 5 o 6

# Luego ejecuta:
python src/simulator.py
```

### Opción 2: Usar el menú interactivo

```bash
python src/quick_start.py
```

Selecciona la opción para ejecutar el simulador y verás los archivos disponibles.

### Opción 3: Ejecutar directamente

```bash
# Edita simulator.py para cambiar LOG_FILE
python src/simulator.py
```

## 📊 Comparación de Archivos

| Archivo | Paquetes | Piezas Máx | Desbordamientos | Monto Máx | Caso de Uso |
|---------|----------|-----------|-----------------|-----------|------------|
| Desbordamiento Simple | 115 | 9,999 | 1 | 1M | Prueba básica |
| Múltiples Desbordamientos | 601 | 9,950 | 3 | 3M | Múltiples ciclos |
| 20K Piezas | 801 | 9,975 | 2 | 3M | Conteo prolongado |
| 50K Piezas | 501 | 9,900 | 5 | 10M | Conteo muy prolongado |
| Desbordamiento Rápido | 1500 | 9,990 | 1 | 749K | Conteo acelerado |
| Realista | 3449 | Variable | Múltiples | Variable | Comportamiento real |

## 🧪 Verificación

Para verificar que los archivos se generaron correctamente:

```bash
python src/test_log_files.py
```

Deberías ver:
```
✅ Paquetes leídos: XXX
📈 Estadísticas:
   Monto mínimo: X
   Monto máximo: X
   Monto promedio: X
📊 Piezas:
   Piezas mínimas: X
   Piezas máximas: X
   Piezas promedio: X
```

## 🔄 Regenerar Archivos

Si necesitas regenerar los archivos:

```bash
python src/generate_log_files.py
```

Esto creará nuevamente todos los 6 archivos en `logs_uwf_protocol/`.

## 📝 Estructura de los Paquetes

Cada paquete tiene la estructura:
```
STX (0x02) + HEADER + MONTO (14 dígitos) + UNKNOWN + PIEZAS (4 dígitos) + ETX (0x03) + CHECKSUM
```

Ejemplo:
```
02 30 30 31 31 30 31 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 03 XX
```

## 🎯 Escenarios de Prueba

### Escenario 1: Desbordamiento Simple
**Archivo:** `conteo_desbordamiento_simple.txt`
- Verifica que el contador acumulativo detecta el desbordamiento
- Verifica que el total acumulado es correcto

### Escenario 2: Múltiples Desbordamientos
**Archivo:** `conteo_desbordamiento_multiple.txt`
- Verifica que el contador maneja múltiples ciclos
- Verifica que el total acumulado llega a 30,000

### Escenario 3: Conteo Prolongado
**Archivo:** `conteo_20mil_piezas.txt`
- Verifica que la aplicación puede procesar muchos paquetes
- Verifica que el contador llega a 20,000

### Escenario 4: Conteo Muy Prolongado
**Archivo:** `conteo_50mil_piezas.txt`
- Verifica que la aplicación puede procesar 50,000 piezas
- Verifica que el contador maneja números grandes

### Escenario 5: Conteo Acelerado
**Archivo:** `conteo_desbordamiento_rapido.txt`
- Verifica que la aplicación puede procesar datos rápidamente
- Verifica que no hay pérdida de datos

### Escenario 6: Comportamiento Realista
**Archivo:** `conteo_realista.txt`
- Simula el comportamiento real de la máquina
- Verifica que la aplicación funciona en condiciones reales

## 📚 Documentación Relacionada

- **`GUIA_SIMULACION.md`** - Guía de uso general
- **`reverse_eng_protocol.md`** - Especificación del protocolo
- **`src/generate_log_files.py`** - Script generador
- **`src/test_log_files.py`** - Script de pruebas

---

**Última actualización:** 2025-10-16
**Versión:** 1.0

