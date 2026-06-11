# Fuentes y requisitos del TP

Fecha: 2026-06-11

## Alcance

Este documento resume los requisitos del trabajo practico sobre sueño, memoria y analisis de señales fisiologicas, usando solo fuentes locales del repositorio.

## Requisitos de la presentacion

| Requisito | Evidencia local |
|---|---|
| Preparar una presentacion grupal en PowerPoint u otro formato adecuado | `docs/Trabajo práctico 2026_ sueño, memoria y análisis de señales fisiológicas.pdf`, p. 1 |
| Incluir objetivo del practico | PDF oficial, p. 1 |
| Formular una o mas hipotesis vinculadas con sueño, memoria y/o señales fisiologicas | PDF oficial, p. 1 |
| Describir metodologia: tarea, datos registrados, que ocurrio, por que la persona no pudo dormir y que se esperaba si dormia | PDF oficial, p. 1 |
| Incorporar fotos del experimento | PDF oficial, p. 1; `assets/` |
| Presentar resultados de señales de sueño y tarea de palabras, en la medida de lo posible | PDF oficial, p. 1 |
| Discutir los resultados integrando contenidos de la materia | PDF oficial, pp. 1-2 |
| Proponer interpretaciones fundamentadas aun si los resultados no fueron esperados | PDF oficial, p. 2 |

## Entregables definidos para esta version

- `outputs/2026-06-11_resultados-memoria_v1.md`
- `outputs/2026-06-11_resultados-eeg_v1.md`
- `outputs/2026-06-11_marco-teorico-discusion_v1.md`
- `outputs/2026-06-11_guion-presentacion-sueno-memoria_v1.md`
- `outputs/2026-06-11_presentacion-sueno-memoria_v1.pptx`
- Figuras generadas en `outputs/figures/`
- Scripts reproducibles en `analysis/`

## Fuentes usadas

### Consigna y estructura del TP

- `AGENTS.md`
- `README.md`
- `docs/README.md`
- `data/README.md`
- `docs/Trabajo práctico 2026_ sueño, memoria y análisis de señales fisiológicas.pdf`
- `outputs/2026-06-11_presentacion-sueno-memoria-spec_v1.md`

### Datos de memoria

- `data/PRÁCTICO LABORATORIO EQUIPO 1.xlsx`

Uso: tabla de tarea de palabras por sujeto y condicion. Se extrajeron respuestas de evaluacion y se separaron dos puntajes:

- palabra objetivo: coincidencia formal normalizada;
- definicion: scoring semantico manual binario.

### Datos fisiologicos secundarios

- `data/S3practica.vhdr`
- `data/S3practica.eeg`
- `data/S3practica.vmrk`
- `data/S3PRACTICA.txt`

Uso: metadatos BrainVision, señal EEG/EOG/EMG, marcadores y scoring/codificacion tentativa.

### Marco teorico local

- `../outputs/2026-05-05_sueno-y-memoria-clase-3_v1.md`
- `../outputs/2026-05-05_clase-7-ritmos-circadianos-higiene-sueno_v1.md`
- `../outputs/2026-05-05_clase-6-estres-apunte_v1.md`
- `../outputs/2026-05-05_clase-8-farmacos-apunte_v1.md`
- `../clases teoricas/CLASE 9 - EEG.pptx`

## Restriccion metodologica central

El sujeto propio registrado con OpenBCI no durmio. Por indicacion de la catedra comunicada al grupo, el analisis fisiologico de sueño debe realizarse con datos secundarios de una persona que si durmio.

Implicancias:

- no mezclar el registro propio y el dataset secundario como si fueran mismo sujeto, sesion o instrumento;
- etiquetar siempre procedencia de datos;
- usar el no-sueño del sujeto propio como limitacion metodologica y discusion teorica;
- formular factores como cafeina, estres, pantallas, cronotipo, fase circadiana, ambiente o incomodidad del dispositivo como variables plausibles, no como causas demostradas si no fueron medidas.

## Riesgos metodologicos

| Riesgo | Mitigacion aplicada |
|---|---|
| Sobreinterpretar el efecto del sueño en memoria con `n=1` en condicion sueño | Reportar resultados como descriptivos y no inferenciales |
| Confundir sujeto propio sin sueño con datos secundarios con sueño | Slides y documentos separan fuentes y procedencia |
| Tratar `S3PRACTICA.txt` como scoring clinico definitivo | Se rotula como codificacion/scoring tentativo |
| Usar nombre propio sin consentimiento | En la presentacion se usa "sujeto propio OpenBCI" por defecto |
| Afirmar causalidad por cafeina/estres/cronotipo | Se presentan como variables moduladoras plausibles |
| Usar datos crudos como archivo de trabajo | Los scripts solo leen `data/` y escriben derivados en `outputs/` |

## Evidencia local por parte del relato

| Parte del TP | Evidencia |
|---|---|
| Objetivo, apartados minimos y criterios | PDF oficial |
| Decision de separar datos propios y secundarios | `README.md`, `data/README.md`, `AGENTS.md` |
| Memoria por sujeto/condicion | `data/PRÁCTICO LABORATORIO EQUIPO 1.xlsx`; `outputs/2026-06-11_resultados-memoria_v1.md` |
| Canales EEG/EOG/EMG y metadatos | `data/S3practica.vhdr`; `outputs/2026-06-11_resultados-eeg_v1.md` |
| Marcadores luz off/on y maniobras iniciales | `data/S3practica.vmrk` |
| Hipnograma tentativo | `data/S3PRACTICA.txt`; `outputs/figures/2026-06-11_eeg_hipnograma_v1.png` |
| Teoria sueño-memoria | Clase 3 local |
| Ritmos circadianos e higiene | Clase 7 local |
| Estres | Clase 6 local |
| Cafeina/farmacologia | Clase 8 local |
| Analisis EEG | Clase 9 local |

