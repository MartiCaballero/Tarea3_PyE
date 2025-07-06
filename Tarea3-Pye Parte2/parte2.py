import pandas as pd     
import numpy as np      
from scipy.stats import t 

df = pd.read_csv('velocidad_internet_ucu.csv')

print(df.head())

central = df[df['codigo_edificio'] == 1]['Velocidad Mb/s']
semprun = df[df['codigo_edificio'] == 2]['Velocidad Mb/s']

# Estadísticos de CENTRAL
n1 = len(central)
media1 = np.mean(central)
std1 = np.std(central, ddof=1) 

print("CENTRAL: n =", n1, ", media =", round(media1,2), ", desvío =", round(std1,2))

#Estadísticos de SEMPRUN
n2 = len(semprun)
media2 = np.mean(semprun)
std2 = np.std(semprun, ddof=1)

print("SEMPRUN: n =", n2, ", media =", round(media2,2), ", desvío =", round(std2,2))

t_stat = (media1 - media2) / np.sqrt((std1**2)/n1 + (std2**2)/n2)
print("t observada =", round(t_stat, 4))

df_welch = ((std1**2)/n1 + (std2**2)/n2)**2 / (
    ((std1**2/n1)**2)/(n1 - 1) + ((std2**2/n2)**2)/(n2 - 1)
)
print("Grados de libertad =", round(df_welch, 2))

alpha = 0.05
t_crit = t.ppf(alpha, df_welch)
p_value = t.cdf(t_stat, df_welch)

print("Valor crítico t =", round(t_crit, 4))
print("p-valor =", round(p_value, 4))

if t_stat < t_crit:
    print("Se rechaza H0: la velocidad en Central es significativamente menor.")
else:
    print("No se puede rechazar H0: no hay evidencia suficiente.")

