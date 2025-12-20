########################################
#### LIBRERIAS NECESARIAS           ####
import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import warnings
warnings.simplefilter(action='ignore', category=UserWarning)

import pandas as pd
########################################

def describe_df(data):
    """
    Proporciona un resumen completo del DataFrame con estadísticas descriptivas,
    información de valores nulos, únicos y categorías más frecuentes.

    Parámetros:
    -----------
    data : pd.DataFrame
        DataFrame de pandas a analizar.

    Retorna:
    --------
    pd.DataFrame
        DataFrame con el resumen detallado del DataFrame dado.
        
    Muestra:
    --------
    - Dimensiones del dataset en un cuadro inicial
    - Resumen por columna con estadísticas relevantes según el tipo de dato
    """
    
    # 1. MOSTRAR DIMENSIONES AL INICIO
    print("=" * 60)
    print(f"📊 DIMENSIONES DEL DATASET")
    print("=" * 60)
    print(f"   Filas:    {data.shape[0]:,}")
    print(f"   Columnas: {data.shape[1]:,}")
    print("=" * 60)
    print()
    
    total = len(data)
    
    # Base del resumen
    summary = pd.DataFrame({
        'Column': data.columns,
        'Type': data.dtypes.astype(str),
        'Non-null': data.count().values,
        '% Null': ((data.isnull().sum() / total) * 100).round(2).values,
        'Unique': data.nunique().values
    })

    # COLUMNAS NUMÉRICAS: Estadísticas descriptivas
    numeric_cols = data.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        stats = data[numeric_cols].describe().T
        stats = stats.rename(columns={'50%': 'Median'})[
            ['mean', 'Median', 'std', 'min', '25%', '75%', 'max']
        ]
        stats.columns = ['Mean', 'Median', 'Std', 'Min', 'Q1', 'Q3', 'Max']
        stats = stats.round(2)
        stats.reset_index(inplace=True)
        stats.rename(columns={'index': 'Column'}, inplace=True)
        summary = pd.merge(summary, stats, on='Column', how='left')

    # COLUMNAS DATETIME: Rango de fechas
    datetime_cols = data.select_dtypes(include=['datetime', 'datetime64[ns]', 'datetime64']).columns
    if len(datetime_cols) > 0:
        date_info = pd.DataFrame({
            'Column': datetime_cols,
            'Min Date': data[datetime_cols].min().values,
            'Max Date': data[datetime_cols].max().values
        })
        summary = pd.merge(summary, date_info, on='Column', how='left')

    # 3. TOP COUNT: Top 3 categorías para columnas categóricas y datetime
    top_counts = []
    for col in data.columns:
        # Aplicar a categóricas (con menos de 50 valores únicos) y datetime
        if col in datetime_cols or (data[col].dtype == 'object' or data[col].nunique() < 50):
            value_counts = data[col].value_counts().head(3)
            if len(value_counts) > 0:
                top_str = "; ".join([f"{val} ({count})" for val, count in value_counts.items()])
                top_counts.append({'Column': col, 'TopCount': top_str})
            else:
                top_counts.append({'Column': col, 'TopCount': ''})
        else:
            top_counts.append({'Column': col, 'TopCount': ''})
    
    top_counts_df = pd.DataFrame(top_counts)
    summary = pd.merge(summary, top_counts_df, on='Column', how='left')

    # Ordenar columnas de forma lógica
    base_cols = ['Column', 'Type', 'Non-null', '% Null', 'Unique']
    numeric_stat_cols = ['Mean', 'Median', 'Std', 'Min', 'Q1', 'Q3', 'Max']
    datetime_cols_list = ['Min Date', 'Max Date']
    other_cols = ['TopCount']
    
    # Construir orden final solo con columnas existentes
    final_order = base_cols.copy()
    final_order += [c for c in numeric_stat_cols if c in summary.columns]
    final_order += [c for c in datetime_cols_list if c in summary.columns]
    final_order += [c for c in other_cols if c in summary.columns]
    
    summary = summary[final_order]
    
    return summary

def detect_duplicates(df):
    """
    Detecta duplicados en un DataFrame y devuelve un nuevo DataFrame con los duplicados.

    :param df: DataFrame de pandas.
    :return: DataFrame con los duplicados detectados.
    """
    try:
        return df[df.duplicated(keep=False)]
    except Exception as e:
        print("Error detectando duplicados:", e)
        return None

def unique_df(df):
    """
    Imprime un resumen de las categorías únicas para las variables categóricas de un DataFrame.

    :param df: DataFrame de pandas.
    """
    categorical_columns = df.select_dtypes(include=['category', 'object']).columns

    if len(categorical_columns) == 0:
        print("No se encontraron columnas categóricas u objeto en el DataFrame.")
        return

    for column in categorical_columns:
        print(f"Resumen para la columna '{column}':\n{df[column].unique()}\n")

