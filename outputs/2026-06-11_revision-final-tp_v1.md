# Revision final del TP

Fecha: 2026-06-11

## Alcance revisado

Se revisaron los entregables generados para el TP de sueño, memoria y analisis de señales fisiologicas:

- `analysis/analyze_memory.py`
- `analysis/analyze_eeg.py`
- `analysis/build_presentation.py`
- `analysis/requirements.txt`
- `outputs/2026-06-11_fuentes-y-requisitos-tp_v1.md`
- `outputs/2026-06-11_resultados-memoria_v1.md`
- `outputs/2026-06-11_resultados-eeg_v1.md`
- `outputs/2026-06-11_marco-teorico-discusion_v1.md`
- `outputs/2026-06-11_presentacion-sueno-memoria-spec_v1.md`
- `outputs/2026-06-11_guion-presentacion-sueno-memoria_v1.md`
- `outputs/2026-06-11_presentacion-sueno-memoria_v1.pptx`
- `outputs/2026-06-11_presentacion-sueno-memoria_ultrabeamer_v3.tex`
- `outputs/2026-06-11_guion-presentacion-sueno-memoria_v3.tex`
- `deliverables/presentacion.pdf`
- `deliverables/presentacion.pptx`
- `deliverables/guion.pdf`
- figuras y assets derivados en `outputs/figures/`

## Consistencia metodologica

| Punto | Estado | Evidencia |
|---|---|---|
| Separacion entre sujeto propio OpenBCI sin sueño y dataset secundario con sueño | OK | La presentacion, guion, marco teorico e informe EEG separan fuentes |
| No mezclar sujetos/sesiones/instrumentos | OK | El dataset BrainVision se rotula como secundario; OpenBCI se usa como limitacion |
| Scoring EEG tratado como tentativo | OK | `outputs/2026-06-11_resultados-eeg_v1.md` |
| Inferencias de memoria prudentes | OK | `outputs/2026-06-11_resultados-memoria_v1.md` marca `n=1` en sueño |
| Nombre propio / datos identificatorios | Corregido | El spec y PPT usan "sujeto propio OpenBCI" por defecto |
| Claims fisiologicos no cuantificados | Corregido | Se removieron afirmaciones no sustentadas por analisis especifico |
| Datos crudos en `data/` | OK | No hay diff sobre `data/` |

## Correcciones aplicadas tras revision

- Se anonimizo el spec para no usar nombre propio sin consentimiento.
- Se bajo el tono fisiologico: la conclusion ahora dice "compatible con N3/SWS probable segun scoring tentativo", no estadificacion clinica.
- Se eliminaron claims no cuantificados sobre tono muscular.
- Se ajusto el tramo EEG a la salida reproducible: 45.5-68.0 min desde inicio y 44.5-67.0 min desde luz off.
- Se agrego `analysis/requirements.txt` para documentar dependencias instaladas localmente.
- Se agrego `node_modules` a `.gitignore` para mantener fuera el enlace local al runtime Node.

## Correcciones de blindaje metodologico aplicadas el 2026-06-14

- Se agrego tabla de cambio formal `TR -> TS` para no presentar consolidacion solo como desempeño final.
- Se reemplazo "aisla el efecto" por lenguaje descriptivo: en un diseño ideal estimaria el efecto; en este TP se interpreta descriptivamente.
- Se cambio "husos" como hallazgo directo por "potencia sigma compatible con husos" cuando corresponde a resultados.
- Se explicito que la codificacion `0/1/2/3` del scoring es una lectura asumida/descriptiva, no estadificacion clinica.
- Se distinguio protocolo de siesta previsto (~90 min) de registro util analizado (79.5 min).
- Se suavizaron cafeina, estres, pantallas y cronotipo como variables plausibles, no causas confirmadas.
- Se regeneraron `deliverables/presentacion.pdf`, `deliverables/presentacion.pptx` y `deliverables/guion.pdf`.

## Verificaciones ejecutadas

| Verificacion | Resultado |
|---|---|
| `analysis/.venv/bin/python analysis/analyze_memory.py` | OK, genero informe y figura de memoria |
| `analysis/.venv/bin/python analysis/analyze_eeg.py` | OK, genero informe y figuras EEG |
| `analysis/.venv/bin/python analysis/build_presentation.py` | OK, genero PPTX y guion |
| Conteo de slides con `python-pptx` sobre PPTX inicial | OK, 19 slides |
| `unzip -t outputs/2026-06-11_presentacion-sueno-memoria_v1.pptx` | OK, sin errores |
| `git diff -- data docs` | OK, sin salida |
| Busqueda de nombre propio y claims fisiologicos fuertes | OK, sin coincidencias en entregables principales |
| `analysis/.venv/bin/python analysis/analyze_memory.py` tras correcciones | OK, genero CSV de cambio TR->TS |
| `pdflatex` x2 sobre presentacion Beamer v3 | OK, 20 paginas, sin overfull/underfull |
| `pdflatex` x2 sobre guion v3 | OK, 10 paginas; advertencia menor de bookmark de `hyperref` |
| Regeneracion de PPTX desde PDF final | OK, 20 slides full-bleed |
| QA visual con contact sheet | OK, sin solapamientos relevantes tras corregir slide de scoring |

## Pendiente antes de entregar

- Confirmar consentimiento para usar fotos propias si se comparten fuera del grupo/catedra.
- Si la catedra provee clave oficial de `S3PRACTICA.txt`, actualizar interpretacion de codigos.
- Si la catedra cuestiona scoring, responder que se uso como lectura descriptiva y que la clave oficial debe confirmarse.

## Estado Git al cierre

Estado observado:

```bash
## main...origin/main
 M analysis/analyze_memory.py
 M deliverables/guion.pdf
 M deliverables/presentacion.pdf
 M deliverables/presentacion.pptx
 M outputs/2026-06-11_guion-presentacion-sueno-memoria_v3.pdf
 M outputs/2026-06-11_guion-presentacion-sueno-memoria_v3.tex
 M outputs/2026-06-11_notas-reanalisis-v3.md
 M outputs/2026-06-11_presentacion-sueno-memoria_ultrabeamer_v3.pdf
 M outputs/2026-06-11_presentacion-sueno-memoria_ultrabeamer_v3.tex
 M outputs/2026-06-11_resultados-memoria-detalle_v1.csv
 M outputs/2026-06-11_resultados-memoria_v1.md
 M outputs/2026-06-11_revision-final-tp_v1.md
?? outputs/2026-06-11_resultados-memoria-cambio-tr-ts_v1.csv
```

Notas:

- `data/` y `docs/` no tienen diff.
- Los auxiliares de LaTeX y previews de QA generados para la revision no quedan como entregables.
- No se hizo commit ni push.

## Diff-like

### Agregado

- `outputs/2026-06-11_resultados-memoria-cambio-tr-ts_v1.csv`: tabla formal TR, TS y Delta.

### Actualizado

- `analysis/analyze_memory.py`: calcula y exporta cambio TR->TS.
- `outputs/2026-06-11_presentacion-sueno-memoria_ultrabeamer_v3.tex`: lenguaje causal suavizado, tabla TR/TS/Delta, sigma como proxy, scoring asumido.
- `outputs/2026-06-11_guion-presentacion-sueno-memoria_v3.tex`: narrativa oral alineada con las correcciones.
- `outputs/2026-06-11_notas-reanalisis-v3.md`: notas de defensa actualizadas.
- `outputs/2026-06-11_resultados-memoria_v1.md`: agrega seccion de cambio TR->TS.
- `deliverables/`: PDFs y PPTX finales regenerados.

### No modificado

- `data/`: sin cambios.
- `docs/`: sin cambios.

### Removido

- Nada.
