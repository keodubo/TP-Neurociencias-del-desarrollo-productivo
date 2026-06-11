# Spec v1 - Presentacion sueño, memoria y señales fisiologicas

Fecha: 2026-06-11  
Formato objetivo: 19 diapositivas totales, numeradas 0-18  
Duracion objetivo: 12-15 minutos  
Enfoque: narrativa cientifica con apoyos didacticos  
Estado: spec base revisado; la version final usa figuras generadas en `outputs/figures/`

## Tesis central

El practico no se presenta como un experimento fallido. El registro propio con OpenBCI mostro un caso real de no conciliacion del sueño en el sujeto propio, util para discutir variables moduladoras del dormir. Por indicacion docente, el analisis fisiologico de sueño se realiza con datos secundarios scoreados, manteniendo separada la procedencia de cada fuente.

## Decisiones fijadas

- No mezclar el registro propio del sujeto propio OpenBCI con el dataset secundario como si fueran el mismo sujeto, sesion o instrumento.
- Usar formulacion anonimizada por defecto: "sujeto propio OpenBCI". Solo usar nombre propio si hay consentimiento explicito antes de entregar.
- Tratar el no-sueño como limitacion metodologica y como material de discusion teorica.
- Presentar factores reportados por el sujeto propio, si el grupo confirma que pueden compartirse:
  - recuperatorio previo de la materia, con nervios/estres;
  - consumo de cafe;
  - uso de pantallas;
  - cronotipo poco favorable para dormir una siesta a las 16:00;
  - dificultad para dormir en lugares no habituales.
- Tratar otros factores como variables moduladoras plausibles solo si se aclara que no fueron medidas.
- Para EEG, usar profundidad tecnica apoyada en Clase 9: epocas de 30 s, PSG como EEG/EOG/EMG, ritmos, PSD/Welch, filtros, artefactos, espectrograma e hipnograma.
- Para memoria, usar doble score:
  - palabra objetivo: recuperacion lexical/formal;
  - definicion: recuperacion semantica/declarativa.
- Resultados de memoria: mostrar sujetos individuales y resumen por condicion; explicitar que es descriptivo, no inferencial.
- Discusion: integrar consolidacion activa + homeostasis sinaptica, con consolidacion activa como eje principal.

## Fuentes locales usadas

- `TP-Neurociencias-del-desarrollo-productivo/docs/Trabajo práctico 2026_ sueño, memoria y análisis de señales fisiológicas.pdf`
- `TP-Neurociencias-del-desarrollo-productivo/README.md`
- `TP-Neurociencias-del-desarrollo-productivo/data/README.md`
- `TP-Neurociencias-del-desarrollo-productivo/data/PRÁCTICO LABORATORIO EQUIPO 1.xlsx`
- `TP-Neurociencias-del-desarrollo-productivo/data/S3practica.vhdr`
- `TP-Neurociencias-del-desarrollo-productivo/data/S3practica.vmrk`
- `TP-Neurociencias-del-desarrollo-productivo/data/S3PRACTICA.txt`
- `clases teoricas/CLASE 9 - EEG.pptx`
- `outputs/2026-05-05_sueno-y-memoria-clase-3_v1.md`
- `outputs/2026-05-05_clase-7-ritmos-circadianos-higiene-sueno_v1.md`
- `outputs/2026-05-05_clase-6-estres-apunte_v1.md`
- `outputs/2026-05-05_clase-8-farmacos-apunte_v1.md`

## Visuales existentes

- `TP-Neurociencias-del-desarrollo-productivo/assets/Colocando-electrodos.png`
- `TP-Neurociencias-del-desarrollo-productivo/assets/pre-siesta.png`
- `TP-Neurociencias-del-desarrollo-productivo/assets/pre-siesta-listo.png`

## Figuras a generar mas adelante

1. Hipnograma/scoring del dataset secundario, con tramo compatible con ondas lentas resaltado.
2. Espectrograma C3/C4, idealmente 0.3-35 Hz y con banda delta visible.
3. Tabla visual de ritmos cerebrales: delta, theta, alfa, sigma/husos, beta.
4. Grafico de memoria con dos paneles: palabra objetivo y definicion, barras por sujeto y color por condicion.
5. Esquema prudente de no conciliacion en el sujeto propio: estres + cafeina + pantallas + cronotipo + ambiente.

## Datos EEG relevantes para el spec

Registro BrainVision:

- 10 canales.
- Muestreo: 250 Hz.
- Canales:
  - EOG I, EOG D;
  - F3, F4, C3, C4, P3, P4;
  - EMGI, EMGD.
- Software filters: disabled en el header.
- Marcas:
  - ojos lado a lado;
  - ojos arriba/abajo;
  - masticacion;
  - luz off;
  - luz on.

Scoring:

- `S3PRACTICA.txt` tiene 159 filas, compatible con 159 epocas de 30 s.
- La primera columna toma valores 0, 1, 2, 3.
- Interpretacion tentativa, a confirmar:

| Codigo | Interpretacion tentativa | Duracion aprox. |
|---|---:|---:|
| 0 | vigilia / no sueño / artefacto | 11 min |
| 1 | N1 / sueño liviano | 14 min |
| 2 | N2 probable | 32.5 min |
| 3 | N3 / SWS probable | 22 min |

Tramo compatible con sueño de ondas lentas:

| Referencia temporal | Tramo |
|---|---:|
| Desde inicio del registro | 45.5-68.0 min |
| Desde luz off | 44.5-67.0 min |
| Epocas | 92-136 |
| Duracion aprox. | 22.5 min |

Formulacion prudente:

> El tramo mas relevante aparece entre aproximadamente 45.5 y 68.0 min desde el inicio del registro como bloque de codigo 3 en el scoring tentativo. Lo interpretamos como compatible con N3/SWS probable, no como estadificacion clinica definitiva. No se incorporan claims de tono muscular ni validacion clinica sin cuantificacion especifica.

## Datos de memoria preliminares

La planilla tiene cuatro sujetos:

| Sujeto | Condicion |
|---|---|
| Sujeto 1 | Vigilia |
| Sujeto 2 | Vigilia |
| Sujeto 3 | Vigilia |
| Sujeto 4 | Sueño |

Score exploratorio automatico para evaluacion:

| Sujeto | Condicion | Palabra objetivo | Definicion |
|---|---|---:|---:|
| Sujeto 1 | Vigilia | 0/20 | 14/20 |
| Sujeto 2 | Vigilia | 14/20 | 20/20 |
| Sujeto 3 | Vigilia | 1/20 | 18/20 |
| Sujeto 4 | Sueño | 17/20 | 20/20 |

Resumen descriptivo:

| Condicion | n | Palabra objetivo | Definicion |
|---|---:|---:|---:|
| Vigilia | 3 | 5/20 promedio | 17.3/20 promedio |
| Sueño | 1 | 17/20 | 20/20 |

Nota metodologica:

- Estos valores sirven como base para diseñar el grafico.
- Las definiciones deben revisarse manualmente antes del PPT final.
- No presentar como inferencia estadistica: sueño tiene n=1.

---

# Estructura de slides

## Slide 0 - Caratula

**Titulo:** Sueño, memoria y analisis de señales fisiologicas  
**Claim:** Presentamos una actividad experimental sobre sueño y memoria, con una limitacion metodologica real y una estrategia de analisis separada por fuente de datos.

**Contenido en slide:**

- Trabajo practico de Neurociencias del Desarrollo Productivo.
- Equipo: TODO completar integrantes.
- Fecha: TODO completar fecha de presentacion.
- Materia / docente: TODO completar si corresponde.

**Visual sugerido:**

- Foto `pre-siesta-listo.png` como fondo o imagen lateral, con recorte cuidado.

**Notas del orador:**

> Vamos a presentar el objetivo del practico, el procedimiento, que ocurrio durante nuestro registro, como resolvimos metodologicamente esa limitacion y como interpretamos los resultados desde sueño, memoria y señales fisiologicas.

**Fuentes/evidencia:**

- Enunciado oficial del TP.
- Fotos propias en `assets/`.

---

## Slide 1 - Pregunta del practico

**Titulo:** Pregunta de investigacion  
**Claim:** El practico busca relacionar sueño, memoria declarativa y señales fisiologicas medibles.

**Contenido en slide:**

- ¿Como se relaciona dormir con la consolidacion de informacion aprendida?
- ¿Que marcadores fisiologicos permiten identificar sueño?
- ¿Que variables pueden modular que una persona logre dormir en un contexto experimental?

**Visual sugerido:**

- Diagrama simple:
  - aprendizaje de palabras;
  - intento de sueño/siesta;
  - registro fisiologico;
  - evaluacion de memoria.

**Notas del orador:**

> La consigna no pide solamente contar que paso, sino usar el practico para pensar criticamente la relacion entre sueño, memoria, actividad fisiologica y variables que modulan el descanso.

**Fuentes/evidencia:**

- Enunciado oficial del TP.

---

## Slide 2 - Hipotesis integrada

**Titulo:** Hipotesis  
**Claim:** Si hay sueño suficiente, esperamos cambios fisiologicos compatibles con sueño y mejor consolidacion declarativa.

**Contenido en slide:**

- Hipotesis fisiologica:
  - transicion de vigilia a fases de sueño;
  - menor tono muscular;
  - menor actividad ocular voluntaria;
  - cambios espectrales: mas actividad lenta en NREM, posible sigma/husos en N2.
- Hipotesis cognitiva:
  - el sueño deberia favorecer la retencion de palabras/definiciones;
  - el beneficio esperado seria especialmente compatible con memoria declarativa.

**Visual sugerido:**

- Dos columnas:
  - señales fisiologicas;
  - memoria.

**Notas del orador:**

> La hipotesis no es solo "dormir mejora memoria". Tambien esperamos que ese dormir tenga una firma fisiologica: cambios en EEG, EOG y EMG. Esa firma permite conectar el resultado conductual con arquitectura de sueño.

**Fuentes/evidencia:**

- Enunciado oficial.
- Clase 3, sueño y memoria.
- Clase 9, EEG.

---

## Slide 3 - Diseño experimental

**Titulo:** Diseño del procedimiento  
**Claim:** El practico combina una tarea de memoria con registro fisiologico durante un intento de sueño.

**Contenido en slide:**

- Tarea de palabras:
  - entrenamiento;
  - intervalo con vigilia o sueño;
  - evaluacion.
- Registro fisiologico:
  - EEG;
  - EOG;
  - EMG.
- Objetivo:
  - observar si la condicion de sueño se asocia con mejor recuerdo;
  - interpretar el sueño mediante señales fisiologicas.

**Visual sugerido:**

- Timeline horizontal:
  - entrenamiento -> preparacion EEG -> siesta/intervalo -> evaluacion.

**Notas del orador:**

> El diseño apunta a conectar dos niveles: el rendimiento en memoria y la fisiologia del sueño. Para eso necesitamos tanto datos conductuales de la tarea como una manera de identificar etapas de sueño.

**Fuentes/evidencia:**

- Enunciado oficial.
- Planilla `PRÁCTICO LABORATORIO EQUIPO 1.xlsx`.

---

## Slide 4 - Procedimiento real

**Titulo:** Montaje y registro  
**Claim:** La adquisicion requirio preparar electrodos y registrar señales debiles, sensibles a ruido y artefactos.

**Contenido en slide:**

- Colocacion de electrodos y preparacion de piel.
- Registro con canales EEG/EOG/EMG.
- Señales en microvolts: alta sensibilidad a ruido.
- Marcadores del registro: ojos, masticacion, luz off/on.

**Visual sugerido:**

- Foto principal: `Colocando-electrodos.png`.
- Mini-callouts:
  - EEG;
  - EOG;
  - EMG;
  - impedancia / contacto.

**Notas del orador:**

> En EEG no se mide una señal grande y limpia. La clase 9 recalca que son señales del orden de microvolts, que requieren amplificacion, buen contacto de electrodos y control de artefactos. Por eso el procedimiento de colocacion es parte central del metodo.

**Fuentes/evidencia:**

- Clase 9, EEG: adquisicion, impedancia, señales en microvolts.
- `S3practica.vhdr`.

---

## Slide 5 - Evento metodologico: el sujeto propio no durmio

**Titulo:** Lo que ocurrio en nuestro registro  
**Claim:** En nuestro registro OpenBCI, el sujeto propio no logro conciliar sueño; esto se trato como limitacion metodologica y como dato para discutir.

**Contenido en slide:**

- El sujeto propio no logro dormir durante el intento de siesta.
- Factores reportados:
  - recuperatorio previo de la materia;
  - nervios/estres;
  - cafe;
  - pantallas;
  - cronotipo poco favorable a dormir a las 16:00;
  - dificultad para dormir en lugares no habituales.
- Consecuencia:
  - no usamos ese registro como registro de sueño.

**Visual sugerido:**

- Foto `pre-siesta.png` o `pre-siesta-listo.png`.
- Caja pequeña: "No conciliacion del sueño != ausencia de valor experimental".

**Notas del orador:**

> Esto no se presenta como una excusa. Fue una limitacion real del procedimiento. Pero tambien es un caso util porque permite discutir, con contenidos de la materia, que dormir no depende solo de estar acostado y con la luz apagada.

**Fuentes/evidencia:**

- Reporte del participante.
- Indicacion docente comunicada al grupo.

---

## Slide 6 - Decision metodologica

**Titulo:** Separacion de fuentes de datos  
**Claim:** Por indicacion docente, separamos el caso OpenBCI propio del analisis fisiologico de sueño.

**Contenido en slide:**

| Fuente | Uso en la presentacion |
|---|---|
| Registro propio OpenBCI | Discusion de no conciliacion y variables moduladoras |
| Datos secundarios scoreados | Analisis de señales y arquitectura de sueño |
| Planilla de palabras | Analisis descriptivo de memoria por sujeto/condicion |

**Mensaje clave:**

- No mezclamos sujetos ni sesiones como si fueran equivalentes.
- No atribuimos causalidad directa entre datos que no pertenecen al mismo registro.

**Visual sugerido:**

- Tabla limpia con iconos:
  - persona;
  - señal EEG;
  - planilla.

**Notas del orador:**

> Esta es la decision metodologica mas importante. El registro propio sirve para discutir por que no se durmio. El analisis fisiologico de sueño se hace con datos secundarios scoreados. Esa separacion evita una interpretacion incorrecta.

**Fuentes/evidencia:**

- Conversacion con docente.
- `README.md`.
- `data/README.md`.

---

## Slide 7 - Como analizamos EEG

**Titulo:** De señal cruda a arquitectura de sueño  
**Claim:** El analisis usa epocas de 30 s y combina EEG, EOG y EMG para interpretar etapas de sueño.

**Contenido en slide:**

- PSG = EEG + EOG + EMG.
- Epoca = 30 s.
- EEG:
  - ritmos cerebrales;
  - delta/theta/alfa/sigma/beta.
- EOG:
  - movimientos oculares.
- EMG:
  - tono muscular.
- Procesamiento esperado:
  - filtro pasabanda;
  - notch 50 Hz;
  - PSD/Welch;
  - espectrograma.

**Visual sugerido:**

- Mini pipeline:
  - señal -> filtrado -> epocas -> PSD/espectrograma -> scoring/hipnograma.

**Notas del orador:**

> En sueño no basta ver una linea de EEG. La interpretacion combina tiempo, frecuencia y señales auxiliares. Por eso la clase 9 es clave: nos da el puente entre la señal cruda y los indicadores que despues interpretamos teoricamente.

**Fuentes/evidencia:**

- Clase 9, EEG.
- `S3practica.vhdr`.

---

## Slide 8 - Arquitectura de sueño en datos secundarios

**Titulo:** Scoring e hipnograma  
**Claim:** El scoring permite visualizar una progresion temporal compatible con etapas de sueño.

**Contenido en slide:**

- `S3PRACTICA.txt` contiene 159 epocas.
- Cada epoca representa aproximadamente 30 s.
- Interpretacion tentativa:
  - 0: vigilia/no sueño/artefacto;
  - 1: N1;
  - 2: N2;
  - 3: N3/SWS probable.
- Duracion aproximada:
  - codigo 0: 11 min;
  - codigo 1: 14 min;
  - codigo 2: 32.5 min;
  - codigo 3: 22 min.

**Visual sugerido:**

- Figura futura: hipnograma/scoring.
- Marcar "interpretacion tentativa segun scoring provisto y rasgos espectrales".

**Notas del orador:**

> La codificacion del archivo no viene suficientemente documentada, asi que no conviene tratarla como una verdad clinica. Lo que hacemos es presentar el scoring tentativo y apoyarlo con visualizaciones espectrales descriptivas.

**Fuentes/evidencia:**

- `S3PRACTICA.txt`.
- `data/README.md`.

---

## Slide 9 - Tramo compatible con ondas lentas

**Titulo:** Evidencia de sueño de ondas lentas probable  
**Claim:** Entre aproximadamente 45.5 y 68.0 min aparece el tramo mas compatible con N3/SWS.

**Contenido en slide:**

- Tramo principal:
  - 45.5-68.0 min desde inicio del registro.
  - 44.5-67.0 min desde luz off.
  - epocas 92-136.
- Rasgos observados:
  - scoring compatible con codigo 3;
  - bloque prolongado en el hipnograma tentativo;
  - visualizacion tiempo-frecuencia C3/C4 descriptiva;
  - interpretacion compatible con ondas lentas probable, sin validacion clinica.
- Formulacion prudente:
  - "N3/SWS probable", no diagnostico clinico.

**Visual sugerido:**

- Figura futura: hipnograma + espectrograma C3/C4.
- Rectangulo resaltado en 49-68 min.

**Notas del orador:**

> Esta slide es clave. No vamos a decir simplemente "hubo SWS" como afirmacion clinica. Mostramos donde esta el tramo segun scoring tentativo y aclaramos que es una clasificacion probable, no una polisomnografia clinica formal.

**Fuentes/evidencia:**

- Analisis exploratorio de `S3practica.eeg`.
- `S3PRACTICA.txt`.
- Clase 9, EEG.

---

## Slide 10 - Como analizamos memoria

**Titulo:** Doble score de la tarea de palabras  
**Claim:** La tarea permite separar memoria lexical de memoria semantica/declarativa.

**Contenido en slide:**

- Score 1: palabra objetivo.
  - Cuenta recuperacion exacta o normalizada de la palabra rara.
  - Ejemplo: BADINA.
- Score 2: definicion.
  - Cuenta recuperacion correcta o semanticamente equivalente.
  - Ejemplo: "charco de agua".
- Motivo:
  - recordar la forma exacta y recordar el significado no son lo mismo.

**Visual sugerido:**

- Ejemplo de una fila de la planilla, anonimizada si hace falta.
- Dos etiquetas:
  - "forma";
  - "significado".

**Notas del orador:**

> Esta distincion es importante porque el sueño puede no afectar igual todos los componentes de una memoria. En una palabra rara, la forma lexical es mas fragil; la definicion permite evaluar recuperacion semantica.

**Fuentes/evidencia:**

- `PRÁCTICO LABORATORIO EQUIPO 1.xlsx`.
- Clase 1, memoria declarativa.
- Clase 3, sueño y memoria.

---

## Slide 11 - Resultados de memoria

**Titulo:** Rendimiento descriptivo por condicion  
**Claim:** El sujeto en condicion sueño mostro mayor rendimiento descriptivo, especialmente en palabra objetivo.

**Contenido en slide:**

- Mostrar sujetos individuales:
  - Sujeto 1, 2, 3: vigilia;
  - Sujeto 4: sueño.
- Dos paneles:
  - palabra objetivo;
  - definicion.
- Mensaje:
  - sueño: 17/20 palabra, 20/20 definicion;
  - vigilia: promedio 5/20 palabra, 17.3/20 definicion.
- Aclaracion:
  - descriptivo, no inferencial;
  - sueño tiene n=1;
  - revisar manualmente definiciones antes de la version final.

**Visual sugerido:**

- Figura futura: barras por sujeto, color por condicion.
- Nota al pie: "n vigilia = 3; n sueño = 1".

**Notas del orador:**

> El patron es compatible con la hipotesis de beneficio del sueño, pero no alcanza para una conclusion estadistica. Lo valioso para esta presentacion es usar el resultado como punto de partida para discutir mecanismos posibles.

**Fuentes/evidencia:**

- `PRÁCTICO LABORATORIO EQUIPO 1.xlsx`.

---

## Slide 12 - Integracion EEG-memoria

**Titulo:** Señal fisiologica y resultado conductual  
**Claim:** La arquitectura de sueño observada en datos secundarios es compatible con mecanismos que podrian favorecer consolidacion declarativa.

**Contenido en slide:**

- Datos fisiologicos:
  - tramo compatible con N3/SWS probable.
- Datos conductuales:
  - mejor rendimiento descriptivo del sujeto sueño.
- Interpretacion:
  - compatibilidad teorica, no causalidad directa.
- Precaucion:
  - no todos los datos pertenecen necesariamente al mismo sujeto/sesion;
  - no se deben fusionar fuentes.

**Visual sugerido:**

- Diagrama de convergencia:
  - EEG/hipnograma -> sueño con ondas lentas;
  - tarea -> recuerdo;
  - teoria -> consolidacion declarativa.

**Notas del orador:**

> Esta slide evita una sobreinterpretacion. No decimos "el tramo EEG causo este resultado individual". Decimos que el patron fisiologico disponible y el resultado conductual son coherentes con lo que predice la teoria.

**Fuentes/evidencia:**

- Datos secundarios EEG.
- Planilla de palabras.
- Clase 3.

---

## Slide 13 - Por que el sujeto propio no durmio

**Titulo:** Variables que pudieron impedir la conciliacion  
**Claim:** En el sujeto propio pudieron converger factores que aumentan arousal y dificultan una siesta a las 16:00.

**Contenido en slide:**

| Factor | Relacion teorica |
|---|---|
| Recuperatorio previo / estres | arousal, eje HPA, cortisol, vigilancia |
| Cafe | bloqueo de adenosina, menor presion subjetiva de sueño |
| Pantallas | luz y señales circadianas, posible demora de conciliacion |
| Cronotipo | Proceso C poco favorable a esa hora |
| Lugar no habitual | contexto experimental, incomodidad, hiperalerta |
| Dispositivo | cables/electrodos pueden dificultar relajacion |

**Visual sugerido:**

- Esquema futuro con "sujeto propio" en el centro y factores alrededor.

**Notas del orador:**

> Aca hay que ser prudentes. Algunos factores fueron reportados por el sujeto propio; otros son variables teoricas plausibles. La idea es que no hubo una unica causa demostrada, sino una posible convergencia de moduladores que aumentaron la latencia de sueño.

**Fuentes/evidencia:**

- Reporte del participante.
- Clase 7, ritmos circadianos e higiene de sueño.
- Clase 6, estres.
- Clase 8, cafeina/farmacos.

---

## Slide 14 - Consolidacion activa

**Titulo:** Interpretacion 1: consolidacion activa  
**Claim:** Durante NREM/SWS, la reactivacion coordinada puede favorecer memorias declarativas dependientes del hipocampo.

**Contenido en slide:**

- En sueño NREM/SWS:
  - ondas lentas corticales;
  - husos talamocorticales;
  - ripples hipocampales.
- Mecanismo:
  - reactivacion de trazas recientes;
  - dialogo hipocampo-corteza;
  - estabilizacion de memoria declarativa.
- Relacion con el TP:
  - tarea de palabras = material declarativo;
  - tramo compatible con ondas lentas = contexto fisiologico plausible.

**Visual sugerido:**

- Esquema hipocampo -> corteza sincronizado por ondas lentas/husos.

**Notas del orador:**

> La consolidacion activa explica por que no todo descanso equivale a consolidacion. Lo importante es que durante ciertas etapas de sueño se reactive informacion reciente en un estado fisiologico que favorece transferencia y estabilizacion.

**Fuentes/evidencia:**

- Clase 3, sueño y memoria.

---

## Slide 15 - Homeostasis sinaptica

**Titulo:** Interpretacion 2: homeostasis sinaptica  
**Claim:** El sueño tambien puede mejorar la relacion señal/ruido mediante renormalizacion sinaptica.

**Contenido en slide:**

- Vigilia:
  - aprendizaje y experiencia aumentan fuerza sinaptica;
  - se acumula demanda metabolica y ruido.
- Sueño:
  - downscaling global;
  - preservacion relativa de trazas relevantes;
  - mejora de eficiencia y señal/ruido.
- Integracion con consolidacion activa:
  - no son teorias necesariamente opuestas;
  - una explica seleccion/reactivacion;
  - la otra explica renormalizacion global.

**Visual sugerido:**

- Antes/despues:
  - muchas conexiones fuertes/ruidosas;
  - reduccion global con memoria relevante preservada.

**Notas del orador:**

> La homeostasis sinaptica permite explicar por que el sueño no solo "fortalece" todo. Tambien puede reducir ruido y evitar saturacion. En conjunto con consolidacion activa, da una explicacion mas completa.

**Fuentes/evidencia:**

- Clase 3, sueño y memoria.

---

## Slide 16 - Limitaciones

**Titulo:** Limitaciones y cuidados interpretativos  
**Claim:** El valor del analisis depende de reconocer sus limites metodologicos.

**Contenido en slide:**

- El sujeto propio no durmio en el registro OpenBCI.
- EEG de sueño se analiza con datos secundarios.
- `S3PRACTICA.txt` requiere confirmar codificacion exacta.
- Sueño en memoria tiene n=1.
- Definiciones requieren revision manual para scoring final.
- No hay inferencia causal directa entre fuentes distintas.

**Visual sugerido:**

- Checklist de limitaciones con iconos de advertencia discretos.

**Notas del orador:**

> Esta slide es importante para no sobreprometer. La conclusion no es estadistica ni clinica. Es una interpretacion fundada, usando evidencia disponible y separando claramente que dato responde a que parte del practico.

**Fuentes/evidencia:**

- `README.md`.
- `data/README.md`.
- Revision de datos.

---

## Slide 17 - Conclusion

**Titulo:** Conclusion  
**Claim:** El practico permite integrar datos, limitaciones reales y teoria del sueño para explicar memoria y moduladores del descanso.

**Contenido en slide:**

- La no conciliacion del sujeto propio se discute mejor como convergencia posible de factores:
  - estres;
  - cafeina;
  - pantallas;
  - cronotipo;
  - contexto experimental.
- Los datos secundarios permiten observar arquitectura de sueño y un tramo compatible con ondas lentas.
- La tarea de palabras muestra un patron descriptivo compatible con beneficio del sueño.
- La interpretacion mas solida integra:
  - consolidacion activa;
  - homeostasis sinaptica;
  - ritmos circadianos e higiene de sueño.

**Visual sugerido:**

- Diagrama final:
  - variables moduladoras -> sueño;
  - sueño fisiologico -> consolidacion;
  - limitaciones -> interpretacion prudente.

**Notas del orador:**

> La idea final es que el sueño es un proceso biologico activo y modulable. No alcanza con acostarse: importan estado fisiologico, contexto, fase circadiana, sustancias como cafeina y arquitectura real del sueño.

**Fuentes/evidencia:**

- Enunciado oficial.
- Clases 3, 6, 7, 8 y 9.

---

## Slide 18 - Gracias

**Titulo:** Gracias  
**Claim:** Cierre simple para preguntas.

**Contenido en slide:**

- Gracias.
- Preguntas.
- Opcional: email o nombres del equipo.

**Visual sugerido:**

- Imagen sutil del montaje o fondo limpio.

**Notas del orador:**

> Cerrar y abrir a preguntas. Si preguntan por causalidad, volver a la separacion metodologica: datos secundarios para sueño, planilla para memoria, caso propio para no conciliacion.

---

# Checklist de armado PPT

- [ ] Completar nombres de integrantes en slide 0.
- [ ] Confirmar consentimiento para usar fotos y cualquier dato identificatorio.
- [ ] Revisar manualmente score de definiciones.
- [ ] Confirmar, si es posible, codificacion exacta de `S3PRACTICA.txt`.
- [ ] Generar hipnograma/scoring con tramo 49-68 min resaltado.
- [ ] Generar espectrograma C3/C4.
- [ ] Generar grafico de memoria por sujeto y condicion.
- [ ] Armar tabla visual de ritmos cerebrales.
- [ ] Diseñar esquema de factores de no-sueño.
- [ ] Mantener una nota visible: resultados descriptivos, no inferenciales.

# Riesgos y como responder

| Riesgo | Respuesta recomendada |
|---|---|
| "Estan mezclando sujetos" | No: separamos fuente y uso. El sujeto propio se usa para discutir no conciliacion; datos secundarios para analizar sueño. |
| "Como saben que fue SWS?" | No lo afirmamos clinicamente. Lo tratamos como tramo compatible con N3/SWS probable segun scoring tentativo y visualizaciones descriptivas. |
| "El n es muy chico" | Si. Por eso el analisis de memoria es descriptivo y no inferencial. |
| "Por que el sujeto propio no durmio?" | Por posible convergencia de factores reportados y teoricamente plausibles: estres, cafeina, pantallas, cronotipo y contexto. |
| "Cafeina mejora alerta, entonces mejora memoria?" | Puede mejorar alerta transitoria, pero antes de dormir puede aumentar latencia y reducir calidad del sueño necesario para consolidacion. |

# Proxima version sugerida

La v2 deberia convertir este spec en un guion de PPT con:

- copy final por slide, maximo 20-35 palabras visibles;
- notas del orador pulidas;
- figuras ya generadas;
- seleccion/crop final de fotos;
- bibliografia/fuentes en pie de slide o slide final segun criterio de la catedra.
