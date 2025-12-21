
# Resumen

Este informe presenta un análisis exhaustivo del dataset de reservas hoteleras de dos hoteles en Portugal (City Hotel y Resort Hotel), abarcando el período 2015-2017 con 119,390 observaciones [HotelBooking Article](Visualizacion_de_Datos_PEC-3/2. Enunciado/hotel_bookings_paper.pdf). El estudio aplica técnicas de analítica visual para explorar **patrones de cancelación**, **comportamiento de reservas**, **estacionalidad y características de los huéspedes**. Se identifican factores clave que influyen en las cancelaciones, diferencias significativas entre tipos de hotel, y tendencias temporales en la demanda. El análisis integra visualizaciones interactivas que permiten descubrir *insights* relevantes para la gestión hotelera, como la relación entre *lead time* y cancelaciones, el impacto del tipo de depósito, y las preferencias según origen geográfico. Los resultados proporcionan una base sólida para la construcción de una narrativa de datos orientada a la toma de decisiones estratégicas en el sector hotelero.

---
# 1. Introducción y Contexto

## 1.1 Descripción del Dataset

El dataset **hotel_bookings.csv** contiene información detallada (119,390 observaciones y 32 variables) sobre reservas realizadas en dos hoteles portugueses: un City Hotel ubicado en Lisboa y un Resort Hotel en el Algarve en el período de 2015 a 2017.

## 1.2. Variables del Dataset


## Estructura de Variables (32 variables totales)

### Variables Temporales

- **Fechas de llegada**: año, mes, número de semana, día del mes
- **Lead Time**: días transcurridos entre la entrada de la reserva en el sistema y la llegada
- **Días en lista de espera**: tiempo antes de confirmación al cliente
- **Fecha de estado de reserva**: fecha del último cambio de estado

### Variables de Estancia

- **Noches en fin de semana**: sábados y domingos
- **Noches entre semana**: lunes a viernes
- **Composición de huéspedes**: adultos, niños, bebés
- **ADR (*Average Daily Rate*)**: tarifa promedio diaria calculada dividiendo el total de transacciones de alojamiento entre el número de noches

### Variables de Reserva

- **Tipo de habitación reservada vs. asignada**: puede diferir por razones operativas (overbooking) o solicitudes del cliente
- **Tipo de comida**: Sin paquete (SC/Undefined), solo desayuno (BB), media pensión (HB), pensión completa (FB)
- **Cambios en la reserva**: número de modificaciones desde la entrada en el sistema hasta check-in o cancelación
- **Solicitudes especiales**: número total de peticiones específicas (cama doble, piso alto, etc.)

### Variables de Cliente

- **País de origen**: formato ISO 3155-3:2013
- **Tipo de cliente**: Contrato, Grupo, Transient (individual), Transient-party (asociado a otras reservas individuales)
- **Huésped repetido**: indica si el perfil del cliente existía previamente
- **Historial**: reservas previas no canceladas y cancelaciones anteriores

### Variables de Distribución

- **Canal de distribución**: TA/TO (agencias/operadores), directo, corporativo, GDS, indefinido
- **Segmento de mercado**: Online, Offline, Directo, Grupos, Corporativo, Complementario, Aviation
- **Agente de viajes**: ID anónimo (NULL = sin agente)
- **Empresa**: ID de entidad responsable del pago (NULL = no aplica)

### Variables de Pago

- **Tipo de depósito**:
    - No Deposit: sin depósito
    - Non Refund: depósito igual o superior al costo total
    - Refundable: depósito menor al costo total
- **Plazas de parking requeridas**

### Variable Objetivo

- **is_canceled**: indica si la reserva fue cancelada (1) o no (0)
- **Estado de reserva**: Canceled, Check-Out, No-Show (no se presentó sin avisar)

## Estadísticas Principales

### Resort Hotel (H1)

- **Tasa de cancelación**: 27.8% (11,122 de 40,060)
- **ADR medio**: €94.95 (rango: -€6.38 a €508)
- **Lead time promedio**: 93 días
- **Estancia promedio**: 4.3 noches totales
- **Países principales**: Portugal (44%), Reino Unido (17%), España (10%)
- **Tipo de comida predominante**: BB (75%)

### City Hotel (H2)

- **Tasa de cancelación**: 41.7% (33,102 de 79,330)
- **ADR medio**: €105.30 (rango: €0 a €5,400)
- **Lead time promedio**: 110 días
- **Estancia promedio**: 3 noches totales
- **Países principales**: Portugal (39%), Francia (11%), Alemania (8%)
- **Tipo de comida predominante**: BB (79%)

## 1.3. Objetivos:

1. Limpiar y preparar los datos.
2. Responder preguntas de interés mediante visualización.
3. Construir gráficos interactivos que sirvan para *storytelling* (cuentas, comparaciones y patrones).
4. Proveer materiales para la presentación: imágenes exportables y tablas interactivas.

---
# 2. Limpieza y preparación de datos

## 2.1. Detección de *Missing values*
## 2.2. Detección de *Outliers*

## 2.3. Creación de Variables Derivadas

---
# 3. Análisis Exploratorio de Datos (EDA)

## 3.1. Análisis de Cancelaciones
## 3.1.1. Factores que Influyen en las Cancelaciones

*  Tasa de Cancelacion según *Lead Time*
* Cancelacion según Tipo de Depósito

## 3.2. Análisis Temporal

* Evolución Temporal de Reservas de hotel
* Reservas por Temporada y Hotel

## 3.3. Análisis de Ingresos (ADR)

* Distribución de ADR por Hotel
* ADR Promedio por Mes

## 3.4. Análisis Geográfico

* Top 15 Paises por Numero de Resrvas

## 3.5. Análisis de Segmentos de Mercado

* Distribución de Reservas Por Segmentos de Mercado

---
# 4. Insights Clave y Hallazgos

## 4.1. Principales Descubrimientos

* **Métricas Clave del Dataset:**

|Métrica|Valor|
|---|---|
|Total de Reservas|119,390|
|Tasa de Cancelación (%)|37.04|
|Lead Time Promedio (días)|104|
|ADR Promedio (€)|101.83|
|País Más Común|PRT|
|Mes Pico|August|

## 4.2 Patrones Identificados

**Cancelaciones:**

- Las reservas con lead time superior a 6 meses presentan las tasas de cancelación más altas
- Los depósitos no reembolsables tienen tasas de cancelación significativamente menores
- El City Hotel tiene mayor tasa de cancelación que el Resort Hotel

**Estacionalidad:**

- La demanda presenta picos claros en verano (julio-septiembre)
- El ADR promedio también aumenta durante los meses de verano
- El Resort Hotel muestra mayor estacionalidad que el City Hotel

**Ingresos:**

- Existe gran variabilidad en el ADR, con outliers significativos
- Los meses de verano y temporadas altas presentan ADR más elevados

**Geográfico:**
- Portugal se diferencia significativamente mas alto que el resto de países en el numero de reservas, y tasa de cancelación.
- No parece haber una relación directa entre la tasa de cancelación y el número de reservas.

**Segmentos de Mercado:**
- El segmento “Online TA” genera el mayor volumen de reservas

---
# 5. Conclusiones y Recomendaciones

## 5.1 Conclusiones

El análisis del dataset de reservas hoteleras revela patrones complejos en el comportamiento de los clientes y oportunidades claras para optimizar la gestión hotelera:

1. **Gestión de Cancelaciones**: Las cancelaciones representan un desafío significativo, especialmente para reservas con lead times prolongados. La implementación de políticas de depósito podría mitigar este riesgo.
    
2. **Optimización de Precios**: La estacionalidad marcada sugiere oportunidades para implementar estrategias de revenue management más sofisticadas.
    
3. **Segmentación de Mercado**: La diversidad de segmentos y orígenes geográficos requiere estrategias de marketing diferenciadas.

## 5.2 Recomendaciones

- Implementar modelos predictivos para identificar reservas con alto riesgo de cancelación
- Desarrollar políticas de pricing dinámico basadas en patrones estacionales
- Focalizar esfuerzos de marketing en países con alta tasa de conversión
- Optimizar la gestión de inventario durante temporadas pico

---
# 6. Referencias y Recursos

- Dataset original: Hotel Booking Demand Datasets (Antonio, Almeida & Nunes, 2019)
- Análisis realizado con R versión R version 4.5.1 (2025-06-13 ucrt)
- Paquetes utilizados: tidyverse, plotly, ggplot2, y otros