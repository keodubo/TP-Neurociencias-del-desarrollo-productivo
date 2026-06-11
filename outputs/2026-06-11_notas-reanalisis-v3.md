# Notas del reanalisis y compilacion (v3)

Fecha: 2026-06-11 · Exposicion: 18/6/2026
Integrantes: Keoni Dubovitsky, Joaquin Pelufo, Sergio Tenoch Sil Cruz.

## Que se rehizo en v3 y por que

El analisis EEG previo (v1) promediaba C3+C4 y calculaba la potencia espectral **sin
filtrar**, lo que inflaba la banda delta en todas las fases e invertia el patron entre
S2 y S3. La v3 corrige esto y suma el diseno experimental y el grupo control.

## Diseno del experimento

Tres etapas, **dos condiciones**:
1. **TR** -- todos aprenden/recuerdan las asociaciones de palabras (linea de base).
2. **Intervalo** -- condicion **sueno**: siesta de 90 min (consolidacion); **grupo
   control**: permanece en **vigilia** (3 sujetos despiertos).
3. **TS** -- ambos vuelven a evaluar; se compara la consolidacion entre condiciones.

## Decisiones clave (para defender en la exposicion)

1. **Scoring.** El archivo `data/S3PRACTICA.txt` contiene los codigos `0,1,2,3` =
   Vigilia, S1, S2, **S3/SWS** (descenso NREM consecutivo). El registro **llego hasta
   S3** (sueno profundo). Por la duracion (~90 min) podia esperarse S4 o REM, pero **no
   aparecen**. Solo se usa la primera columna del `.txt`.
2. **Control de calidad de canal.** C4 resulto malo (std ~513 uV, ~18x C3, con
   saturacion). Se **descarta C4** y se analiza **C3**.
3. **Filtros antes del analisis:** notch 50 Hz + pasa banda 0.3-35 Hz; epocas de 30 s
   sin solapamiento alineadas al scoring.
4. **Husos:** sigma 12-15 Hz como **proxy descriptivo** (sin detector formal).
5. **Sin correlacion husos-memoria:** EEG y memoria son fuentes/sujetos distintos; el
   vinculo se integra a nivel teorico.

## Resultados principales (C3, filtrado)

- Fases: Vigilia 13.8% | S1 17.6% | S2 40.9% | S3/SWS 27.7%. Sin REM ni S4.
- Latencias: sueno 4.0 min; S2 7.5 min; S3 45.5 min. Eficiencia 86%.
- Bloque S3/SWS sostenido: 45.5-68.0 min.
- Delta relativa crece con la profundidad: 57% (Vigilia) -> 92% (S3).
- Husos: sigma absoluta maxima en S2 (11.6 uV^2).
- Memoria: palabra objetivo sueno 17/20 vs control vigilia 5/20 promedio (descriptivo, n=1).

## Entorno y reproduccion

- Python 3.12 en `analysis/.venv`; MNE 1.12.1 (ver `analysis/requirements_v3.txt`).
- EEG: `analysis/.venv/bin/python analysis/analyze_eeg_mne_v3.py`
- Memoria: `analysis/.venv/bin/python analysis/analyze_memory.py`
- LaTeX: TeX Live 2025 (BasicTeX), `pdflatex` (sin `latexmk`). Dos pasadas por archivo.

## Notas de formato (segun pedidos del equipo)

- Sin "equipo" en ningun lado; portada con integrantes y fecha 18/6/2026.
- **Sin lineas de fuente** en las diapositivas ni en los pies de figura.
- Teoria **relacionada con el TP**, no re-explicada.
- Los `.tex` usan castellano sin acentos/ene de forma deliberada (compilacion robusta).
- No se uso `tcolorbox` (copia local rota): beamer usa bloques nativos; el guion usa
  cajas con `colortbl`.
- Verificacion: presentacion 20 paginas, **0 overfull**; guion 9 paginas, **0 overfull**.
- **PPTX:** cada slide es una imagen full-bleed del PDF (16:9): visualmente identico,
  no editable como texto.

## Entregables

- `deliverables/` (3 archivos): presentacion PDF + PPTX y guion PDF.
- Reproducibles y fuentes en `outputs/` y `analysis/`. `data/` no se modifico.
