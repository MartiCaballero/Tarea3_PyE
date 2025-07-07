#Parte 1 del ejercicio: Distribución de hogares con mayores ingresos per cápita entre departamentos

# Importar las bibliotecas necesarias
import pandas as pd
from scipy.stats import chi2

# Cargar datos (ajustá la ruta si es necesario)
df = pd.read_csv("ech.csv")

# Crear la nueva columna de ingreso per cápita
df["ingreso_per_capita"] = df["ingreso"] / df["personas_hogar"]

# Clasificar hogares en quintiles según ingreso per cápita
df["quintil"] = pd.qcut(df["ingreso_per_capita"], 5, labels=[1, 2, 3, 4, 5])

# Filtrar los hogares del quintil superior (quintil 5) (quintil con mayor ingreso)
quintil_superior = df[df["quintil"] == 5]

# Construir la tabla de frecuencias observadas por departamento
frecuencias_observadas = quintil_superior["departamento"].value_counts().sort_index()

# Calcular las frecuencias esperadas bajo la hipótesis de distribución uniforme
k = df["departamento"].nunique()  # 19 departamentos
n = len(quintil_superior)                  # Total de hogares ricos (quintil 5)
esperadas = pd.Series([n / k] * k, index=frecuencias_observadas.index)

# Calcular el estadístico chi-cuadrado
chi_cuadrado = ((frecuencias_observadas - esperadas) ** 2 / esperadas).sum()

# Grados de libertad
grados_libertad = k - 1

# Valor crítico de chi-cuadrado para α = 0.05 y k - 1 grados de libertad
valor_critico = chi2.ppf(0.95, grados_libertad)

# Determinar si se rechaza la hipótesis nula
rechazar_nula = chi_cuadrado > valor_critico

# Imprimir resultados
print("Frecuencias observadas por departamento:")
print(frecuencias_observadas)

print("\nFrecuencias esperadas bajo la hipótesis de distribución uniforme:")
print(esperadas)

print(f"\nEstadístico chi-cuadrado: {chi_cuadrado}")
print(f"Valor crítico de chi-cuadrado (α = 0.05, k - 1 = {grados_libertad}): {valor_critico}")
print(f"¿Rechazar la hipótesis nula? {'Sí' if rechazar_nula else 'No'}")

# Interpretación de los resultados
if rechazar_nula:
    print("\nSe rechaza la hipótesis nula.\nEsto sugiere que los hogares con mayores ingresos per cápita no están distribuidos uniformemente entre los departamentos del país.")
else:
    print("\nNo se rechaza la hipótesis nula.\nEsto sugiere que no hay evidencia suficiente para afirmar que los hogares con mayores ingresos per cápita están distribuidos de manera desigual entre los departamentos del país.")


