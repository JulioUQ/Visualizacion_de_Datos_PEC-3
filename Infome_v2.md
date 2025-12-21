
---

```yaml
---
title: "PEC 3 - Visualizacion de datos"
subtitle: "StoryTelling"
author: "Julio Úbeda Quesada"
date: "`r format(Sys.time(), '%d/%m/%Y, %H:%M')`"
output:
  pdf_document:
    toc: true
  html_document:
    df_print: paged
    theme: united
    toc: true
    toc_float: true
abstract: |
  En este trabajo se presenta un análisis visual interactivo del conjunto de datos `hotel_bookings.csv`,
  que contiene información sobre reservas de dos hoteles (City Hotel y Resort Hotel) en Portugal.
  El objetivo es realizar una limpieza y preprocesado básico, explorar patrones relevantes (cancelaciones,
  distribución temporal, duración de la estancia, procedencia de clientes, ADR y tipos de cliente),
  y construir visualizaciones interactivas que permitan contar historias basadas en los datos. Se incluyen
  ejemplos concretos de exploración: tasas de cancelación por hotel y mes, distribución de lead_time,
  relación entre ADR y cancelación, uso de tabla interactiva para inspección de registros y gráficas
  interactivas exportables para presentación. El documento está diseñado para ser reproducible en RStudio
  (salida HTML optimizada para interactividad).
---
```

```{r
knitr::opts_chunk$set(
  echo = TRUE,
  eval = TRUE,
  message = FALSE,
  warning = FALSE,
  error = FALSE,
  tidy = TRUE
)
```

```{r
rm(list=ls())
#--------------ESPACIO DE TRABAJO Y RUTAS RELATIVAS---------------#
# Modificar por el path del directorio de trabajo 
home_path  = "~/GitHub/Visualizacion_de_Datos_PEC-3"
data_loc   = paste0(home_path,"/1. Datos/")
file_path_csv = paste0(data_loc, "hotel_bookings.csv")
#--------------PAQUETES NECESARIOS PARA EL CURSO---------------#
Packages = c("ggmosaic", "ggplot2", "fitdistrplus", "MASS", "survival",
             "ggstatsplot", "tidyverse", "plotly", "DT", "lubridate", "scales")
# Instalar los paquetes que no estén instalados
new_packages <- Packages[!(Packages %in% installed.packages()[,"Package"])]
if(length(new_packages)) install.packages(new_packages, dependencies = TRUE)
# Cargar los paquetes
invisible(lapply(Packages, library, character.only = TRUE))

# 1. Preparación del conjunto de datos
## 1.1 Cargar el archivo de datos
df_csv = read.csv(file_path_csv, stringsAsFactors = TRUE)
# Convertir fechas y tipos útiles
df_csv <- df_csv %>%
  mutate(arrival_date = as.Date(paste(arrival_date_year, arrival_date_month, arrival_date_day_of_month, sep = "-"),
                                format = "%Y-%B-%d"),
         arrival_date_month = factor(arrival_date_month, levels = month.name),
         total_nights = stays_in_weekend_nights + stays_in_week_nights,
         is_canceled = as.integer(is_canceled),
         children = as.numeric(as.character(children)),
         babies = as.numeric(as.character(babies)),
         adults = as.numeric(as.character(adults)),
         # tratar NA en children si existen
         children = ifelse(is.na(children), 0, children),
         adr = as.numeric(as.character(adr))
         )
# Vista rápida
options(dplyr.width = Inf)
```

# 1 Introducción

Breve explicación del dataset y objetivos del informe.

- El dataset contiene 119,390 observaciones y 32 variables sobre reservas en dos tipos de hotel (City Hotel y Resort Hotel) en Portugal.
    
- Variables clave: `is_canceled`, `lead_time`, `arrival_date_*`, `stays_in_*`, `adults`, `children`, `meal`, `country`, `market_segment`, `distribution_channel`, `reserved_room_type`, `assigned_room_type`, `adr`, `total_of_special_requests`, `reservation_status`, etc.
    
- Objetivos:
    
    1. Limpiar y preparar los datos.
    2. Responder preguntas de interés mediante visualización.
    3. Construir gráficos interactivos que sirvan para storytelling (cuentas, comparaciones y patrones).
    4. Proveer materiales para la presentación: imágenes exportables y tablas interactivas.

# 2 Abstract (completado)

_(Ver el encabezado YAML — resumen ejecutivo corto del análisis y objetivos)._

# 3 Preparación y limpieza de datos

```{r
# Estructura básica y valores faltantes
glimpse(df_csv)
summary(df_csv$adr)
sum(is.na(df_csv))
# Tabla de NA por columna
na_tab <- sapply(df_csv, function(x) sum(is.na(x)))
na_tab[na_tab > 0]
```

Explicación:

- Detectamos y convertimos fechas `arrival_date`.
    
- Creamos `total_nights` como suma de noches de fin de semana y entre semana.
    
- Coerciones para asegurar que `adr`, `children`, `adults` sean numéricas.
    
- Mostramos valores faltantes para decidir imputación o exclusión.
    

### Tratamiento de valores atípicos y NA

```{r
# Revisar ADR valores negativos o excesivos
sum(df_csv$adr < 0, na.rm = TRUE)
quantile(df_csv$adr, probs = c(0.001, 0.01, 0.5, 0.9, 0.99), na.rm = TRUE)

# Si hay ADR 0 -> podrían ser registros de no-shows o error; contarlos
table(adr_zero = df_csv$adr == 0, useNA = "ifany")

# Para el análisis visual vamos a:
# - eliminar filas con ADR NA
# - limitar lead_time extremo (por ejemplo, top 0.1%) sólo para visualizaciones que lo requieran
df_clean <- df_csv %>%
  filter(!is.na(adr)) %>%
  mutate(lead_time_cut = ifelse(lead_time > quantile(lead_time, 0.999, na.rm=TRUE),
                                quantile(lead_time, 0.999, na.rm=TRUE),
                                lead_time))
nrow(df_clean)
```

Explicación:

- Decidimos eliminar filas con `adr` NA porque ADR es variable central para análisis de ingresos.
    
- Para visualizar `lead_time` capamos valores extremos en una nueva variable `lead_time_cut` para mejorar escalas.
    

# 4 Análisis exploratorio (preguntas guía)

Proponemos responder varias preguntas mediante visualización:

1. ¿Cuál es la tasa de cancelación por hotel y cómo varía por mes?
    
2. ¿Cuál es la distribución de `lead_time` y su relación con cancelaciones?
    
3. ¿Cómo se comporta el `adr` ( Average Daily Rate ) por hotel y por tipo de cliente?
    
4. ¿Qué países/clientes son más frecuentes? (tabla interactiva)
    
5. Duración media de estancia por hotel.
    

# 5 Visualizaciones interactivas

> **Nota**: las gráficas son `ggplot2` + `plotly` (interactividad con hover/zoom), y las tablas con `DT`.

## 5.1 Tasa de cancelación por hotel y mes (gráfico interactivo)

```{r
cancel_month <- df_clean %>%
  group_by(hotel, arrival_date_month) %>%
  summarise(n = n(),
            canceled = sum(is_canceled),
            cancel_rate = canceled / n) %>%
  ungroup() %>%
  mutate(arrival_date_month = factor(arrival_date_month, levels = month.name))

p1 <- ggplot(cancel_month, aes(x = arrival_date_month, y = cancel_rate, group = hotel, color = hotel)) +
  geom_line(size = 1) + geom_point() +
  labs(title = "Tasa de cancelación por hotel y mes",
       x = "Mes", y = "Tasa de cancelación (proporción)") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))
plotly::ggplotly(p1, tooltip = c("x","y","colour"))
```

Explicación:

- Agrupamos por `hotel` y `arrival_date_month` y calculamos la proporción de cancelaciones.
    
- `plotly` permite explorar mes por mes y comparar hoteles.
    

## 5.2 Distribución de lead_time (histograma interactivo + violin por cancelación)

```{r
p2 <- ggplot(df_clean, aes(x = lead_time_cut)) +
  geom_histogram(bins = 50) +
  labs(title = "Distribución de lead_time (recortado en 99.9%)",
       x = "Lead time (días)", y = "Frecuencia") +
  theme_minimal()
ggplotly(p2)

# Violin lead_time por cancelación
p3 <- ggplot(df_clean %>% filter(!is.na(is_canceled)), aes(x = factor(is_canceled), y = lead_time_cut)) +
  geom_violin(trim = TRUE) + geom_boxplot(width = 0.1) +
  labs(title = "Lead time por estado de cancelación", x = "is_canceled (0=no,1=si)", y = "Lead time (días)")
ggplotly(p3)
```

Explicación:

- Histograma para ver la distribución general; violín permite comparar `lead_time` entre cancelados/no-cancelados.
    

## 5.3 ADR por hotel y tipo de cliente (boxplot interactivo)

```{r
p4 <- ggplot(df_clean %>% filter(adr > 0 & adr < quantile(adr, 0.99, na.rm=TRUE)), 
             aes(x = hotel, y = adr, fill = customer_type)) +
  geom_boxplot(position = position_dodge(width = 0.8)) +
  labs(title = "Distribución de ADR por hotel y tipo de cliente",
       x = "Hotel", y = "ADR (eur)") +
  theme_minimal()
ggplotly(p4)
```

Explicación:

- Removemos ADR extremos (top 1%) para evitar que unos pocos registros distorsionen la visual.
    
- Boxplots por `hotel` y `customer_type` ayudan a ver diferencias de precios.
    

## 5.4 Relación ADR vs probabilidad de cancelación (binned + line)

```{r
adr_bins <- df_clean %>%
  filter(adr > 0 & adr < quantile(adr, 0.995, na.rm = TRUE)) %>%
  mutate(adr_bin = cut(adr, breaks = seq(0, ceiling(max(adr, na.rm=TRUE)), by = 10))) %>%
  group_by(adr_bin) %>%
  summarise(mean_adr = mean(adr, na.rm=TRUE),
            cancel_rate = mean(is_canceled, na.rm=TRUE),
            n = n()) %>%
  filter(n > 30)

p5 <- ggplot(adr_bins, aes(x = mean_adr, y = cancel_rate)) +
  geom_line() + geom_point(aes(size = n)) +
  labs(title = "Tasa de cancelación por nivel de ADR (bins)", x = "ADR medio del bin", y = "Tasa de cancelación") +
  theme_minimal()
ggplotly(p5)
```

Explicación:

- Agrupamos ADR en bins y calculamos la tasa de cancelación por bin para ver si hay relación entre precio medio y cancelación.
    

## 5.5 Tabla interactiva: principales países y segmentos

```{r
top_countries <- df_clean %>%
  group_by(country) %>%
  summarise(n = n(), canceled = sum(is_canceled), cancel_rate = round(100*canceled/n,2)) %>%
  arrange(desc(n)) %>%
  slice(1:30)
DT::datatable(top_countries, 
              options = list(pageLength = 10, autoWidth = TRUE, 
                             columnDefs = list(list(width = '100px', targets = c(0)))),
              caption = "Top 30 países por número de reservas")
```

Explicación:

- Tabla interactiva que permite buscar y ordenar los países más frecuentes.
    

## 5.6 Duración media de estancia (por hotel)

```{r
stay_summary <- df_clean %>%
  group_by(hotel) %>%
  summarise(mean_nights = mean(total_nights, na.rm=TRUE),
            median_nights = median(total_nights, na.rm=TRUE),
            sd_nights = sd(total_nights, na.rm=TRUE),
            n = n())

stay_summary

p6 <- ggplot(df_clean %>% group_by(hotel, total_nights) %>% summarise(n = n()), aes(x = total_nights, y = n, fill = hotel)) +
  geom_col(position = "dodge") +
  labs(title = "Distribución de duración de estancia (nº noches) por hotel", x = "Total noches", y = "Número de reservas") +
  theme_minimal()
ggplotly(p6)
```

# 6 Historias sugeridas (Storytelling)

Propongo 3 posibles historias (cada una enlaza a una o varias visualizaciones anteriores):

1. **"¿Por qué se cancelan más reservas en el Resort en verano?"**
    
    - Muestra: tasa de cancelación por mes y hotel (sección 5.1).
        
    - Complemento: bins de ADR y lead_time para ver si altas anticipaciones o precios influyen.
        
2. **"Lead time largo y riesgo de cancelación"**
    
    - Muestra: violín de `lead_time` por cancelación (5.2) y análisis bivariado `lead_time` vs `adr` (extensión posible).
        
3. **"Clientes y precios: ¿quién paga más?"**
    
    - Muestra: cajas de ADR por `customer_type` (5.3) y tabla de países (5.5) para segmentar.
        

# 7 Recomendaciones y Buenas prácticas (para presentar)

- Exporta las figuras interactivas a HTML para presentarlas dinámicamente (o generar PNG para PDF si la entrega exige PDF).
    
- Añade anotaciones y llamadas (callouts) en las figuras clave para guiar al público.
    
- Evita saturar una sola diapositiva con demasiada información; usa una figura por idea.
    
- Cuando presentes tasas (p.ej. cancelación), acompáñalas de tamaños muestrales (`n`) para dar contexto.
    

# 8 Código adicional de apoyo (guardado de figuras e informes)

```{r
# Guardar una gráfica plotly como HTML (ejemplo)
library(htmlwidgets)
p_html <- ggplotly(p1)
htmlwidgets::saveWidget(p_html, file = "cancel_rate_by_month.html", selfcontained = TRUE)

# Guardar tabla como CSV con resumen agregado
write.csv(top_countries, file = "top_countries_summary.csv", row.names = FALSE)
```

# 9 Conclusiones

- El dataset permite múltiples historias: diferencias de cancelación entre hoteles, influencia del `lead_time` y del `adr` en la probabilidad de cancelación, y patrones estacionales.
    
- Las visualizaciones interactivas ayudan a descubrir patrones finos (picos por mes, outliers de ADR, países emisores).
    
- Recomendación final: basar la presentación en 2–3 visualizaciones interactivas clave y usar la tabla interactiva para responder preguntas “ad hoc” durante la exposición.
    

# 10 Apéndice — ejercicios propuestos (extensiones)

1. Construir una pequeña app Shiny que permita seleccionar un hotel, rango de fechas y ver gráficos filtrados (ideal para demo).
    
2. Añadir geolocalización de los países (mediante ISO2/ISO3) y un mapa interactivo (leaflet) que muestre volumen por país.
    
3. Entrenar un modelo simple (árbol o logistic regression) para predecir cancelación y comparar features importantes (lead_time, adr, market_segment).
    

```

---

Si quieres, puedo:
- Generar la versión Shiny mínima para filtrar por hotel/mes y mostrar las gráficas interactivas (te doy el `app.R` listo).
- Añadir el mapa `leaflet` con la localización de países (necesitaré un fichero con lat/lon por código país o permiso para buscarlo).
- Adaptar la salida para que el PDF incluya snapshots estáticos además del HTML interactivo.

Dime cuál de estas extensiones quieres y lo preparo directamente.
```