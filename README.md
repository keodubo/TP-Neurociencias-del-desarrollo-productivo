# TP Neurociencias del Desarrollo Productivo

Repositorio para el trabajo práctico 2026 sobre sueño, memoria y análisis de señales fisiológicas.

## Objetivo

Organizar el material provisto por la cátedra, los datos disponibles y los futuros análisis para preparar una presentación grupal con:

1. Objetivo del práctico.
2. Hipótesis de trabajo.
3. Metodología del procedimiento.
4. Resultados de señales fisiológicas y tarea de palabras.
5. Discusión teórica integrada con sueño, memoria, ritmos circadianos, higiene de sueño y variables moduladoras.

## Decisión metodológica inicial

Durante el práctico con OpenBCI, el sujeto de prueba no durmió. Según la indicación de la cátedra comunicada al grupo, el análisis de sueño debe apoyarse en datos secundarios provistos por la materia, correspondientes a una persona que sí durmió.

Esto implica:

- El registro propio de OpenBCI se documenta como evento experimental relevante y limitación metodológica.
- Los datos usados para análisis fisiológico de sueño deben tratarse como dataset secundario con sueño, no como continuación directa del registro propio.
- La planilla de tarea de palabras debe analizarse respetando la condición indicada para cada sujeto.
- La presentación debe justificar de forma prudente por qué el sujeto pudo no haber dormido: cronotipo, fase circadiana, higiene de sueño, cafeína, estrés, contexto experimental, incomodidad del dispositivo u otras variables plausibles.
- No se deben afirmar causas personales sin evidencia directa.
- No se deben comparar sujetos, años, equipos o condiciones como si fueran equivalentes sin aclarar la limitación.

## Estructura

```text
docs/
  Enunciados, consignas y material oficial provisto por la cátedra.

data/
  Datos crudos o provistos para el análisis del práctico.

analysis/
  Futuro código o notebooks de análisis, si se agregan.

outputs/
  Futuras figuras, tablas, informes o presentaciones generadas.
```

## Fuentes iniciales

- `docs/Trabajo práctico 2026_ sueño, memoria y análisis de señales fisiológicas.pdf`: consigna oficial del práctico.
- `data/PRÁCTICO LABORATORIO EQUIPO 1.xlsx`: datos crudos de tarea de palabras.
- `data/S3practica.*`: registro fisiológico en formato BrainVision.
- `data/S3PRACTICA.txt`: archivo tabular asociado al scoring o codificación del registro; confirmar codificación antes de analizar.

## Marco teórico recomendado

Para discutir los resultados, priorizar material local de la materia:

- Sueño NREM/REM, hipnograma, EEG, EOG y EMG.
- Consolidación activa durante el sueño.
- Ondas lentas, husos de sueño y reactivación hipocampo-cortical.
- Hipótesis de homeostasis sináptica.
- Proceso S, Proceso C, cronotipo, zeitgebers e higiene de sueño.
- Efectos potenciales de cafeína, estrés, ambiente experimental y privación de sueño.

## Flujo de trabajo v1

1. Mantener originales de `docs/` y `data/` sin editar.
2. Registrar supuestos metodológicos antes de analizar.
3. Separar datos propios sin sueño de datos secundarios con sueño.
4. Generar análisis reproducibles en `analysis/` si se agrega código.
5. Guardar figuras, tablas y presentación final en `outputs/`.
6. Documentar cualquier transformación de datos.

## Próximos pasos sugeridos

- Confirmar la procedencia exacta de cada archivo en `data/`.
- Definir hipótesis de trabajo para memoria y señales fisiológicas.
- Crear un notebook o script de análisis reproducible.
- Generar tablas/figuras para la presentación.
- Armar una discusión que conecte resultados con teoría y limitaciones.
