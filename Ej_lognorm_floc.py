import numpy as np
from scipy import stats

# Datos de ejemplo
data = np.array([100, 200, 300, 500, 800, 1200])

# Caso 1: Sin fijar loc (3 parámetros)
s1, loc1, scale1 = stats.lognorm.fit(data)
print("Sin floc=0:")
print(f"  shape (s) = {s1:.4f}")
print(f"  loc = {loc1:.4f}")  # ← Puede ser cualquier valor
print(f"  scale = {scale1:.4f}")

# Caso 2: Fijando loc=0 (2 parámetros)
s2, loc2, scale2 = stats.lognorm.fit(data, floc=0)
print("\nCon floc=0:")
print(f"  shape (s) = {s2:.4f}")
print(f"  loc = {loc2:.4f}")  # ← Siempre 0
print(f"  scale = {scale2:.4f}")

# Verificación manual:
log_data = np.log(data)
mu_manual = log_data.mean()
sigma_manual = log_data.std(ddof=0)  # Aca se hace ddof=0 porque el metodo stats.lognorm.fit calcula la desviacion estandar con ddof=0. De esta forma es comparable.


print("\nCálculo manual (con loc=0):")
print(f"  sigma_log = {sigma_manual:.4f} (debe ≈ s2)")
print(f"  exp(mu_log) = {np.exp(mu_manual):.4f} (debe ≈ scale2)")