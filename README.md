# Ej_lognorm_floc
Explicacion de floc=0 para distribucion lognormal

# Análisis de Frecuencias Hidrológicas

## Parámetro `floc` en Distribución Lognormal

### ¿Qué es la distribución Lognormal en scipy? 

En `scipy.stats`, las distribuciones continuas tienen **3 parámetros genéricos**:

1. **Parámetros de forma** (shape): definen la "forma" de la distribución
2. **`loc`** (location): desplaza la distribución horizontalmente
3. **`scale`**: escala la distribución

Para la **lognormal**, la parametrización es: 

```
Y = loc + scale * X
```

Donde:
- `X` ~ Lognormal estándar con parámetro de forma `s` (sigma)
- `Y` es la variable final
- **`s`** (shape) = σ = desviación estándar de ln(X)
- **`scale`** = exp(μ) = mediana de la distribución
- **`loc`** = desplazamiento (threshold)

### ¿Qué es `floc`?

`floc` = **"fixed location"** (localización fija)

Cuando usas `.fit()`, scipy intenta estimar **los 3 parámetros** simultáneamente.  Pero en hidrología, casi siempre queremos la **lognormal de 2 parámetros** (sin desplazamiento), donde: 

- El valor mínimo teórico es **0** (no negativo)
- `loc = 0`

#### Comparación: 

```python
# SIN fijar loc (estima 3 parámetros):
shape, loc, scale = stats.lognorm.fit(Data.iloc[:, 0])
# loc podría ser cualquier valor → Lognormal de 3 parámetros

# CON floc=0 (fija loc=0, estima solo 2 parámetros):
shape, loc, scale = stats.lognorm.fit(Data.iloc[:, 0], floc=0)
# loc = 0 (fijo) → Lognormal de 2 parámetros (estándar en hidrología)
```

### Ejemplo numérico

```python
import numpy as np
from scipy import stats

# Datos de ejemplo
data = np.array([100, 200, 300, 500, 800, 1200])

# Caso 1: Sin fijar loc (3 parámetros)
s1, loc1, scale1 = stats.lognorm.fit(data)
print("Sin floc=0:")
print(f"  shape (s) = {s1:.4f}")
print(f"  loc = {loc1:.4f}")  # ← Puede ser cualquier valor
print(f"  scale = {scale1:. 4f}")

# Caso 2: Fijando loc=0 (2 parámetros)
s2, loc2, scale2 = stats.lognorm.fit(data, floc=0)
print("\nCon floc=0:")
print(f"  shape (s) = {s2:.4f}")
print(f"  loc = {loc2:.4f}")  # ← Siempre 0
print(f"  scale = {scale2:. 4f}")

# Verificación manual:
log_data = np.log(data)
mu_manual = log_data.mean()
sigma_manual = log_data.std(ddof=0)  # MLE usa ddof=0

print("\nCálculo manual (con loc=0):")
print(f"  sigma_log = {sigma_manual:.4f} (debe ≈ s2)")
print(f"  exp(mu_log) = {np.exp(mu_manual):.4f} (debe ≈ scale2)")
```

### ¿Cuándo usar cada uno?

| Caso | Parámetros | Cuándo usar |
|------|-----------|-------------|
| **`floc=0`** | 2 parámetros (s, scale) | **HIDROLOGÍA**:  caudales, precipitaciones (valores ≥ 0) |
| **Sin `floc`** | 3 parámetros (s, loc, scale) | Datos con umbral desconocido o cuando loc ≠ 0 |

### Recomendación para análisis de frecuencias hidrológicas

```python
# RECOMENDADO para análisis de frecuencias hidrológicas:
shape, loc, scale = stats.lognorm.fit(Data.iloc[:, 0], floc=0)
```

Esto garantiza que:
1. ✅ La distribución no permita valores negativos
2. ✅ Los parámetros coincidan con el cálculo manual (`mu_log`, `sigma_log`)
3. ✅ Sea consistente con la teoría hidrológica estándar

### Resumen

- **`floc=0`**: Fija el parámetro `loc` en 0 durante el ajuste
- **Sin `floc=0`**: Scipy estima `loc` automáticamente (puede ser ≠ 0)
- **Para hidrología**: Casi siempre usa `floc=0` (lognormal de 2 parámetros)

---

## ¿Qué significa MLE? 

**MLE** significa **"Maximum Likelihood Estimation"** (Estimación de Máxima Verosimilitud).

### Concepto

Es un **método estadístico** para estimar los parámetros de una distribución de probabilidad que **maximizan la probabilidad** de observar los datos que tienes.

#### Ejemplo intuitivo:

Si tienes datos de caudales:  [100, 200, 150, 300, 250]

MLE pregunta: *"¿Qué valores de μ (mu) y σ (sigma) hacen que estos datos sean **más probables** de ocurrir según una distribución Normal?"*

### MLE vs. Método de Momentos

| Método | Descripción | Ejemplo (Normal) | ddof |
|--------|-------------|------------------|------|
| **Método de Momentos** | Iguala momentos muestrales con teóricos | μ = media, σ² = varianza muestral | ddof=1 (insesgado) |
| **MLE** | Maximiza la función de verosimilitud | μ = media, σ² = varianza **poblacional** | ddof=0 |

### Diferencia clave

Para la distribución **Normal**:
- **Ambos métodos** dan el mismo **μ** (promedio)
- **Difieren en σ** (desviación estándar):

```python
# Método de Momentos (insesgado):
sigma_momentos = data.std(ddof=1)  # Divide por (n-1)

# MLE:
sigma_mle = data. std(ddof=0)  # Divide por n
```

**Relación matemática:**
```python
sigma_momentos = sigma_mle * sqrt(n / (n-1))
```

### ¿Por qué `stats.norm.fit()` usa MLE?

Porque `scipy.stats.fit()` implementa el algoritmo de **máxima verosimilitud** por defecto, que:

✅ Tiene propiedades estadísticas óptimas (asintóticamente eficiente)  
✅ Es consistente para cualquier distribución  
✅ Pero es **sesgado** para muestras pequeñas (por eso usa ddof=0)

### En el código

```python
# stats.norm.fit() usa MLE internamente: 
mu_fit_norm, sigma_fit_mle_norm = stats.norm. fit(Data.iloc[:, 0])
# ↑ sigma_fit_mle_norm usa ddof=0 (sesgado para muestras pequeñas)

# Ajuste manual a ddof=1 (insesgado):
sigma_fit_norm = sigma_fit_mle_norm * np.sqrt(n / (n - 1))
# ↑ Ahora coincide con Data.std(ddof=1)
```

### Ejemplo numérico

```python
data = np.array([100, 200, 300, 400, 500])
n = len(data)

# MLE (ddof=0):
sigma_mle = data. std(ddof=0)  # = 141.42

# Método de Momentos (ddof=1):
sigma_momentos = data.std(ddof=1)  # = 158.11

# Verificación:
print(sigma_mle * np.sqrt(n/(n-1)))  # = 158.11 ✓*

