# Análisis de Protocolo de Comunicación de la UWF (Visor Externo)

## Conexion configuracion
- **Protocolo:** RS232
- **BaudRate:** 19200 bps
- **Data Bits:** 8
- **Stop Bits:** 1
- **Parity:** None
  


## Estructura General del Mensaje

```
POSICIÓN  | BYTES      | CAMPO                           | DESCRIPCIÓN
----------|------------|---------------------------------|-------------------------------------------
1         | 02         | STX                             | Inicio de transmisión
2-3       | 30 30      | UNKNOWN_1                       | Propósito desconocido (investigar)
4         | 30/31      | STATUS                          | 0x31 = Activo, 0x30 = Standby (tambien a cambiado a 34 y 35)
5         | 31         | UNKNOWN_2                       | varia entre 0x30, 0x31 y 0x32
6         | 30/31      | UNKNOWN_3                       | Variable (investigar condiciones)
7         | 30/31      | RECHAZO_SENSOR                  | 0x31 = Activo, 0x30 = Inactivo
8-22      | 28 bytes   | MONTO_CONTADO                   | Valor monetario (14 dígitos, der→izq)
23-24     | 2 bytes    | UNKNOWN_4                       | Propósito desconocido 
25-28     | 4 bytes    | CONTADOR_PIEZAS                 | Cantidad de piezas contadas
29        | 03         | ETX                             | Fin de transmisión
30        | 3A (var)   | CHECKSUM                        | Verificación de integridad
```

## Desglose Detallado

### Cabecera (Posiciones 1-7)
- **STX (Pos 1):** Delimitador de inicio
- **UNKNOWN_1 (Pos 2-3):** Investigar si es versión, tipo de dispositivo, o flag de configuración
- **STATUS (Pos 4):** Estado operativo del dispositivo
- **UNKNOWN_2 (Pos 5):** Valor constante (posible padding o flag fijo)
- **UNKNOWN_3 (Pos 6):** Variable según condiciones (¿modo de operación?)
- **RECHAZO_SENSOR (Pos 7):** Estado del sensor de rechazo/validación

### Datos (Posiciones 8-27)
- **MONTO_CONTADO (Pos 8-22):** 
  - 14 dígitos en formato ASCII
  - Llena de izquierda con ceros
  - Orden: **derecha a izquierda** (little-endian en representación decimal)
  - Ejemplo: `3030303030303030363031303030` = 601000 
  
- **UNKNOWN_4 (Pos 23-24):**
  - 2 bytes sin identificar
  - Posible relación con conteo de piezas o validaciones
  - Requiere más muestras para análisis
  
- **CONTADOR_PIEZAS (Pos 25-28):**
  - 4 dígitos ASCII
  - Confirmado: cuenta de piezas contadas

### Cola (Posiciones 29-30)
- **ETX (Pos 29):** Delimitador de fin
- **CHECKSUM (Pos 30):** Valor variable (posible CRC o suma de verificación)

---

## Ejemplo Práctico

```
Mensaje: 02 30 30 30 31 30 31 30 30 30 30 30 30 30 30 36 30 31 30 30 30 30 30 30 30 30 37 38 03 3b

Decodificación:
┌─────────────────────────────┬──────--─────┬─────────────────┐
│ Campo                       │ Hex         │ Valor ASCII     │
├─────────────────────────────┼────--───────┼─────────────────┤
│ STX                         │ 02          │ [STX]           │
│ UNKNOWN_1                   │ 30 30       │ 00              │
│ STATUS                      │ 31          │ 1 (Activo)      │
│ UNKNOWN_2                   │ 30          │ 0               │
│ UNKNOWN_3                   │ 30          │ 0               │
│ RECHAZO_SENSOR              │ 30          │ 0 (Inactivo)    │
│ MONTO_CONTADO               │ 30 30 ...   │ 000100000000060 │
│ UNKNOWN_4                   │ 31 30       │ 10              │
│ CONTADOR_PIEZAS             │ 30 30 37 38 │ 0078 = 120      │
│ ETX                         │ 03          │ [ETX]           │
│ CHECKSUM                    │ 3a          │ : (0x3A)        │
└─────────────────────────────┴───────────--┴─────────────────┘
```

---

## Áreas de Investigación Pendiente

1. **UNKNOWN_1 (Pos 2-3):** ¿Identificador de dispositivo, versión o tipo de mensaje?
2. **UNKNOWN_3 (Pos 6):** ¿Qué condiciones hacen que cambie de 0x30 a 0x31?
3. **UNKNOWN_4 (Pos 22-23):** ¿Relacionado con validación de piezas o peso?
4. **CHECKSUM (Pos 29):** ¿Algoritmo utilizado? (CRC-8, suma de bytes, etc.)

## Notas
- Todos los valores numéricos están en formato **ASCII hexadecimal**
- El monto se estructura de **derecha a izquierda** (confirmar si incluye decimales)
- Recolecta más muestras con diferentes estados para validar patrones