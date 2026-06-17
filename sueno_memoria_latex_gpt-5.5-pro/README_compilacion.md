# Entregables LaTeX - Sueño, memoria y señales fisiológicas

Archivos principales:

- `presentacion_sueno_memoria_latex_v1.tex`: presentación en Beamer, formato 16:9.
- `guion_sueno_memoria_latex_v1.tex`: guion de exposición en formato artículo.
- `assets/`: figuras, fotos y gráficos usados por la presentación.

Compilación recomendada:

```bash
pdflatex presentacion_sueno_memoria_latex_v1.tex
pdflatex presentacion_sueno_memoria_latex_v1.tex
pdflatex guion_sueno_memoria_latex_v1.tex
pdflatex guion_sueno_memoria_latex_v1.tex
```

Los PDF ya compilados están incluidos en la carpeta.

Notas metodológicas:

- La tarea de memoria y el EEG se presentan como fuentes separadas.
- El sujeto OpenBCI propio no durmió; se discute como limitación y no como EEG de sueño.
- El EEG de sueño proviene de un dataset secundario BrainVision.
- La banda sigma se trata como proxy compatible con husos, no como detección formal de husos.
- El lenguaje recomendado es: compatible con, apoyo descriptivo, apoyo parcial.
