# Puente de comparabilidad (rediseño 2024)

A partir del **4.º trimestre de 2024**, el rediseño del cuestionario de la EPH eliminó de las bases usuarias varias variables agregadas, que fueron publicadas en su lugar como sub-componentes por fuente. Cualquier serie que use esas variables (ingresos no laborales, estrategias de los hogares) se corta en 2024-T3 si no se reconstruyen.

La función `pyeph.comparability_bridge()` o `pyeph.puente_comparabilidad()` reconstruye las variables eliminadas con reglas determinísticas, para mantener la comparabilidad con la serie histórica:

| Base | Variables reconstruidas | A partir de |
| -------- | ------------- | -------- |
| Hogar | `V5` (subsidio en dinero), `V11` (beca de estudio), `V21` (aguinaldo), `V22` (retroactivos) | `V5_01`–`V5_03`, `V11_01`–`V11_02`, `V21_01`–`V21_03`, `V22_01`–`V22_03` |
| Individual | `V2_M`, `V5_M`, `V11_M`, `V21_M`, `V22_M` (montos de ingresos no laborales) | sus sub-componentes `*_0X_M`, con la variable de estrategia del hogar como control |

Además corrige, si detecta la condición de error, la **inversión de las columnas `PP11L1` y `PP11L2`** de la base individual (sus contenidos aparecen intercambiados en las bases publicadas).

Las bases anteriores a 2024-T4 no requieren puente y se devuelven sin cambios. Si una variable agregada ya existe, o faltan sus sub-componentes, su reconstrucción se omite con un aviso. Ningún valor existente se modifica (única excepción: el intercambio PP11L1/PP11L2).

## Uso

```python
import pyeph

hogares    = pyeph.get(data="eph", year=2025, period=1, base_type="hogar")
individuos = pyeph.get(data="eph", year=2025, period=1, base_type="individual")

hogares    = pyeph.comparability_bridge(hogares)
individuos = pyeph.comparability_bridge(individuos, base_hogar=hogares)
```

## Parámetros

| Parámetros | Tipo de dato | Descripción |
| -------- | ------------- | -------- |
| base | pandas.DataFrame | Base usuaria de la EPH (hogar o individual). El tipo se detecta por la presencia de la columna `COMPONENTE`. |
| base_hogar | pandas.DataFrame | Base hogar del mismo trimestre. Obligatoria cuando `base` es individual (aporta las variables control); se ignora cuando `base` ya es de hogar. |

## Metodología y cómo citar

Las reglas de reconstrucción están documentadas y validadas en:

> Tessmer, G. y Boggiano, B. (2026). *From Breaks to Bridges: An Architecture for Survey Redesigns That Expand Conceptual Scope*. SSRN Working Paper 6597399. <https://papers.ssrn.com/abstract=6597399>

> Observatorio Económico Social UNR. *Manual Metodológico EPH – Observatorio*, Parte A. <https://hdl.handle.net/2133/33253>

Si esta función resulta útil para tu investigación, citá el paper. Las mismas reglas están en producción desde 2024-T4 en el pipeline EPH-Observatorio, cuyos datasets (la EPH explicada, etiquetada y ampliada, con las variables ya reconstruidas) están publicados en el **Dataverse de la UNR**:

> Observatorio Económico Social UNR. *Encuesta Permanente de Hogares de Argentina (EPH - Observatorio)*. <https://doi.org/10.57715/UNR/BL85Z8>

Existe una implementación equivalente propuesta para el paquete [`eph` de R](https://github.com/ropensci/eph/issues/70) y un módulo de Stata (`ephbridge`, en preparación para SSC); las tres implementaciones están verificadas entre sí mediante chequeos de equivalencia exhaustivos.
