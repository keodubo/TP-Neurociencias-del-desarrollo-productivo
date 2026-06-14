# Resultados de memoria - tarea de palabras

Fecha: 2026-06-11

## Fuente y procedencia

- Fuente: `data/PRÁCTICO LABORATORIO EQUIPO 1.xlsx`.
- Hojas leidas: cuatro sujetos, con condicion indicada en cada hoja.
- Derivados generados: este informe, CSV de detalle, CSV de resumen, CSV de cambio TR -> TS y figura en `outputs/figures/`.

## Metodo de scoring

- **Palabra objetivo:** coincidencia formal exacta luego de normalizar mayusculas, acentos y signos.
- **Definicion:** scoring semantico manual binario, documentado item por item en el CSV de detalle.
- El analisis es descriptivo. La condicion sueño tiene `n=1`, por lo que no corresponde inferencia estadistica fuerte.

## Tabla por sujeto

| sujeto   | condicion   |   palabra_objetivo |   definicion |   items |
|:---------|:------------|-------------------:|-------------:|--------:|
| Sujeto 1 | Vigilia     |                  0 |           14 |      20 |
| Sujeto 2 | Vigilia     |                 14 |           20 |      20 |
| Sujeto 3 | Vigilia     |                  1 |           18 |      20 |
| Sujeto 4 | Sueño       |                 17 |           20 |      20 |

## Resumen por condicion

| condicion   |   n |   palabra_objetivo_promedio |   definicion_promedio |
|:------------|----:|----------------------------:|----------------------:|
| Vigilia     |   3 |                         5.0 |                  17.3 |
| Sueño       |   1 |                        17.0 |                  20.0 |

## Cambio formal TR -> TS

| sujeto   | condicion   |   palabra_objetivo_TR |   palabra_objetivo_TS |   delta_TS_menos_TR |   items |
|:---------|:------------|----------------------:|----------------------:|--------------------:|--------:|
| Sujeto 1 | Vigilia     |                     0 |                     0 |                   0 |      20 |
| Sujeto 2 | Vigilia     |                    10 |                    14 |                   4 |      20 |
| Sujeto 3 | Vigilia     |                     1 |                     1 |                   0 |      20 |
| Sujeto 4 | Sueño       |                    15 |                    17 |                   2 |      20 |

Lectura: el sujeto en condicion sueño tuvo el desempeño final mas alto en palabra objetivo, pero ya partia de una linea de base alta y su cambio fue +2. Por eso este resultado se reporta como desempeño final alto y mejora descriptiva, no como evidencia causal de mayor consolidacion.

## Figura

![Resultados de memoria](figures/2026-06-11_memoria_scores_v1.png)

## Lectura prudente

- En palabra objetivo, el sujeto en condicion sueño obtuvo el desempeño final mas alto y mostro una mejora TR -> TS de +2.
- El grupo vigilia fue heterogeneo: un sujeto paso de 10/20 a 14/20 y eleva el promedio final del grupo.
- En definicion, el rendimiento es alto en casi todos los sujetos; esto sugiere que la recuperacion semantica fue menos exigente que la recuperacion formal de pseudopalabras.
- La diferencia observada no debe atribuirse causalmente al sueño sin aclarar el tamaño muestral y el caracter descriptivo del practico.

## Archivos derivados

- `outputs/2026-06-11_resultados-memoria-detalle_v1.csv`
- `outputs/2026-06-11_resultados-memoria-resumen_v1.csv`
- `outputs/2026-06-11_resultados-memoria-cambio-tr-ts_v1.csv`
- `outputs/figures/2026-06-11_memoria_scores_v1.png`
