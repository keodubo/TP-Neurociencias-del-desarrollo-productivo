# Marco teorico y discusion integrada

Fecha: 2026-06-11

## Idea guia

El TP debe presentarse como una actividad experimental con una limitacion metodologica real: el sujeto propio registrado con OpenBCI no durmio. Esa limitacion no invalida el trabajo si se separan las fuentes: la tarea de memoria se analiza por sujeto/condicion y el analisis fisiologico de sueño se realiza sobre un dataset secundario de una persona que si durmio.

## Arquitectura del sueño

El sueño no es un estado de apagado cerebral. Es un estado biologico organizado en fases NREM y REM, con perfiles distintos de EEG, EOG, EMG y modulacion neuroquimica.

- NREM incluye transiciones de sueño liviano y sueño mas profundo.
- N2 suele asociarse con husos de sueño y complejos K.
- N3 o sueño de ondas lentas se caracteriza por actividad lenta de alta amplitud.
- REM combina actividad cortical mas parecida a vigilia, movimientos oculares rapidos y atonia muscular.

Fuentes locales: `../outputs/2026-05-05_sueno-y-memoria-clase-3_v1.md`; `../clases teoricas/CLASE 9 - EEG.pptx`.

## Señales fisiologicas

La polisomnografia combina:

- EEG: actividad cortical;
- EOG: movimientos oculares;
- EMG: tono muscular.

En el dataset secundario se registraron 10 canales: EOG I, EOG D, F3, F4, C3, C4, P3, P4, EMGI y EMGD. Esto permite analizar cambios de actividad cortical, movimientos oculares y tono muscular de forma compatible con la consigna, aunque el scoring disponible debe tratarse como tentativo.

Fuentes locales: `data/S3practica.vhdr`; `data/README.md`; `../clases teoricas/CLASE 9 - EEG.pptx`.

## Sueño y memoria declarativa

La tarea de palabras evalua recuperacion declarativa. En este TP conviene separar dos niveles:

- palabra objetivo: recuperacion lexical/formal;
- definicion: recuperacion semantica/declarativa.

Los resultados muestran una diferencia descriptiva: el sujeto en condicion sueño obtuvo mejor recuperacion formal de palabra objetivo que los sujetos en vigilia, mientras que las definiciones fueron altas en casi todos los sujetos. Esto sugiere que recuperar el significado fue menos exigente que recuperar la forma exacta de las palabras.

Limitacion central: la condicion sueño tiene `n=1`, por lo que no corresponde afirmar causalidad estadistica.

Fuente local: `outputs/2026-06-11_resultados-memoria_v1.md`.

## Consolidacion activa

La teoria de consolidacion activa plantea que durante el sueño, especialmente durante SWS/N3, se reactivan memorias recientes dependientes del hipocampo y se redistribuyen gradualmente hacia redes neocorticales. La coordinacion entre ondas lentas corticales, husos talamocorticales y ripples hipocampales es el mecanismo teorico central.

Conexion con el TP:

- si hubo sueño suficiente, se esperaria una firma fisiologica compatible con NREM y, potencialmente, condiciones favorables para consolidacion declarativa;
- el dataset secundario muestra un bloque compatible con N3/SWS probable;
- la tarea de memoria es compatible con este marco, pero el tamaño muestral impide una conclusion causal fuerte.

Fuente local: `../outputs/2026-05-05_sueno-y-memoria-clase-3_v1.md`.

## Homeostasis sinaptica

La hipotesis de homeostasis sinaptica sostiene que durante la vigilia aumenta globalmente la fuerza sinaptica por aprendizaje y experiencia. Durante NREM/SWS ocurriria un downscaling global que mejora eficiencia, reduce ruido y preserva selectivamente memorias relevantes.

Conexion con el TP:

- complementa la consolidacion activa;
- ayuda a explicar por que el sueño podria mejorar la relacion señal/ruido de memorias relevantes;
- no permite, por si sola, atribuir los resultados individuales a sueño sin controlar otras variables.

Fuente local: `../outputs/2026-05-05_sueno-y-memoria-clase-3_v1.md`.

## Proceso S, Proceso C y cronotipo

El sueño depende de la interaccion entre:

- Proceso S: presion homeostatica de sueño, que aumenta con la vigilia y se relaciona con adenosina;
- Proceso C: modulacion circadiana de la propension al sueño segun la hora biologica.

Una persona puede sentirse cansada y aun asi no dormirse si la fase circadiana, la luz, el contexto experimental o el cronotipo no favorecen dormir en ese momento.

Conexion con el caso propio:

- el no-sueño del sujeto OpenBCI puede discutirse como limitacion metodologica;
- cronotipo, siesta a media tarde, pantallas, cafeina, estres y ambiente no habitual son variables plausibles;
- sin mediciones directas, no deben presentarse como causas confirmadas.

Fuente local: `../outputs/2026-05-05_clase-7-ritmos-circadianos-higiene-sueno_v1.md`.

## Higiene de sueño, cafeina y estres

La higiene de sueño incluye horarios, luz, ambiente, uso de pantallas, sustancias y estres. La cafeina bloquea receptores de adenosina, puede reducir somnolencia subjetiva, aumentar latencia de sueño y disminuir sueño de ondas lentas. El estres puede modular memoria por cortisol/noradrenalina y tambien afectar indirectamente la consolidacion al alterar el sueño.

Conexion con el TP:

- estos factores ayudan a discutir por que el sujeto propio podria no haber conciliado sueño;
- deben formularse como hipotesis plausibles o variables moduladoras, no como hechos demostrados;
- el foco narrativo no es "fallo experimental", sino como el contexto modula el dormir y obliga a separar fuentes.

Fuentes locales: `../outputs/2026-05-05_clase-7-ritmos-circadianos-higiene-sueno_v1.md`; `../outputs/2026-05-05_clase-6-estres-apunte_v1.md`; `../outputs/2026-05-05_clase-8-farmacos-apunte_v1.md`.

## Integracion de resultados

### Analisis fisiologico secundario

El scoring/codificacion secundaria muestra 159 epocas de 30 s. Bajo interpretacion tentativa:

- codigo 0: vigilia/no sueño/artefacto probable;
- codigo 1: N1 probable;
- codigo 2: N2 probable;
- codigo 3: N3/SWS probable.

El tramo compatible con N3/SWS probable se ubica aproximadamente entre 45.5 y 68.0 min desde el inicio del registro, o 44.5 y 67.0 min desde luz off. Esta formulacion debe mantenerse como probable, no clinica.

Fuente local: `outputs/2026-06-11_resultados-eeg_v1.md`.

### Tarea de memoria

Los resultados descriptivos fueron:

| Sujeto | Condicion | Palabra objetivo | Definicion |
|---|---|---:|---:|
| Sujeto 1 | Vigilia | 0/20 | 14/20 |
| Sujeto 2 | Vigilia | 14/20 | 20/20 |
| Sujeto 3 | Vigilia | 1/20 | 18/20 |
| Sujeto 4 | Sueño | 17/20 | 20/20 |

Lectura prudente: el sujeto en condicion sueño rindio mejor en palabra objetivo, pero la comparacion es descriptiva porque el grupo sueño tiene `n=1` y podria estar afectado por diferencias individuales o contextuales.

Fuente local: `outputs/2026-06-11_resultados-memoria_v1.md`.

## Frase segura para la presentacion

> La ausencia de sueño en el registro propio puede discutirse como una limitacion metodologica y como un fenomeno compatible con variables moduladoras del sueño, tales como fase circadiana, cronotipo, higiene de sueño, cafeina, estres, ambiente experimental o adaptacion al dispositivo. Sin mediciones directas, estas variables no deben presentarse como causas individuales confirmadas.

## Conclusion sugerida

El analisis fisiologico secundario mostro una secuencia compatible con sueño NREM y un tramo probable de sueño de ondas lentas. La tarea de memoria mostro, de forma descriptiva, mejor recuperacion formal en el sujeto en condicion sueño y alto rendimiento semantico en casi todos los sujetos. El caso propio sin sueño aporta una limitacion metodologica relevante y una oportunidad de discutir variables circadianas, contextuales y fisiologicas. No se puede concluir causalidad fuerte entre sueño y memoria con este tamaño muestral ni mezclar fuentes como si pertenecieran al mismo sujeto.

