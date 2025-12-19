################################################################################
#                LABORATORIO DE ANÁLISIS - HOTEL BOOKINGS DATASET              #
#                        Análisis Exploratorio Completo                        #
################################################################################

# Autor: Julio Úbeda Quesada
# Fecha: 2024
# Descripción: Script de laboratorio para análisis exploratorio detallado del
#              dataset de reservas hoteleras

################################################################################
# 0. CONFIGURACIÓN INICIAL
################################################################################

# Limpiar entorno
rm(list = ls())
cat("\014")  # Limpiar consola

# Establecer directorio de trabajo
home_path <- "C:/Users/jubeda2/Desktop/Visualizacion_de_Datos_PEC-3"
data_loc <- paste0(home_path, "/1. Datos/")
file_path_csv <- paste0(data_loc, "hotel_bookings.csv")

# Paquetes necesarios
packages <- c(
  "tidyverse",      # Manipulación y visualización
  "ggplot2",        # Gráficos avanzados
  "corrplot",       # Matrices de correlación
  "GGally",         # Pares de gráficos
  "psych",          # Estadísticas descriptivas
  "gridExtra",      # Múltiples gráficos
  "reshape2",       # Reestructuración de datos
  "scales",         # Escalas para gráficos
  "RColorBrewer",   # Paletas de colores
  "moments",        # Medidas de forma (asimetría, curtosis)
  "car",            # Pruebas estadísticas
  #"ggmosaic",       # Gráficos de mosaico
  "vcd"             # Visualización de datos categóricos
)

# Instalar paquetes faltantes
nuevos_paquetes <- packages[!(packages %in% installed.packages()[,"Package"])]
if(length(nuevos_paquetes)) install.packages(nuevos_paquetes)

# Cargar paquetes
lapply(packages, library, character.only = TRUE)

remotes::install_github("haleyjeppson/ggmosaic")
library(ggmosaic)

# Configurar opciones
options(scipen = 999)  # Evitar notación científica
theme_set(theme_minimal())  # Tema por defecto para ggplot2

################################################################################
# 1. CARGA Y PREPARACIÓN DE DATOS
################################################################################

# Cargar datos
df <- read.csv(file_path_csv, stringsAsFactors = TRUE)

# Información básica
cat("Dimensiones del dataset:\n")
cat("  - Filas:", nrow(df), "\n")
cat("  - Columnas:", ncol(df), "\n\n")

cat("Estructura del dataset:\n")
str(df)

# Crear backup original
df_original <- df

################################################################################
# 2. ANÁLISIS DESCRIPTIVO GENERAL
################################################################################

# 2.1 Resumen estadístico completo

summary(df)

# 2.2 Tipos de variables
tipos_var <- data.frame(
  Variable = names(df),
  Tipo = sapply(df, class),
  Valores_Unicos = sapply(df, function(x) length(unique(x))),
  Valores_NA = sapply(df, function(x) sum(is.na(x))),
  Porcentaje_NA = round(sapply(df, function(x) sum(is.na(x))/length(x)*100), 2)
)
rownames(tipos_var) <- NULL

print(tipos_var)

# 2.3 Identificar variables por tipo
vars_numericas <- names(df)[sapply(df, is.numeric)]
vars_categoricas <- names(df)[sapply(df, is.factor)]
vars_entero <- names(df)[sapply(df, is.integer)]

cat("\n2.3 CLASIFICACIÓN DE VARIABLES:\n")
cat("--------------------------------\n")
cat("Variables numéricas (", length(vars_numericas), "):\n  ", 
    paste(vars_numericas, collapse = ", "), "\n\n")
cat("Variables categóricas (", length(vars_categoricas), "):\n  ", 
    paste(vars_categoricas, collapse = ", "), "\n\n")
cat("Variables enteras (", length(vars_entero), "):\n  ", 
    paste(vars_entero, collapse = ", "), "\n\n")

################################################################################
# 3. ANÁLISIS DE VARIABLES CATEGÓRICAS
################################################################################

cat("\n========================================\n")
cat("3. ANÁLISIS DE VARIABLES CATEGÓRICAS\n")
cat("========================================\n\n")

# 3.1 Función para analizar variable categórica
analizar_categorica <- function(data, var_name, top_n = 10) {
  cat("\n--- Análisis de:", var_name, "---\n")
  
  # Tabla de frecuencias
  freq_table <- as.data.frame(table(data[[var_name]]))
  names(freq_table) <- c(var_name, "Frecuencia")
  freq_table$Porcentaje <- round(freq_table$Frecuencia / sum(freq_table$Frecuencia) * 100, 2)
  freq_table$Porcentaje_Acum <- cumsum(freq_table$Porcentaje)
  freq_table <- freq_table[order(-freq_table$Frecuencia), ]
  
  cat("\nNúmero de categorías:", nrow(freq_table), "\n")
  cat("Categoría más frecuente:", as.character(freq_table[1, var_name]), 
      "(", freq_table[1, "Frecuencia"], "obs,", freq_table[1, "Porcentaje"], "%)\n")
  
  # Mostrar top N categorías
  cat("\nTop", min(top_n, nrow(freq_table)), "categorías:\n")
  print(head(freq_table, top_n))
  
  return(freq_table)
}

# 3.2 Analizar variables categóricas principales
cat("\n3.1 HOTEL:\n")
freq_hotel <- analizar_categorica(df, "hotel")

cat("\n3.2 MEAL (Tipo de comida):\n")
freq_meal <- analizar_categorica(df, "meal")

cat("\n3.3 MARKET SEGMENT:\n")
freq_market <- analizar_categorica(df, "market_segment")

cat("\n3.4 DISTRIBUTION CHANNEL:\n")
freq_distribution <- analizar_categorica(df, "distribution_channel")

cat("\n3.5 CUSTOMER TYPE:\n")
freq_customer <- analizar_categorica(df, "customer_type")

cat("\n3.6 DEPOSIT TYPE:\n")
freq_deposit <- analizar_categorica(df, "deposit_type")

cat("\n3.7 RESERVATION STATUS:\n")
freq_status <- analizar_categorica(df, "reservation_status")

cat("\n3.8 COUNTRY (Top 20):\n")
freq_country <- analizar_categorica(df, "country", top_n = 20)

# 3.3 Gráficos para variables categóricas principales
cat("\n3.9 Generando gráficos de variables categóricas...\n")

# Hotel
p1 <- ggplot(df, aes(x = hotel, fill = hotel)) +
  geom_bar() +
  geom_text(stat = "count", aes(label = after_stat(count)), vjust = -0.5) +
  scale_fill_brewer(palette = "Set2") +
  labs(title = "Distribución por Tipo de Hotel",
       x = "Hotel", y = "Frecuencia") +
  theme(legend.position = "none")

# Cancelaciones
p2 <- ggplot(df, aes(x = factor(is_canceled), fill = factor(is_canceled))) +
  geom_bar() +
  geom_text(stat = "count", aes(label = after_stat(count)), vjust = -0.5) +
  scale_fill_manual(values = c("#4ECDC4", "#FF6B6B"),
                    labels = c("No cancelada", "Cancelada")) +
  labs(title = "Distribución de Cancelaciones",
       x = "Cancelada", y = "Frecuencia", fill = "Estado") +
  theme(legend.position = "bottom")

# Market segment
p3 <- ggplot(df, aes(x = market_segment, fill = market_segment)) +
  geom_bar() +
  coord_flip() +
  geom_text(stat = "count", aes(label = after_stat(count)), hjust = -0.1) +
  scale_fill_brewer(palette = "Set3") +
  labs(title = "Distribución por Segmento de Mercado",
       x = "Segmento", y = "Frecuencia") +
  theme(legend.position = "none")

# Deposit type
p4 <- ggplot(df, aes(x = deposit_type, fill = deposit_type)) +
  geom_bar() +
  geom_text(stat = "count", aes(label = after_stat(count)), vjust = -0.5) +
  scale_fill_brewer(palette = "Pastel1") +
  labs(title = "Distribución por Tipo de Depósito",
       x = "Tipo de Depósito", y = "Frecuencia") +
  theme(legend.position = "none")

# Combinar gráficos
grid.arrange(p1, p2, p3, p4, ncol = 2)

# 3.4 Tablas de contingencia (relaciones entre categóricas)
cat("\n3.10 TABLAS DE CONTINGENCIA:\n")
cat("-----------------------------\n")

# Hotel vs Cancelación
cat("\nHotel vs Cancelación:\n")
tabla_hotel_cancel <- table(df$hotel, df$is_canceled)
print(addmargins(tabla_hotel_cancel))
cat("\nProporción:\n")
print(prop.table(tabla_hotel_cancel, 1))

# Chi-cuadrado
test_chi <- chisq.test(tabla_hotel_cancel)
cat("\nTest Chi-cuadrado:\n")
cat("  X-squared =", test_chi$statistic, "\n")
cat("  p-value =", test_chi$p.value, "\n")
if(test_chi$p.value < 0.05) {
  cat("  Resultado: Existe asociación significativa\n")
} else {
  cat("  Resultado: No existe asociación significativa\n")
}

# Deposit type vs Cancelación
cat("\n\nDeposit Type vs Cancelación:\n")
tabla_deposit_cancel <- table(df$deposit_type, df$is_canceled)
print(addmargins(tabla_deposit_cancel))
cat("\nProporción:\n")
print(prop.table(tabla_deposit_cancel, 1))

# 3.5 Gráfico de mosaico (relación categóricas)
cat("\n3.11 Generando gráfico de mosaico...\n")

ggplot(data = df) +
  geom_mosaic(aes(x = product(hotel, is_canceled), fill = hotel)) +
  labs(title = "Mosaico: Hotel vs Cancelación",
       x = "Cancelación", y = "Hotel") +
  scale_fill_brewer(palette = "Set2")

################################################################################
# 4. ANÁLISIS DE VARIABLES NUMÉRICAS
################################################################################

cat("\n========================================\n")
cat("4. ANÁLISIS DE VARIABLES NUMÉRICAS\n")
cat("========================================\n\n")

# 4.1 Seleccionar variables numéricas clave para análisis
vars_num_analisis <- c("lead_time", "stays_in_weekend_nights", "stays_in_week_nights",
                       "adults", "children", "babies", "adr", 
                       "days_in_waiting_list", "booking_changes",
                       "previous_cancellations", "previous_bookings_not_canceled",
                       "required_car_parking_spaces", "total_of_special_requests")

df_numeric <- df[, vars_num_analisis]

# 4.2 Estadísticas descriptivas detalladas
cat("4.1 ESTADÍSTICAS DESCRIPTIVAS DETALLADAS:\n")
cat("------------------------------------------\n")

desc_stats <- describe(df_numeric)
print(round(desc_stats, 2))

# 4.3 Medidas adicionales por variable
cat("\n4.2 MEDIDAS ADICIONALES POR VARIABLE:\n")
cat("--------------------------------------\n")

for(var in vars_num_analisis) {
  cat("\n>>>", var, "<<<\n")
  datos <- df_numeric[[var]]
  
  cat("  Media:", round(mean(datos, na.rm = TRUE), 2), "\n")
  cat("  Mediana:", round(median(datos, na.rm = TRUE), 2), "\n")
  cat("  Moda:", names(sort(table(datos), decreasing = TRUE))[1], "\n")
  cat("  Desv. Estándar:", round(sd(datos, na.rm = TRUE), 2), "\n")
  cat("  Varianza:", round(var(datos, na.rm = TRUE), 2), "\n")
  cat("  Rango:", paste(min(datos, na.rm = TRUE), "-", max(datos, na.rm = TRUE)), "\n")
  cat("  IQR:", round(IQR(datos, na.rm = TRUE), 2), "\n")
  cat("  Coef. Variación:", round(sd(datos, na.rm = TRUE)/mean(datos, na.rm = TRUE)*100, 2), "%\n")
  cat("  Asimetría:", round(skewness(datos, na.rm = TRUE), 2), "\n")
  cat("  Curtosis:", round(kurtosis(datos, na.rm = TRUE), 2), "\n")
  
  # Percentiles
  percs <- quantile(datos, probs = c(0.01, 0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99), na.rm = TRUE)
  cat("  Percentiles:\n")
  print(round(percs, 2))
}

# 4.4 Detección de outliers
cat("\n4.3 DETECCIÓN DE OUTLIERS (Método IQR):\n")
cat("----------------------------------------\n")

outliers_summary <- data.frame()

for(var in vars_num_analisis) {
  datos <- df_numeric[[var]]
  Q1 <- quantile(datos, 0.25, na.rm = TRUE)
  Q3 <- quantile(datos, 0.75, na.rm = TRUE)
  IQR_val <- Q3 - Q1
  lower_bound <- Q1 - 1.5 * IQR_val
  upper_bound <- Q3 + 1.5 * IQR_val
  
  outliers <- sum(datos < lower_bound | datos > upper_bound, na.rm = TRUE)
  pct_outliers <- round(outliers / length(datos) * 100, 2)
  
  outliers_summary <- rbind(outliers_summary, data.frame(
    Variable = var,
    Q1 = Q1,
    Q3 = Q3,
    IQR = IQR_val,
    Lower_Bound = lower_bound,
    Upper_Bound = upper_bound,
    N_Outliers = outliers,
    Pct_Outliers = pct_outliers
  ))
}

print(outliers_summary)

# 4.5 Histogramas y densidades
cat("\n4.4 Generando histogramas y curvas de densidad...\n")

# Función para crear histograma con densidad
plot_hist_density <- function(data, var_name) {
  ggplot(data, aes(x = .data[[var_name]])) +
    geom_histogram(aes(y = after_stat(density)), bins = 30, 
                   fill = "#69b3a2", color = "black", alpha = 0.7) +
    geom_density(color = "#FF6B6B", size = 1.2) +
    labs(title = paste("Distribución de", var_name),
         x = var_name, y = "Densidad") +
    theme_minimal()
}

# Crear gráficos para variables clave
plot_list <- list()
vars_plot <- c("lead_time", "adr", "stays_in_week_nights", "adults")

for(i in seq_along(vars_plot)) {
  plot_list[[i]] <- plot_hist_density(df, vars_plot[i])
}

do.call(grid.arrange, c(plot_list, ncol = 2))

# 4.6 Boxplots para identificar outliers visualmente
cat("\n4.5 Generando boxplots...\n")

# Preparar datos en formato largo
df_long <- df_numeric %>%
  select(lead_time, adr, stays_in_week_nights, adults, 
         booking_changes, total_of_special_requests) %>%
  pivot_longer(everything(), names_to = "Variable", values_to = "Valor")

ggplot(df_long, aes(x = Variable, y = Valor, fill = Variable)) +
  geom_boxplot() +
  scale_fill_brewer(palette = "Set3") +
  labs(title = "Boxplots de Variables Numéricas Principales",
       x = "Variable", y = "Valor") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1),
        legend.position = "none") +
  facet_wrap(~ Variable, scales = "free")

# 4.7 Análisis de ADR (Variable clave)
cat("\n4.6 ANÁLISIS ESPECIAL DE ADR:\n")
cat("------------------------------\n")

# Filtrar ADR válidos (> 0 y < outliers extremos)
adr_valido <- df$adr[df$adr > 0 & df$adr < 500]

cat("ADR válido (0 < ADR < 500):\n")
cat("  N observaciones:", length(adr_valido), "\n")
cat("  Media:", round(mean(adr_valido), 2), "€\n")
cat("  Mediana:", round(median(adr_valido), 2), "€\n")
cat("  Desv. Estándar:", round(sd(adr_valido), 2), "€\n")

# Histograma de ADR
ggplot(df %>% filter(adr > 0 & adr < 500), aes(x = adr)) +
  geom_histogram(aes(y = after_stat(density)), bins = 50, 
                 fill = "#69b3a2", alpha = 0.7) +
  geom_density(color = "#FF6B6B", size = 1.2) +
  geom_vline(xintercept = mean(adr_valido), linetype = "dashed", 
             color = "blue", size = 1) +
  geom_vline(xintercept = median(adr_valido), linetype = "dashed", 
             color = "red", size = 1) +
  labs(title = "Distribución de ADR (Average Daily Rate)",
       subtitle = "Línea azul: Media | Línea roja: Mediana",
       x = "ADR (€)", y = "Densidad") +
  theme_minimal()

# ADR por tipo de hotel
cat("\nADR por tipo de hotel:\n")
adr_hotel <- df %>%
  filter(adr > 0 & adr < 500) %>%
  group_by(hotel) %>%
  summarise(
    N = n(),
    Media = mean(adr),
    Mediana = median(adr),
    SD = sd(adr),
    Min = min(adr),
    Max = max(adr)
  )
print(adr_hotel)

# Test de diferencias
t_test_adr <- t.test(adr ~ hotel, data = df %>% filter(adr > 0 & adr < 500))
cat("\nTest t de Student (ADR entre hoteles):\n")
cat("  t =", t_test_adr$statistic, "\n")
cat("  p-value =", t_test_adr$p.value, "\n")
if(t_test_adr$p.value < 0.05) {
  cat("  Resultado: Existen diferencias significativas\n")
} else {
  cat("  Resultado: No existen diferencias significativas\n")
}

################################################################################
# 5. CORRELACIÓN ENTRE VARIABLES NUMÉRICAS
################################################################################

cat("\n========================================\n")
cat("5. CORRELACIÓN ENTRE VARIABLES NUMÉRICAS\n")
cat("========================================\n\n")

# 5.1 Matriz de correlación
cat("5.1 MATRIZ DE CORRELACIÓN:\n")
cat("--------------------------\n")

# Calcular matriz de correlación
cor_matrix <- cor(df_numeric, use = "complete.obs")
print(round(cor_matrix, 3))

# 5.2 Visualización de correlaciones
cat("\n5.2 Generando visualizaciones de correlación...\n")

# Método 1: corrplot clásico
corrplot(cor_matrix, method = "color", type = "upper", 
         tl.col = "black", tl.srt = 45,
         addCoef.col = "black", number.cex = 0.7,
         title = "Matriz de Correlación - Variables Numéricas",
         mar = c(0,0,2,0))

# Método 2: corrplot con círculos
corrplot(cor_matrix, method = "circle", type = "upper",
         tl.col = "black", tl.srt = 45,
         title = "Matriz de Correlación - Círculos",
         mar = c(0,0,2,0))

# Método 3: Heatmap con ggplot
cor_melted <- melt(cor_matrix)

ggplot(cor_melted, aes(x = Var1, y = Var2, fill = value)) +
  geom_tile() +
  scale_fill_gradient2(low = "#FF6B6B", mid = "white", high = "#4ECDC4",
                       midpoint = 0, limit = c(-1,1), 
                       name = "Correlación") +
  geom_text(aes(label = round(value, 2)), size = 2.5) +
  labs(title = "Heatmap de Correlaciones",
       x = "", y = "") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# 5.3 Identificar correlaciones fuertes
cat("\n5.3 CORRELACIONES FUERTES (|r| > 0.5):\n")
cat("---------------------------------------\n")

# Extraer correlaciones fuertes
cor_df <- as.data.frame(as.table(cor_matrix))
names(cor_df) <- c("Variable1", "Variable2", "Correlacion")
cor_df <- cor_df %>%
  filter(Variable1 != Variable2) %>%
  filter(abs(Correlacion) > 0.5) %>%
  arrange(desc(abs(Correlacion)))

# Eliminar duplicados (A-B = B-A)
cor_df <- cor_df[!duplicated(t(apply(cor_df[,1:2], 1, sort))),]

print(cor_df)

# 5.4 Scatterplot matrix (para variables clave)
cat("\n5.4 Generando matriz de dispersión...\n")

vars_scatter <- c("lead_time", "adr", "stays_in_week_nights", 
                  "adults", "total_of_special_requests")

ggpairs(df[, vars_scatter],
        title = "Matriz de Dispersión - Variables Clave",
        upper = list(continuous = wrap("cor", size = 3)),
        lower = list(continuous = wrap("points", alpha = 0.3, size = 0.5)))

# 5.5 Correlaciones con la variable objetivo (is_canceled)
cat("\n5.5 CORRELACIONES CON CANCELACIÓN:\n")
cat("-----------------------------------\n")

# Calcular correlaciones con is_canceled
cor_canceled <- data.frame(
  Variable = vars_num_analisis,
  Correlacion = sapply(vars_num_analisis, function(var) {
    cor(df[[var]], df$is_canceled, use = "complete.obs")
  })
) %>%
  arrange(desc(abs(Correlacion)))

print(cor_canceled)

# Visualizar
ggplot(cor_canceled, aes(x = reorder(Variable, abs(Correlacion)), 
                         y = Correlacion, fill = Correlacion > 0)) +
  geom_bar(stat = "identity") +
  coord_flip() +
  scale_fill_manual(values = c("#4ECDC4", "#FF6B6B"),
                    labels = c("Negativa", "Positiva")) +
  labs(title = "Correlación de Variables Numéricas con Cancelación",
       x = "Variable", y = "Correlación", fill = "Tipo") +
  theme_minimal()

# 5.6 Análisis de colinealidad (VIF)
cat("\n5.6 ANÁLISIS DE COLINEALIDAD (VIF):\n")
cat("------------------------------------\n")

# Preparar modelo lineal simple para calcular VIF
vars_vif <- c("lead_time", "stays_in_week_nights", "adults", 
              "booking_changes", "previous_cancellations", 
              "days_in_waiting_list")

formula_vif <- as.formula(paste("is_canceled ~", paste(vars_vif, collapse = " + ")))
model_vif <- lm(formula_vif, data = df)

vif_values <- vif(model_vif)
vif_df <- data.frame(
  Variable = names(vif_values),
  VIF = vif_values
) %>%
  arrange(desc(VIF))

cat("\nVIF (Variance Inflation Factor):\n")
cat("VIF > 10: Colinealidad alta\n")
cat("VIF > 5: Colinealidad moderada\n\n")
print(vif_df)

################################################################################
# 6. ANÁLISIS BIVARIADO
################################################################################

cat("\n========================================\n")
cat("6. ANÁLISIS BIVARIADO\n")
cat("========================================\n\n")

# 6.1 ADR vs Lead Time
cat("6.1 Generando gráfico ADR vs Lead Time...\n")

ggplot(df %>% filter(adr > 0 & adr < 500 & lead_time < 500), 
       aes(x = lead_time, y = adr)) +
  geom_point(alpha = 0.2, color = "#69b3a2") +
  geom_smooth(method = "loess", color = "#FF6B6B", se = TRUE) +
  labs(title = "Relación entre Lead Time y ADR",
       x = "Lead Time (días)", y = "ADR (€)") +
  theme_minimal()

# 6.2 ADR por hotel y cancelación
cat("6.2 Generando gráfico ADR por hotel y cancelación...\n")

ggplot(df %>% filter(adr > 0 & adr < 500), 
       aes(x = hotel, y = adr, fill = factor(is_canceled))) +
  geom_boxplot() +
  scale_fill_manual(values = c("#4ECDC4", "#FF6B6B"),
                    labels = c("No cancelada", "Cancelada")) +
  labs(title = "Distribución de ADR por Hotel y Estado de Cancelación",
       x = "Hotel", y = "ADR (€)", fill = "Estado") +
  theme_minimal()

# 6.3 Lead time vs Cancelación
cat("6.3 Generando gráfico Lead Time vs Cancelación...\n")

ggplot(df %>% filter(lead_time < 500), 
       aes(x = factor(is_canceled), y = lead_time, fill = factor(is_canceled))) +
  geom_violin(alpha = 0.7) +
  geom_boxplot(width = 0.2, alpha = 0.5) +
  scale_fill_manual(values = c("#4ECDC4", "#FF6B6B"),
                    labels = c("No cancelada", "Cancelada")) +
  labs(title = "Distribución de Lead Time según Estado de Cancelación",
       x = "Cancelada", y = "Lead Time (días)", fill = "Estado") +
  theme_minimal()

