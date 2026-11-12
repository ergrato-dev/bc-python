# 01 · De la exploración a la pregunta

⏱️ 45 min

## 🎯 Objetivos

- Distinguir un análisis exploratorio de uno confirmatorio, y saber cuál estás haciendo.
- Convertir una pregunta de tu dominio en algo que los datos pueden responder: población, unidad, métrica y comparación.
- Decidir el análisis **antes** de ver el resultado, y reconocer el jardín de los senderos que se bifurcan.
- Escribir una pregunta que admite un "no" por respuesta.

---

## 1. Explorar y confirmar

La semana 29 exploraste: miraste tus datos sin saber qué ibas a encontrar, con un recorrido fijo, y apuntaste lo que viste. Explorar sirve para **tener ideas**: "parece que el Sur mide más que el Norte".

Esta semana confirmas: decides una pregunta, eliges cómo responderla y aceptas lo que salga. Confirmar sirve para **sostener una afirmación** delante de otra persona: "el Sur mide más que el Norte, entre 2 y 6 unidades, y no es azar".

| | Exploratorio | Confirmatorio |
|---|---|---|
| Empieza con | Datos | Una pregunta |
| Busca | Ideas, problemas, sorpresas | Una respuesta, con su incertidumbre |
| El resultado es | "Parece que..." | "Sí, entre tanto y tanto" o "no se puede decir" |
| Si sale algo raro | Sigues mirando | Lo cuentas, no cambias de método |
| Herramienta de la semana | El notebook | `observatorio hallazgos` |

La trampa es usar los **mismos datos** para tener una idea y para confirmarla. Si miras veinte gráficos, eliges el que muestra una diferencia y luego la "confirmas" con una prueba sobre esos datos, la prueba siempre sale bien: elegiste el gráfico justo porque se veía la diferencia.

## 2. Una pregunta que los datos pueden responder

"¿Qué zona está peor?" no se puede responder con datos. Le faltan cuatro cosas:

| Pieza | Pregunta | Ejemplo |
|---|---|---|
| **Población** | ¿De qué medidas hablas? | Las de la carga 3, del 1 al 30 de marzo |
| **Unidad** | ¿Qué cuenta como un caso? | Una medida (no un día, no un sensor) |
| **Métrica** | ¿Qué número resume "peor"? | La media del valor, en µg/m³ |
| **Comparación** | ¿Peor que qué? | Cada zona frente a cada otra |

Con las cuatro: "en la carga 3, ¿la media de las medidas difiere entre zonas?". Ahora sí hay un cálculo que la responde, y una respuesta que puede ser **no**.

La unidad importa más de lo que parece. Si un sensor del Norte manda 200 medidas al día y uno del Sur 20, comparar "medidas" da al Norte diez veces más peso. Comparar "medias diarias por sensor" da otra respuesta. Ninguna es la correcta en abstracto: depende de qué quieres saber. Lo que no vale es elegir después la que te gusta.

## 3. Decidir antes de mirar

En ciencia se llama **prerregistro**: escribir el análisis antes de tener los datos. En tu Observatorio, una versión ligera basta: antes de ejecutar `hallazgos`, escribe en `informe/README.md` la sección **Pregunta**, con las cuatro piezas, y haz commit. Git guarda la hora: cualquiera puede ver que la pregunta estaba antes que la respuesta.

Lo que decides antes:

- qué etiquetas comparas y con qué métrica;
- qué haces con los valores que faltan (en el Observatorio, se dejan fuera);
- con qué nivel de confianza y qué α (`--confianza 0.95`, `--alfa 0.05`);
- cómo corriges por comparaciones múltiples (teoría 03).

Si después cambias algo, se puede, pero se cuenta: "con α = 0,05 no sale nada; con α = 0,10, dos pares". Lo que no se puede es cambiar en silencio.

## 4. El jardín de los senderos que se bifurcan

Cada decisión de un análisis es una bifurcación: quitar o no los atípicos, usar la media o la mediana, agrupar por día o por semana, incluir o no la carga de prueba. Con cinco decisiones de dos opciones hay 32 análisis posibles. Si pruebas varios y te quedas con el que da un p-valor pequeño, ese p-valor ya no significa nada, aunque cada análisis por separado sea correcto.

No hace falta ninguna mala intención: basta con probar "a ver qué pasa" hasta que algo sale. Por eso:

- el código de `hallazgos` fija las decisiones, y el informe las escribe en su sección **Método**;
- el informe sale de un comando, no de una sesión de notebook en la que ejecutaste celdas a mano;
- un test comprueba que el informe del repositorio es el que sale **hoy** de la instantánea (teoría 04).

## 5. Una pregunta que admite un "no"

En los datos sintéticos del bootcamp, las cinco zonas se generan con la misma distribución. La respuesta honesta a "¿difieren las zonas?" es **no**, y el informe de ejemplo lo dice: "Difieren 0 de 10 pares". Es un hallazgo tan válido como cualquier otro, y a veces el más útil: evita que alguien invierta en arreglar la zona "peor" que en realidad no lo es.

Si tu pregunta solo puede responderse con un "sí" ("¿cuánto mejor es el Sur?"), no es una pregunta: es una conclusión buscando datos.

## ⚠️ Errores comunes

| Error | Consecuencia | Mejor |
|---|---|---|
| Elegir la pregunta después de mirar los gráficos | Una "confirmación" que siempre sale | La pregunta, en un commit, antes de `hallazgos` |
| Una pregunta sin unidad | Un sensor con más medidas pesa más | Decir qué es un caso |
| Cambiar α o quitar atípicos hasta que sale algo | Un p-valor sin significado | Fijarlo antes; si cambias, contarlo |
| Analizar a mano en el notebook | Nadie sabe qué celdas se ejecutaron | Un comando que escribe el informe |
| Ocultar un "no" | Decisiones basadas en una diferencia que no existe | Publicarlo como hallazgo |

## ✅ Qué debes saber al terminar

- La diferencia entre explorar y confirmar, y por qué no se hacen con los mismos datos.
- Las cuatro piezas de una pregunta: población, unidad, métrica y comparación.
- Qué decides antes de ejecutar `hallazgos`, y cómo lo demuestra Git.
- Qué es el jardín de los senderos que se bifurcan, y cómo lo evita un informe generado por un comando.
- Por qué "no difieren" es un hallazgo.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 30](../README.md) | **01 · De la exploración a la pregunta** | [02 · Hallazgos defendibles](02-hallazgos-defendibles.md) |
