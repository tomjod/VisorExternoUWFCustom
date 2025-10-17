# Lógica de Detección de Desbordamiento y Reinicio

## Problema Original
La lógica anterior no distinguía entre:
1. **Desbordamiento**: Contador llega a 9999 y vuelve a 0 (debe sumar offset)
2. **Reinicio manual**: Usuario presiona reset (debe resetear offset a 0)

Ambos casos mostraban un salto hacia atrás en piezas, pero requerían acciones diferentes.

**Problema crítico**: Si el usuario reseteaba cuando llevaba >5000 piezas, se interpretaba como desbordamiento en lugar de reinicio.

## Solución Nueva
Ahora usamos **TANTO piezas COMO monto** para distinguir entre ambos casos:

### 1. **Desbordamiento (Overflow)** ⚠️
Cuando el contador físico llega a 9999 y vuelve a 0, pero el monto se mantiene igual.

**Condición**:
- `piezas_actual < piezas_anterior` Y diferencia > 5000
- **Y** `monto_actual >= monto_anterior` (monto NO bajó)

**Ejemplo**:
```
Lectura anterior: 9980 piezas, 50000 monto
Lectura actual:   25 piezas,   50000 monto
Diferencia:       9955 piezas (> 5000) ✓ DESBORDAMIENTO
Monto igual:      50000 = 50000 ✓ Confirma desbordamiento

Acción: offset += 10000
Resultado: total = 10000 + 25 = 10025 piezas acumuladas
```

### 2. **Reinicio Manual (Reset)** 🔄
Cuando el usuario presiona "reset" en la máquina, TANTO piezas COMO monto se resetean.

**Condición**:
- `piezas_actual < piezas_anterior` Y diferencia > 5000
- **Y** `monto_actual < monto_anterior` (monto TAMBIÉN bajó)

**Ejemplo**:
```
Lectura anterior: 5000 piezas, 25000 monto
Lectura actual:   0 piezas,   0 monto
Diferencia:       5000 piezas (> 5000) ✓ Salto hacia atrás
Monto bajó:       0 < 25000 ✓ Confirma reinicio manual

Acción: offset = 0
Resultado: total = 0 + 0 = 0 piezas acumuladas
```

### 3. **Reinicio Suave** 🔄
Cuando se resetea desde un valor bajo (sin gran salto).

**Condición**: `piezas_actual < 100` Y `piezas_anterior > 100`

**Ejemplo**:
```
Lectura anterior: 150 piezas
Lectura actual:   0 piezas
Diferencia:       150 (< 5000) - No es gran salto

Acción: offset = 0
Resultado: total = 0 + 0 = 0 piezas acumuladas
```

### 4. **Cambio en Monto (Informativo)** ℹ️
Si el monto baja pero las piezas no, es solo un cambio de modo o ajuste.

## Ventajas de la Nueva Lógica

✅ **Distingue desbordamiento de reinicio**: Usa el monto como confirmación
✅ **Funciona en ambos modos**: Modo piezas (monto=0) y modo dinero
✅ **Más robusta**: Valida con dos parámetros en lugar de uno
✅ **Flexible**: Parámetros configurables
✅ **Mejor logging**: Emojis y mensajes claros para cada tipo de evento
✅ **Maneja casos especiales**: Reinicio suave, cambios de monto, etc.

## Tabla de Decisión

| Piezas ↓ | Monto ↓ | Diferencia | Acción | Evento |
|----------|---------|-----------|--------|--------|
| 9980→25  | 50→50   | >5000     | offset += 10000 | ⚠️ Desbordamiento |
| 5000→0   | 25→0    | >5000     | offset = 0 | 🔄 Reinicio Manual |
| 150→0    | 0→0     | <5000     | offset = 0 | 🔄 Reinicio Suave |
| 100→50   | 50→50   | <5000     | (sin cambio) | Normal |

## Configuración

Si tu contador físico tiene un máximo diferente a 10000:
```python
self.max_counter_value = 9999  # Cambiar según tu máquina
self.overflow_threshold = self.max_counter_value * 0.5  # Se recalcula automáticamente
```

Los umbrales también son ajustables en el método `update()`:
- Reinicio suave: `piezas_actual < 100 and piezas_anterior > 100` → cambiar 100
- Diferencia mínima: `diferencia_piezas > self.overflow_threshold` → cambiar 0.5

