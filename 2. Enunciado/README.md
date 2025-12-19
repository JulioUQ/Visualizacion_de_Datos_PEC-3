# Enunciado de la PEC 3

Para hacer frente a esta PAC sobre narrativa de datos con técnicas de visualización, recomendamos estructurar el proceso en varios pasos clave que le guiarán desde la conceptualización hasta la presentación final del proyecto. Aquí le ofrecemos una guía detallada y recursos para cada componente de la entrega:

## **Componente 1: Analítica visual**

El primer paso es analizar el conjunto de datos propuesto mediante técnicas muy sencillas propias de la analítica visual. Se trata, por un lado, de detectar problemas en los datos (y corregirlos), y por otro, de extraer conocimiento de los datos que sea interesante explicar mediante una visualización de datos.

Para ello, el primer paso es ejecutar un notebook interactivo en R que le irá guiando paso a paso, revelando la naturaleza de los datos y planteándose cuestiones que deberá responder pensando en la visualización de datos que creará posteriormente. Puede plantearse cualquier pregunta que le parezca interesante relacionada con el conjunto proporcionado, el cual puede enriquecer con otros que considere que son relevantes para la historia que desea contar.

Debéis instalar R y RStudio (desktop) en este orden, la página de RStudio os proporciona instrucciones sobre cómo hacerlo [aquí](https://posit.co/download/rstudio-desktop). Entonces debéis descargar los siguientes archivos y ponerlos en una misma carpeta:

- [hotel_bookings.csv](https://aula.uoc.edu/courses/69616/files/8541285?wrap=1 "hotel_bookings.csv") [Download hotel_bookings.csv](https://aula.uoc.edu/courses/69616/files/8541285/download?download_frd=1): fichero CSV con los datos a explorar.
- [hotel_bookings.Rmd](https://aula.uoc.edu/courses/69616/files/8541281?wrap=1 "hotel_bookings.Rmd") [Download hotel_bookings.Rmd](https://aula.uoc.edu/courses/69616/files/8541281/download?download_frd=1): notebook a ejecutar para hacer el análisis visual.

Primero de todo os recomendamos leer el [artículo original](https://aula.uoc.edu/courses/69616/files/8541291?wrap=1 "hotel_bookings_paper.pdf")donde se describe el conjunto de datos, que os permitirá entender las variables que describen cada una de las reservas hechas en dos hoteles de Portugal, uno en Lisboa y otro en el Algarve. Este conjunto de datos ha sido utilizado en muchos otros trabajos para predecir las cancelaciones mediante técnicas de minería de datos, por ejemplo, o para crear visualizaciones en forma de *dashboards* para entender los datos y hacerse preguntas interesantes, como en este otro [artículo](https://aula.uoc.edu/courses/69616/files/8541296?wrap=1 "Design-of-Dashboards-for-CRM-Associated-with-Health-and-Wellbeing-Tourism.pdf") el cual os puede servir de inspiración.

Para ejecutar el notebook con el ejemplo guiado, si hacéis doble clic sobre el archivo .Rmd se debería abrir RStudio y entonces podréis ejecutar y visualizar los resultados del análisis. Otra opción es ejecutar RStudio manualmente y abrir el archivo .Rmd que estará en la carpeta donde lo hayáis dejado.

Ejecutad (con la opción Run) el notebook (instalad todos los packages que sean necesarios la primera vez siguiendo las instrucciones de RStudio) y leed detenidamente los textos que describen cada paso, los resultados obtenidos y, opcionalmente, resolved los ejercicios propuestos que os ayudarán a encontrar una posible historia a contar. Para ejecutar el notebook debéis ejecutar la opción "Run All", ya sea desde el menú "Code" -> "Run Region" o desde el icono de "Run".

Todos los ficheros relativos a esta actividad también pueden encontrarse en el [apartado correspondienteLinks to an external site.](https://gitlab.com/UOC/eimt/datascience/MUCD/VD/hotel-bookings) dentro del gitlab de la asignatura.

## **Componente 2: Visualización tipo storytelling**

1) Contextualización y Guión Gráfico:

Objetivo y Usuario: Define qué mensaje deseas comunicar y al que va dirigido, teniendo en cuenta la naturaleza de los datos y el resultado del análisis realizado.

Storyboarding: Crea un guión gráfico que esboce cómo se presentarán los datos. Esto incluye el flujo de información, los gráficos y los elementos interactivos si existen.

2) Selección de Herramientas: Puedes optar por herramientas como Flourish Studio o Infogram para una solución sin código, o librerías de JavaScript, tales como ScrollyTeller o ScrollMagic para una experiencia más personalizada y programada. Tienes muchas otras herramientas tanto gratuitas como libres y propietarias, pero recuerda que lo importante no es la herramienta, sino la historia que quieres contar y la forma de hacerlo.

3) Diseño y Desarrollo:

Narrativa Visual: diseña una historia con estructura narrativa, como inicio, nudo, desenlace y cómo los datos pueden generar tensión o resolver conflictos para mantener el interés.

Visualización de Datos: Elige las técnicas que mejor representen tus datos y elimina cualquier elemento visual que no aporte claridad y valor. Revisa lo trabajado en la PAC anterior para asociar datos con representación gráfica.

Estética: Organiza visualmente los elementos de forma equilibrada y atractiva, usando colores, tipografías y maquetas (layouts) que refuercen el mensaje principal.

Revisión y Ajustes: Aseguraos de revisar vuestra visualización para garantizar que la narrativa es coherente y los elementos visuales son claros y efectivos.

## **Componente 3: Vídeo de presentación**

Guión del Vídeo: Escribe un guión detallado que cubra todos los puntos exigidos: título, descripción, origen de datos, herramientas utilizadas, navegación y análisis de elementos visuales, y reflexiones finales.

Grabación y Edición: Graba tu vídeo asegurando una calidad de audio y visual adecuada. Mantén el vídeo entre 4 y 6 minutos, editando para asegurar claridad y concisión.

Contenido del Vídeo:

- Introducción: Presenta brevemente el objetivo de la visualización.
- Metodología: Explica de dónde provienen los datos y con qué herramientas se ha creado la visualización.
- Demostración: Guía a los espectadores a través de la navegación y elementos interactivos de la visualización.
- Análisis Visual: Discute los tipos de gráficos utilizados, la paleta de colores, la tipografía y cómo estos elementos ayudan a contar la historia.
- Conclusiones: Reflexiona sobre lo que tu visualización aporta al entendimiento del tema y cómo capta la atención del usuario.

Revisión Final: Revisa el vídeo final para asegurarte de que todos los componentes están correctamente integrados y que se respeta el tiempo estipulado.

### **Rúbrica del vídeo**

El vídeo debe contener al menos estos puntos:

1. [10%] Título y descripción de la visualización creada.
2. [20%] Breve presentación del conjunto de datos y resultados de la analítica visual que motivan la historia contada.
3. [10%] Herramienta con la que se ha creado la visualización y las funcionalidades empleadas.
4. [25%] Presentación de la navegación/animación de la visualización creada.
5. [20%] Análisis y justificación de los elementos visuales usados: tipos de gráficos, interacción, colores, textos…
6. [15%] Reflexiones finales sobre qué explica y que aporta la visualización creada y qué formas de captar la atención del usuario se han utilizado.

  ---
## **Recursos adicionales**

Ejemplos de Storytelling con Datos:

- [10 Ejemplos de Narración de DatosLinks to an external site.](https://www.vev.design/blog/data-storytelling-examples)
- [20 Mejores Ejemplos de Narración de DatosLinks to an external site.](https://www.juiceanalytics.com/writing/20-best-data-storytelling-examples)
- [Tutoriales y Guías: Como transformar _insights_ de un cuadro de mando en una narración.Links to an external site.](https://www.youtube.com/watch?v=YC3ncq8QdEY)

