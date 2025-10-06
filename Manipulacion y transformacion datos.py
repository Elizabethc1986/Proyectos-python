
# 1.Carga los datos y crea un DataFrame con cada uno de ellos.
import pandas as pd
import pickle

ruta_archivo = r'C:\Users\eliza\OneDrive\Escritorio\PYTHON\desafio5\incidents.pkl'


with open(ruta_archivo, 'rb') as archivo:
    datos = pickle.load(archivo)

# Si los datos son compatibles con DataFrame
df1 = pd.DataFrame(datos)

# Muestra las primeras filas del DataFrame df2 Officers
print(df1.head())


ruta_archivo = r'C:\Users\eliza\OneDrive\Escritorio\PYTHON\desafio5\officers.pkl'

with open(ruta_archivo, 'rb') as archivo:
    datos = pickle.load(archivo)

df2 = pd.DataFrame(datos)

# Muestra las primeras filas del DataFrame
print(df2.head())
# Muestra las primeras filas del DataFrame
print(df2.head())


ruta_archivo = r'C:\Users\eliza\OneDrive\Escritorio\PYTHON\desafio5\subjects.pkl'

with open(ruta_archivo, 'rb') as archivo:
    datos = pickle.load(archivo)

# Si los datos son compatibles con DataFrame
df3 = pd.DataFrame(datos)

# Muestra las primeras filas del DataFrame
print(df3.head())


#2.Genera una tabla que contenga la unión de las 3 tablas. hint: utiliza sufijos para para las
#columnas que se llaman igual usando el parámetro suffixes de pd.merge()

# Unir df1 y df2 usando la columna en común, por ejemplo 'case_number'
merge_1_2 = pd.merge(df1, df2,how ='outer', on='case_number', suffixes=('_df1', '_df2'))

# Luego unir el resultado con df3
tabla_final = pd.merge(merge_1_2, df3,how ='outer', on='case_number', suffixes=('', '_df3'))

# Mostrar la tabla final
print(tabla_final.head())

print("Columnas de df1:", tabla_final.columns)



#3.c. Verifica si hay filas duplicadas; si es así, elimínalas.
filas_duplicadas = tabla_final[tabla_final.duplicated()]
print("Las filas duplicadas son:", filas_duplicadas)

df_nuevo_sin_duplicados= tabla_final.drop_duplicates()

filas_duplicadas = df_nuevo_sin_duplicados[df_nuevo_sin_duplicados.duplicated()]
print("Las filas duplicadas son:", filas_duplicadas)

#4. ¿Cuántos sujetos de género F hay en el DataFrame resultante? hint: usa el método .value_counts() sobre la columna.

Q_Femenino = df_nuevo_sin_duplicados['gender'].value_counts().get('F', 0)
print(f"Cantidad género F: {Q_Femenino}")

#4.¿Encuántos números de caso hay por lo menos una sospechosa que sea mujer? hint: utiliza el método unique() para obtener los valores únicos de una columna específica de  un DataFrame luego de filtrar.

sospecha_mujer = df_nuevo_sin_duplicados[df_nuevo_sin_duplicados['gender'] == 'F']

# valores únicos donde aparece al menos una mujer
casos_mujeres = sospecha_mujer['case_number'].unique()

# Contar cuántos casos únicos hay
cantidad_casos = len(casos_mujeres)

print(f"la cantidad de {cantidad_casos} casos de sospecha de mujer.")


#5.Genera una tabla pivote que muestre en las filas el género del oficial y en las columnas el  género del subject. ¿Cómo interpretas los valores que muestra esta vista?

tabla_pivote = pd.pivot_table(
    df_nuevo_sin_duplicados, 
    index='gender', 
    columns='subjects', 
    aggfunc='size', 
    fill_value=0
)

print(tabla_pivote)


 #Para continuar con el desarrollo de este desafío, necesitarás el archivos  Cleaned_DS_Jobs.csv
import pandas as pd 

ruta_archivo = r'C:\Users\eliza\OneDrive\Escritorio\PYTHON\desafio5\Cleaned_DS_Jobs.csv'

df_cleaned = pd.read_csv(ruta_archivo)

# Mostrar las primeras filas
print(df_cleaned.head())

#Utiliza la siguiente lista de valores que serán considerados como nulos: ["na", "NA",-1, "0", "-1", "null", "n/a", "N/A", "NULL"]  (hint: utiliza el método replace para reemplazar los valores indicados por np.nan)

import numpy as np

valor_nulo = ["na", "NA", -1, "0", "-1", "null", "n/a", "N/A", "NULL"]
df_cleaned = df_cleaned.replace(valor_nulo, np.nan)
print(df_cleaned.isna().sum())


#Elimina todas las filas con datos faltantes. (hint: utiliza el método .dropna())
df_cleaned = df_cleaned.dropna()
print(df_cleaned.isna().sum()) 


#Apartir de la columna “Salary Estimate”, genera dos columnas: Salario Estimado Mínimo  y Máximo. (hint: Utiliza el método apply sobre la columna.)

#Realiza la recodificación de la columna Size con los valores de la siguiente tabla: (hint: utilice reemplazo con diccionario usando el método replace sobre la columna.)
diccionario_size = {
    '10000+ employees': 'MegaEmpresas',
    '5001 to 10000 employees': 'Grandes Empresas',
    '1001 to 5000 employees': 'Medianas Empresas',
    '501 to 1000 employees': 'Pequeñas Grandes Empresas',
    '201 to 500 employees': 'Pequeñas Empresas',
    '51 to 200 employees': 'Pequeñas Empresas',
    '1 to 50 employees': 'Microempresas',
    'Unknown': 'Empresas sin Información',
    '-1': 'Empresas sin Información',  
    '0': 'Empresas sin Información',  
}

df_cleaned['Size'] = df_cleaned['Size'].replace(diccionario_size)
print(df_cleaned['Size'].value_counts())


#Finalmente, genera una tabla pivote que muestre la media del salario estimado mínimo y  la media del salario estimado máximo por tamaño de empresa. (hint: utiliza  pd.pivot_table para generar la vista adecuada con las columnas generadas.)

tabla_S = pd.pivot_table(
    df_cleaned,
    index='Size',
    values=['min_salary', 'max_salary'],
    aggfunc='mean'
)

print(tabla_S)