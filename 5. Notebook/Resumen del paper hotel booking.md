# Resumen Completo del Dataset de Reservas Hoteleras

## Visión General del Dataset

Este documento describe dos datasets con datos reales de demanda hotelera provenientes de dos establecimientos en Portugal:

- **H1 (Resort Hotel)**: Hotel resort en la región de Algarve con 40,060 observaciones
- **H2 (City Hotel)**: Hotel urbano en Lisboa con 79,330 observaciones

Ambos datasets comparten la misma estructura con **31 variables** y cubren reservas programadas para llegar entre el 1 de julio de 2015 y el 31 de agosto de 2017, incluyendo tanto reservas efectivas como canceladas.

## Propósito y Valor del Dataset

Los datasets fueron creados originalmente para desarrollar modelos de predicción de cancelaciones hoteleras, pero su utilidad se extiende a múltiples aplicaciones:

- **Investigación**: Análisis descriptivo, predicción de cancelaciones, segmentación de clientes, estudio de estacionalidad
- **Machine Learning**: Benchmarking de algoritmos de clasificación y segmentación
- **Educación**: Entrenamiento en estadística, minería de datos y aprendizaje automático
- **Revenue Management**: Investigación específica de la industria hotelera

## Metodología de Recolección

### Extracción de Datos

- Datos extraídos directamente de las bases de datos SQL del Property Management System (PMS)
- Uso de consultas TSQL en SQL Server Management Studio
- Información sensible de identificación de hotel y clientes fue eliminada para garantizar anonimato

### Prevención de Data Leakage

Para evitar la filtración de información futura en modelos predictivos, se aplicó un principio crítico: el timestamp de las variables independientes debe ser anterior al de la variable objetivo. Por ello, los valores fueron extraídos del registro de cambios de reservas (change log) con timestamp relativo al **día previo a la fecha de llegada**.

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
- **ADR (Average Daily Rate)**: tarifa promedio diaria calculada dividiendo el total de transacciones de alojamiento entre el número de noches

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

## Consideraciones Importantes

### Diferencias en Distribuciones

Las visualizaciones mediante "table plots" revelan que variables como Adults, Children, StaysInWeekendNights, StaysInWeekNights, Meal, Country y AssignedRoomType muestran distribuciones claramente diferentes entre reservas canceladas y no canceladas. Esto ocurre porque:

- Los clientes frecuentemente modifican atributos durante el check-in o estancia
- La nacionalidad correcta a menudo no se conoce hasta el check-in
- Estas diferencias deben considerarse al usar los datasets para modelado

### Valores NULL

No representan datos faltantes sino **"no aplicable"**. Por ejemplo, Agent = NULL significa que la reserva no provino de una agencia de viajes.

## Relevancia Científica

Este dataset llena un vacío importante en la investigación de Revenue Management, que tradicionalmente se ha centrado en la industria de aviación (formato PNR). La hospitalidad tiene particularidades específicas que requieren datos propios para investigación efectiva, haciendo estos datasets especialmente valiosos para la comunidad académica y profesional.