# Decisiones de diseño — presentación integrada

Trazabilidad de las decisiones tomadas para esta versión (build v1).

## Alcance
- **Defensa del TP, integrada:** el experimento (sueño · memoria · EEG) es el protagonista; el contenido de todas las clases se teje en la cadena conceptual ("Una sola cadena"), el marco teórico y la discusión integrada.
- **Decisión del usuario:** NO etiquetar de qué clase viene cada concepto. Se quitaron los chips de clase, los badges numerados y el apéndice "aporte por clase". La integración queda en el contenido, no en marcadores en pantalla.
- Se conserva el framing honesto del trabajo previo: evidencia *compatible/parcial*, no causal; n=1 en sueño; memoria y EEG como fuentes separadas.

## Modernización / animaciones (pedido del usuario)
- **Ondas EEG animadas data-driven** (Canvas/JS, `js/eeg-waves.js`), elegido sobre React (overhead de build) y GIFs de Python (pesados/estáticos).
- Las trazas se sintetizan sumando sinusoides por banda con amplitud ∝ √(potencia absoluta real por fase) y ráfagas de sigma como husos. Resultado fiel a los datos: S3 = ondas lentas grandes, S2 = husos sobre fondo intermedio, Vigilia = rápida/baja.
- Usadas en: portada (traza de fondo) y slide "Cómo se ve el EEG en cada fase" (4 trazas, una por fase). Barra de progreso de reveal activada. Respeta `prefers-reduced-motion`.

## Estética
- "Editorial científico (claro)": papel `#FBFAF7`, serif Fraunces (titulares) + sans Inter (cuerpo), acento índigo `#4338CA` + teal de datos `#0E7C7B`, coral para cautelas.
- Motor **reveal.js 5.1.0** vendorizado local (offline). Vista de orador (S) con el guion como notas.

## Datos y scoring
- **Clave de scoring (escala estándar de estadificación):** 0=Vigilia, 1=S1, **2=S2, 3=S3**, 4=S4. La columna 1 del `.txt` solo llega al código 3: la fase más profunda alcanzada es S3 (sueño de ondas lentas); no hay S4 ni REM (códigos 4/5/8 ausentes).
- El pico de sigma cae en el código 2 (=S2), justamente la fase donde clásicamente aparecen los husos; aun así se reporta como potencia de banda / *proxy* de husos, **no** como "huso confirmado" con un detector (slides 13 y 16, y nota en el guion).
- Figuras regeneradas con esas etiquetas y la paleta editorial (`scripts/gen_figuras.py`), a partir de los valores cacheados (`outputs/2026-06-11_eeg-resultados-mne_v3.json`) + re-análisis MNE para PSD/espectrograma (canal C3).

## Imágenes
- Figuras de datos propias (EEG + memoria) regeneradas.
- Fotos reales del experimento (copiadas de `outputs/figures/deck-assets` y `sueno_memoria_latex_gpt-5.5-pro/assets`).
- 4 imágenes CC de Wikimedia (EEG 10-20, hipocampo, amígdala, eje HPA) con `assets/web/LICENSES.md`; las CC BY llevan crédito visible.

## Pendientes / mejoras posibles (v2)
- Usar el espectrograma (`assets/figuras/espectrograma.png`) y la PSD (`psd-por-fase.png`) como slide "wow" o apéndice extra si se quiere más densidad de EEG.
- Diagramas conceptuales adicionales (eje HPA, fases de memoria, Proceso S/C) en `assets/diagramas/` si se busca más apoyo visual.
- Clave de scoring resuelta a la escala estándar (2=S2, 3=S3); la columna 1 del `.txt` no supera el código 3, así que el registro no alcanza S4.

## Fuentes del contenido
- Consigna: `docs/Trabajo práctico 2026_… .pdf`; notas: `docs/notas-pre-entrega.rtf`.
- Resultados: `outputs/2026-06-11_resultados-eeg-mne_v3.md`, `…_resultados-memoria_v1.md`, `…_eeg-resultados-mne_v3.json`.
- Marco/clases: apuntes por clase en el repo padre (`outputs/2026-05-05_clase-*.md`).
- Deck previo de referencia: `sueno_memoria_latex_gpt-5.5-pro/` y `deliverables/presentacion.pdf`.
