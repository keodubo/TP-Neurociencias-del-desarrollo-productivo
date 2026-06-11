# Resultados EEG con MNE (v3) - dataset secundario con sueno

Fecha: 2026-06-11

## Procedencia y alcance

- Senal: `data/S3practica.vhdr` + `.eeg` + `.vmrk` (BrainVision, 10 canales, 250 Hz).
- Scoring: `data/S3PRACTICA.txt`, **solo primera columna**; la segunda se ignora.
- Dataset **secundario** de una persona que SI durmio. No es el sujeto propio OpenBCI (que no durmio).
- Analisis reproducible: `analysis/analyze_eeg_mne_v3.py` (MNE 1.12.1).

## Interpretacion del scoring

El esquema general de la catedra contempla las fases `0`=Wake, `1`=S1, `2`=S2, `3`=S3 (SWS), `4`=S4 (SWS), `5`=REM, `8`=MT.

El archivo real **solo contiene** los codigos `0` (x22), `1` (x28), `2` (x65), `3` (x44), es decir un descenso NREM consecutivo `0->1->2->3`:

- `0` = Vigilia/transicion, `1` = S1, `2` = S2, `3` = **S3 / SWS** (sueno profundo).
- El registro **llego hasta S3 (SWS)**; no hay `4` (S4), `5` (REM) ni `8` (MT).
- Esto es coherente con la nota de catedra: el registro solo llego a fase 3. Por la duracion (~80-90 min) podria haberse esperado llegar a S4 o a un primer episodio REM, pero **no aparecen** en estos datos.
- Se trabaja con la primera columna del `.txt`; la segunda se ignora.

## Filtros aplicados (antes del analisis)

- Notch 50 Hz (ruido de linea).
- Pasa banda 0.3-35.0 Hz (FIR). Remueve deriva/DC y alta frecuencia; es lo que corrige el sesgo de delta del analisis previo sin filtrar.

## Control de calidad de canales C3/C4

| Canal | std (uV) | P2P aprox (uV) | Frac. saturacion | Estado |
|---|---:|---:|---:|---|
| C3 | 28.1 | 187 | 0.0000 | OK |
| C4 | 513.3 | 5726 | 0.0071 | DESCARTADO (std 513 uV > 150; saturacion 0.71%) |

**C4 presenta artefactos fuertes** (desvio ~18x mayor que C3 y saturacion INT16), por lo que se **descarta** y el analisis espectral usa **C3**. Promediar C4 contaminaba el espectro e invertia el patron de delta entre fases; este es justamente el control de calidad pedido por la catedra.

## Arquitectura del sueno

- Duracion scoreada: 159 epocas x 30 s = 79.5 min.
- Latencia de sueno (primera epoca fuera de Vigilia): 4.0 min (epoca 9).
- Latencia a N2: 7.5 min. Latencia a S3/SWS: 45.5 min.
- Tiempo total de sueno (no Vigilia): 68.5 min (eficiencia 86.2% del registro).
- Bloque principal S3/SWS: 45.5-68.0 min desde el inicio.
- Marcadores: Luz OFF 1.0 min; Luz ON 79.7 min.

## Distribucion de fases

| Fase | Codigo | Epocas | Minutos | % tiempo |
|---|---:|---:|---:|---:|
| Vigilia / transicion (codigo 0) | 0 | 22 | 11.0 | 13.8 |
| S1 - sueno liviano (codigo 1) | 1 | 28 | 14.0 | 17.6 |
| S2 - husos/complejos K (codigo 2) | 2 | 65 | 32.5 | 40.9 |
| S3 / SWS - sueno de ondas lentas (codigo 3) | 3 | 44 | 22.0 | 27.7 |

## Potencia relativa por banda y fase (C3)

| Fase | Delta % | Theta % | Alfa % | Sigma % | Beta % |
|---|---:|---:|---:|---:|---:|
| Vigilia | 57.0 | 8.6 | 15.4 | 2.3 | 14.3 |
| S1 | 55.1 | 18.6 | 9.2 | 2.5 | 11.3 |
| S2 | 68.6 | 15.5 | 4.9 | 5.2 | 2.5 |
| S3/SWS | 91.6 | 5.0 | 1.7 | 0.6 | 0.2 |

## Potencia absoluta por banda y fase (uV^2, C3)

| Fase | Delta | Theta | Alfa | Sigma | Beta |
|---|---:|---:|---:|---:|---:|
| Vigilia | 534.5 | 11.4 | 18.8 | 4.3 | 19.8 |
| S1 | 57.0 | 16.7 | 7.1 | 2.6 | 10.4 |
| S2 | 192.8 | 36.3 | 11.5 | 11.6 | 4.7 |
| S3/SWS | 840.2 | 43.3 | 14.4 | 5.0 | 1.7 |

## Figuras

- `outputs/figures/2026-06-11_eeg_hipnograma_mne_v3.png`
- `outputs/figures/2026-06-11_eeg_porcentaje-fases_v3.png`
- `outputs/figures/2026-06-11_eeg_potencia-bandas-por-fase_v3.png`
- `outputs/figures/2026-06-11_eeg_psd-por-fase_v3.png`
- `outputs/figures/2026-06-11_eeg_espectrograma_c3-c4_mne_v3.png`

## Lectura prudente

- El registro muestra un descenso NREM completo hasta S3/SWS, sin evidencia de REM ni S4.
- Tras el filtrado correcto, **delta crece con la profundidad** y es maxima en S3/SWS, corrigiendo el patron invertido del analisis sin filtrar previo.
- La banda **sigma (12-15 Hz)** se analiza como **proxy descriptivo** de husos; no se aplico un detector formal de husos. Proponer un detector (p. ej. YASA) como trabajo futuro.
- Como el EEG y la tarea de memoria provienen de fuentes distintas, **no se calcula** correlacion directa husos-memoria; el vinculo se integra a nivel teorico.
- Segunda columna de `S3PRACTICA.txt` (ignorada): {0: 144, 1: 15}.
