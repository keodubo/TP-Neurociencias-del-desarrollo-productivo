# Resultados EEG/EOG/EMG - dataset secundario con sueño

Fecha: 2026-06-11

## Procedencia y alcance

- Fuente fisiologica: `data/S3practica.vhdr`, `data/S3practica.eeg`, `data/S3practica.vmrk`.
- Fuente de scoring/codificacion: `data/S3PRACTICA.txt`.
- Estos datos se tratan como dataset secundario de una persona que si durmio. No corresponden al sujeto propio OpenBCI que no durmio.
- La codificacion `0-3` se interpreta en forma tentativa porque no hay clave oficial adjunta.

## Metadatos del registro

- Canales: 10 (`EOG I, EOG D, F3, F4, C3, C4, P3, P4, EMGI, EMGD`).
- Frecuencia de muestreo: 250 Hz.
- Resolucion: 0.1 uV por unidad INT16.
- Duracion del archivo EEG: 4787.02 s (79.78 min).
- Duracion cubierta por scoring: 4770.00 s (79.50 min).

## Marcadores

| Marcador | Muestra | Segundo | Minuto |
|---|---:|---:|---:|
| New Segment | 1 | 0.00 | 0.00 |
| OJOS DE UN LADO AL OTRO | 2691 | 10.76 | 0.18 |
| OJOS ARRIBA ABAJO | 4886 | 19.54 | 0.33 |
| MASTICAR | 10056 | 40.22 | 0.67 |
| MASTICAR | 12896 | 51.58 | 0.86 |
| LUZ OFF | 15691 | 62.76 | 1.05 |
| LUZ ON | 1195226 | 4780.90 | 79.68 |

- Luz apagada: 62.76 s (1.05 min).
- Luz encendida: 4780.90 s (79.68 min).
- Intervalo luz off/on: 78.64 min.

## Scoring tentativo

| Codigo | Interpretacion tentativa | Epocas | Minutos |
|---:|---|---:|---:|
| 0 | 0 - Vigilia/no sueno/artefacto probable | 22 | 11.0 |
| 1 | 1 - N1 probable | 28 | 14.0 |
| 2 | 2 - N2 probable | 65 | 32.5 |
| 3 | 3 - N3/SWS probable | 44 | 22.0 |

- Segunda columna de `S3PRACTICA.txt`: Counter({0: 144, 1: 15}). Se reporta como bandera/codificacion no interpretada.

## Tramos relevantes

| Codigo | Desde epoca | Hasta epoca | Duracion min |
|---:|---:|---:|---:|
| 0 | 1 | 8 | 4.0 |
| 2 | 23 | 29 | 3.5 |
| 2 | 33 | 39 | 3.5 |
| 2 | 47 | 53 | 3.5 |
| 2 | 62 | 68 | 3.5 |
| 2 | 74 | 91 | 9.0 |
| 3 | 92 | 97 | 3.0 |
| 3 | 99 | 136 | 19.0 |
| 1 | 137 | 142 | 3.0 |
| 2 | 147 | 159 | 6.5 |

- Tramo compatible con N3/SWS probable: 45.5-68.0 min desde inicio; 44.5-67.0 min desde luz off.
- Formulacion recomendada: tramo compatible con sueño de ondas lentas probable, no estadificacion clinica definitiva.

## Potencia por banda en C3/C4

| Codigo | Interpretacion | Duracion min | Delta % | Theta % | Alfa % | Sigma % | Beta % |
|---:|---|---:|---:|---:|---:|---:|---:|
| 0 | Vigilia | 11.0 | 77.2 | 13.8 | 3.3 | 0.9 | 1.1 |
| 1 | N1 | 14.0 | 80.7 | 10.3 | 3.3 | 1.2 | 1.8 |
| 2 | N2 | 32.5 | 89.9 | 6.3 | 1.5 | 0.5 | 0.7 |
| 3 | N3/SWS | 22.0 | 66.8 | 23.4 | 3.8 | 0.7 | 1.3 |

## Figuras

- `outputs/figures/2026-06-11_eeg_hipnograma_v1.png`
- `outputs/figures/2026-06-11_eeg_espectrograma_c3_c4_v1.png`
- `outputs/figures/2026-06-11_eeg_ritmos_v1.png`
- `outputs/figures/2026-06-11_eeg_delta_por_scoring_v1.png`

## Lectura prudente

- El scoring secundario muestra una secuencia compatible con arquitectura de sueño NREM, con un bloque prolongado de codigo 3.
- En C3/C4, el analisis espectral permite observar el peso de actividad lenta y ubicar el tramo compatible con ondas lentas.
- Como la clave oficial de `S3PRACTICA.txt` no esta adjunta, la conclusion debe formularse como interpretacion fisiologica probable y no como diagnostico o estadificacion clinica.
