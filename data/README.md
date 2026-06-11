# data

Carpeta para almacenar los datos obtenidos durante el testeo y los datos provistos por la cátedra para resolver el práctico.

## Regla metodológica clave

El sujeto registrado por el grupo con OpenBCI no durmió durante el práctico. Los datos usados para el análisis fisiológico de sueño deben tratarse como datos secundarios de una persona que sí durmió, usados por recomendación de la cátedra para poder realizar ese análisis. La planilla de tarea de palabras debe interpretarse según la condición indicada para cada sujeto.

En cualquier análisis o presentación:

- aclarar qué datos corresponden al registro propio sin sueño y cuáles al dataset secundario con sueño;
- no presentar ambos como si fueran el mismo sujeto o la misma sesión;
- no atribuir diferencias únicamente al sueño si también cambian sujeto, año, equipo, contexto o procedimiento;
- usar el caso OpenBCI sin sueño para discutir limitaciones, cronotipo, higiene de sueño, estrés, contexto experimental y adaptación al dispositivo.

## Archivos actuales

| Archivo | Tipo | Uso esperado |
|---|---|---|
| `PRÁCTICO LABORATORIO EQUIPO 1.xlsx` | Planilla Excel | Datos crudos de tarea de palabras. Contiene hojas por sujeto; la inspección inicial muestra sujetos en condición vigilia y un sujeto en condición sueño. |
| `S3practica.vhdr` | Header BrainVision | Metadatos del registro fisiológico: 10 canales, muestreo de 250 Hz, unidades en microvoltios. |
| `S3practica.eeg` | Señal BrainVision | Datos binarios de EEG/EOG/EMG asociados al header. |
| `S3practica.vmrk` | Marcadores BrainVision | Marcadores del registro, incluyendo segmento nuevo, movimientos oculares, masticación, luz apagada y luz encendida. |
| `S3PRACTICA.txt` | Texto tabular | Archivo de dos columnas asociado al scoring o codificación del registro. Confirmar el significado exacto de cada columna antes de analizar. |

## Canales registrados

Según `S3practica.vhdr`:

| Canal | Señal |
|---|---|
| EOG I | Electrooculograma izquierdo |
| EOG D | Electrooculograma derecho |
| F3 | EEG frontal |
| F4 | EEG frontal |
| C3 | EEG central |
| C4 | EEG central |
| P3 | EEG parietal |
| P4 | EEG parietal |
| EMGI | Electromiograma izquierdo |
| EMGD | Electromiograma derecho |

## Buenas prácticas

- No editar archivos crudos directamente.
- Guardar derivados en una carpeta separada, por ejemplo `analysis/processed/` u `outputs/`.
- Documentar cualquier limpieza, filtrado, recorte, scoring o transformación.
- Si se agregan datos nuevos, registrar fuente, fecha, condición experimental, sujeto anonimizado y relación con el práctico.
