# AGENTS.md

## Alcance

Este repositorio contiene el trabajo práctico 2026 de Neurociencias del Desarrollo Productivo sobre sueño, memoria y análisis de señales fisiológicas.

Trabajá siempre en español y priorizá precisión académica, trazabilidad de fuentes y cambios reversibles.

## Contexto obligatorio

Antes de modificar archivos o proponer análisis, leé:

1. `README.md`
2. `docs/README.md`
3. `data/README.md`
4. `docs/Trabajo práctico 2026_ sueño, memoria y análisis de señales fisiológicas.pdf`

Si necesitás teoría, usá primero el material local disponible. En este workspace puede estar en el repo padre `neurociencias`, en especial clases de sueño/memoria, ritmos circadianos e higiene de sueño. No uses internet salvo pedido explícito.

## Regla metodológica central

El sujeto registrado por el grupo con OpenBCI no durmió durante el práctico. Según la indicación de la cátedra comunicada al grupo, los análisis fisiológicos de sueño deben hacerse con datos secundarios de una persona que sí durmió.

Por lo tanto:

- No mezcles el registro propio sin sueño con los datos secundarios con sueño como si fueran el mismo sujeto, sesión o instrumento.
- Etiquetá siempre la procedencia de los datos.
- Tratá el no-sueño del sujeto OpenBCI como limitación experimental y objeto de discusión.
- Justificá hipótesis de no conciliación con lenguaje prudente: cronotipo, fase circadiana, higiene de sueño, cafeína, estrés, ambiente experimental, incomodidad del dispositivo o activación fisiológica.
- No inventes datos personales ni causas no observadas.
- Separá resultados descriptivos de inferencias causales.

## Convenciones de archivos

- Documentación compartible: Markdown por defecto.
- Enunciados y material oficial: `docs/`.
- Datos crudos o provistos: `data/`.
- Código/notebooks futuros: `analysis/`.
- Figuras, tablas, informes y presentaciones generadas: `outputs/`.
- Usá nombres claros y con fecha cuando crees entregables nuevos: `YYYY-MM-DD_topic_v1.md`.

## Manejo de datos

- No borres, muevas ni sobrescribas datos crudos sin confirmación explícita.
- No pegues información sensible o identificatoria en respuestas, commits o documentos.
- Si generás derivados, documentá fuente, transformación y fecha.
- Si un archivo tiene codificación o scoring ambiguo, marcá el supuesto y pedí confirmación antes de usarlo como evidencia fuerte.

## Estilo de análisis

- Citá rutas locales cuando uses fuentes del repositorio.
- Explicá supuestos, limitaciones y alternativas.
- Para el práctico, conectá resultados con:
  - arquitectura del sueño;
  - consolidación activa;
  - homeostasis sináptica;
  - memoria declarativa;
  - cronotipo y ritmos circadianos;
  - higiene de sueño;
  - cafeína, estrés y contexto experimental.

## Testing y código futuro

Si se agrega código, los tests implementados por Codex deben ser unitarios, de caja negra y orientados a comportamiento observable. No agregues tests que dependan de métodos privados, orden interno de llamadas, detalles de implementación o inspección de estructura interna.

## Revisión antes de cerrar

Antes de finalizar una tarea:

1. Revisá `git status --short --branch`.
2. Revisá el diff de los archivos modificados.
3. Confirmá que no se hayan tocado datos crudos salvo pedido explícito.
4. Resumí cambios en formato diff-like: agregado, actualizado, removido.
