
## _El Enigma de las Cancelaciones: 37 % de pérdidas que podemos evitar_

## INTRODUCCIÓN · EL PROBLEMA

> **37 por ciento.**
> 
> Este número representa más de **44.000 habitaciones vacías**.  
> 44.000 oportunidades perdidas.  
> 44.000 razones por las que los hoteles en Portugal dejaron de ingresar millones de euros entre 2015 y 2017.
> 
> Imagina que eres director de un hotel en Lisboa.  
> Cada mañana revisas las reservas del día… y descubres que **4 de cada 10 clientes no llegan**.
> 
> La frustración es evidente.  
> Pero la pregunta clave no es si el problema existe, sino **si puede entenderse y anticiparse**.

---

## CONTEXTO Y OBJETIVO

> En esta visualización analizo **119.390 reservas hoteleras** realizadas entre 2015 y 2017 en dos hoteles de Portugal:  
> un **City Hotel en Lisboa** y un **Resort Hotel en el Algarve**.
> 
> El objetivo del proyecto es claro:  
> **identificar patrones de cancelación** y mostrar cómo una narrativa visual puede transformar datos complejos en conocimiento útil para la toma de decisiones.

---

## METODOLOGÍA Y ANALÍTICA VISUAL

> Como punto de partida, realicé una **analítica visual exploratoria** del conjunto de datos, siguiendo el **notebook guiado proporcionado en la asignatura**, que permitió comprender la estructura del dataset, validar las variables más relevantes y detectar patrones iniciales.
> 
> A partir de ese análisis previo, desarrollé este **dashboard interactivo en Python**, utilizando **Streamlit y Plotly**, con el objetivo de combinar **exploración, interactividad y storytelling visual**.
> 
> La navegación está organizada en capítulos mediante pestañas, de forma que el usuario avanza progresivamente desde el problema hasta las conclusiones.

---

## LA PREGUNTA CENTRAL

> La pregunta no es simplemente **por qué se cancelan reservas**,  
> sino **cuándo y en qué condiciones podemos predecirlo**.
> 
> Al observar el conjunto completo, vemos que aproximadamente **el 37 % de las reservas terminan cancelándose**.  
> Sin embargo, este comportamiento no es aleatorio.  
> Los datos revelan **patrones muy claros**.

---

## CULPABLE 1 · EL FACTOR TIEMPO

> El primer factor clave es el **tiempo de anticipación**, o _lead time_.
> 
> En este gráfico utilizo una **agrupación por categorías**, lo que facilita la comparación directa entre distintos niveles de anticipación.
> 
> Las reservas realizadas con **menos de una semana de antelación** presentan tasas de cancelación muy bajas.  
> En cambio, cuando la reserva se hace con **más de seis meses de antelación**, la tasa de cancelación supera el **50 %**.
> 
> El tiempo reduce el compromiso.  
> Cuanto más lejos está la fecha de llegada, mayor es la probabilidad de que el cliente cambie de planes.
> 
> Además, la mayor concentración de reservas se sitúa entre **uno y tres meses**, lo que convierte esta franja en el punto crítico donde actuar.

---

## CULPABLE 2 · CANALES Y FIDELIZACIÓN

> El segundo factor es el **canal de distribución**.
> 
> Más del **80 % de las reservas provienen de agencias online**, como OTAs.  
> Este alcance es positivo, pero tiene un efecto colateral claro: **cancelar es extremadamente sencillo**.
> 
> A esto se suma un problema estructural:  
> **solo el 3 % de los clientes son repetidores**.
> 
> Esto indica una dependencia elevada de clientes nuevos, con bajo nivel de vínculo con el hotel y, por tanto, mayor propensión a cancelar.
> 
> Visualmente, el uso de gráficos de barras y circulares permite identificar rápidamente esta dependencia y comparar proporciones sin ambigüedad.

---

## CULPABLE 3 · POLÍTICAS DE DEPÓSITO

> El tercer factor es la **política de depósitos**.
> 
> En este gráfico apilado se comparan reservas completadas y canceladas según el tipo de depósito.
> 
> Las reservas **sin depósito** presentan tasas de cancelación elevadas, cercanas al 30 %.  
> Pero el resultado más llamativo aparece en las tarifas **no reembolsables**, donde la cancelación es casi total.
> 
> Esto indica un uso especulativo de este tipo de tarifas:  
> el cliente bloquea la reserva y cancela antes de asumir el coste.
> 
> Además, al analizar el **precio medio por noche**, se observa que las habitaciones más caras se cancelan menos, lo que refuerza la idea de que **tener dinero en juego incrementa el compromiso**.

---

## SOLUCIONES Y RECOMENDACIONES

> A partir de estos patrones, el dashboard propone **estrategias concretas**.
> 
> La primera es una **política de depósitos escalonada**, ajustada al lead time.
> 
> La segunda, **reforzar el canal directo**, mediante incentivos y programas de fidelización.
> 
> Y la tercera, trabajar la **comunicación con el cliente** antes de la llegada, para reducir la desconexión entre reserva y estancia.

---

## IMPACTO ECONÓMICO

> La parte final del dashboard permite **simular el impacto económico** de estas medidas.
> 
> Si se reduce la tasa de cancelación en solo **10 puntos porcentuales**, se recuperarían más de **11.000 reservas**, lo que supone aproximadamente **3 millones de euros en ingresos**.
> 
> Esta interactividad refuerza el mensaje principal:  
> pequeñas decisiones estratégicas pueden tener un impacto económico muy significativo.

---

## CONCLUSIÓN FINAL

> Esta visualización muestra cómo la **analítica visual combinada con una narrativa clara** permite comprender mejor fenómenos complejos como las cancelaciones hoteleras.
> 
> Los datos revelan que el problema no es aleatorio, sino estructural, y que puede abordarse desde el diseño de políticas, canales y precios.
> 
> Más allá del sector hotelero, este enfoque demuestra el valor del **storytelling con datos** como herramienta para apoyar la toma de decisiones.
> 
> Porque los datos no solo describen la realidad:  
> **cuando se interpretan correctamente, permiten cambiarla**.
> 
> Gracias por vuestra atención.

---

Si quieres, en el siguiente mensaje puedo:

- Ajustarlo a **5:00 exactos**
    
- Marcar **pausas de respiración**
    
- Adaptarlo a un **tono aún más académico o más divulgativo**
    

Pero tal como está ahora, **es totalmente defendible y seguro para la PEC**.