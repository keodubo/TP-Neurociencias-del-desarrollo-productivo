# Presentación HTML — Sueño, memoria y señales fisiológicas

Deck en **reveal.js** (estética editorial clara) + **guion** para el TP de Neurociencias del Desarrollo Productivo.
Conecta el experimento (sueño · memoria · EEG) con **las 10 clases teóricas** del curso.

## Cómo presentar

1. Abrí **`index.html`** en un navegador (Chrome/Edge/Firefox/Safari). Funciona **sin internet**: reveal.js, fuentes, figuras e imágenes están vendorizados localmente.
2. Navegación: **→ / Space** avanza, **←** retrocede, **`F`** pantalla completa, **`Esc`** vista general, **`.`** pausa (pantalla negra).
3. **Vista de orador (notas + cronómetro):** apretá **`S`**. Se abre una segunda ventana con el guion de cada slide, el reloj y la próxima diapositiva. Ideal para la defensa.

> Para que la vista de orador funcione, permití *pop-ups* del archivo local en el navegador.

## Exportar a PDF (respaldo)

Opción rápida (Chrome/Edge):
1. Abrí `index.html?print-pdf` en Chrome.
2. `Cmd/Ctrl + P` → Destino **Guardar como PDF** → Márgenes **Ninguno** → activar **Gráficos de fondo** → tamaño horizontal.
3. Guardá como `presentacion.pdf`.

Opción CLI (si tenés Node):
```bash
npx decktape reveal "index.html" presentacion.pdf -s 1280x720
```

## Estructura

```
presentacion-integrada-html/
├── index.html              # el deck (23 diapositivas + 3 de apéndice), con speaker notes
├── guion.md                # guion con reparto de oradores, Q&A y checklist
├── design.md               # decisiones de diseño (trazabilidad)
├── css/
│   ├── editorial.css        # tema propio "editorial científico"
│   ├── reveal.css, reset.css
│   └── fonts/               # Fraunces + Inter (woff2, offline)
├── js/
│   ├── reveal.js + plugin/  # reveal.js 5.1.0 (notes, highlight, zoom)
│   └── eeg-waves.js         # ondas EEG animadas, sintetizadas desde la potencia real
├── scripts/gen_figuras.py   # regenera las figuras de datos (paleta + etiquetas)
└── assets/
    ├── figuras/             # figuras de datos (EEG + memoria), etiquetas S3/S4
    ├── fotos/               # fotos reales del experimento
    ├── diagramas/           # (reservado para diagramas generados)
    └── web/                 # imágenes CC de Wikimedia + LICENSES.md
```

## Notas importantes

- **Animaciones de onda:** la portada y la slide "Cómo se ve el EEG en cada fase" muestran trazas EEG **sintetizadas en vivo a partir de la potencia de banda real** de cada fase (canvas, `js/eeg-waves.js`). Respetan `prefers-reduced-motion` (caen a un frame estático) y solo animan la slide visible.
- **Integración con la materia:** los conceptos de todas las clases están tejidos en el contenido (cadena conceptual, marco, discusión), **sin etiquetar números de clase** en pantalla.
- **Clave de scoring:** se usa la clave de la cátedra confirmada — código **2 = S3** y **3 = S4** (sin S2 separado, sin REM). Todas las figuras y textos reflejan esto.
- **Lenguaje:** "compatible con / apoyo descriptivo / proxy de sigma". Evitar "demostrado / causal".
- **Atribución:** las imágenes CC BY de `assets/web/` llevan crédito en su `figcaption`. Ver `assets/web/LICENSES.md`.
- **Regenerar figuras:** `analysis/.venv/bin/python scripts/gen_figuras.py` (desde la raíz del TP).

## Créditos de datos

- Memoria: planilla propia (Equipo 1), 4 sujetos.
- EEG de sueño: dataset secundario BrainVision de la cátedra (otra persona).
- Análisis EEG: MNE 1.12.1 sobre canal C3 (C4 descartado por artefactos).
