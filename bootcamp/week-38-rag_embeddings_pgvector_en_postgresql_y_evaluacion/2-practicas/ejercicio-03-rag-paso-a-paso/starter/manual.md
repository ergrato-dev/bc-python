# Manual de mantenimiento de la red de estaciones

## Visitas

Cada estación se visita una vez al mes. En cada visita, el técnico anota en una nota qué hizo: una limpieza, una calibración o la reparación de una avería. Una nota sin lo que se hizo no sirve para el informe.

## Filtro de partículas

El filtro de partículas se cambia cada 30 días, o antes si la caída de presión supera 50 Pa. Un filtro saturado hace que baje el caudal, y el sensor mide menos partículas de las que hay.

Antes de cambiar el filtro, apaga la bomba de muestreo y espera a que la presión se iguale. Después del cambio, haz una prueba de fugas: tapa la entrada y comprueba que el caudal baja a cero en menos de un minuto.

## Toma de aire

La toma de aire se limpia con agua y un cepillo suave en cada visita. Si hay insectos o telarañas, revisa también la malla: una malla rota se cambia, no se repara.

## Calibración del analizador de ozono

El analizador de ozono se calibra cada tres meses con un generador de ozono de referencia. Se ajustan dos puntos: el cero, con aire sin ozono, y la ganancia, con 400 ppb.

Si el analizador da lecturas negativas, el cero se ha desplazado: repite el ajuste del cero antes de la calibración completa. Si la deriva supera 5 ppb en un mes, avisa al laboratorio, porque puede fallar el detector.

## Calibración del sensor de partículas

El sensor de partículas no se calibra en la estación: se envía al laboratorio una vez al año. Mientras tanto, se compara cada semana con la estación de referencia de Centro; una diferencia mayor del 20 % durante tres días seguidos es motivo de envío.

## Cortes de energía

Las estaciones tienen un sistema de alimentación ininterrumpida con cuatro horas de autonomía. Si un corte dura más, la estación se apaga sola y guarda los datos de las últimas 48 horas.

Al volver la corriente, la estación arranca sola, pero los analizadores necesitan 30 minutos para estabilizarse: los datos de esa media hora se marcan como no válidos.

## Comunicaciones

Cada estación envía sus lecturas al servidor cada cinco minutos por la red móvil. Si el servidor no recibe datos de una estación durante una hora, envía una alerta al técnico de guardia.

Si la estación no transmite pero sigue midiendo, los datos se guardan en la tarjeta de memoria durante 30 días y se recuperan en la siguiente visita.

## Averías

Una avería se anota con el equipo, el síntoma y lo que se hizo. Si hay que cambiar una pieza, se pide al almacén con el número de serie del equipo; el plazo habitual es de una semana.

Un equipo que queda fuera de servicio se marca en el servidor, para que sus datos no entren en los informes.

## Seguridad

Antes de abrir un analizador, desconecta la alimentación. Las botellas de gas patrón se transportan sujetas y en posición vertical, y nunca se dejan dentro de la caseta al terminar.
