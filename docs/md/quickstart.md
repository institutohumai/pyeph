# Uso básico

Los siguientes son algunos ejemplos de uso. Para ver todos los cálculos podés ir para la documentación

En inglés

```python
import pyeph

# Obtención
eph = pyeph.get(data="eph", year=2021, period=2, base_type='individual') # EPH individual
basket = pyeph.get(data="canastas") # canasta basica total y alimentaria
adequi = pyeph.get(data="adulto-equivalente") # adulto equivalente

# Cálculos de ejemplo de pobreza 
poverty = pyeph.Poverty(eph, basket)
population_poverty = poverty.population(group_by='CH04') # Población pobre por sexo 
labeled_poverty = pyeph.map_labels(population_poverty) # Etiquetado de las variables

# Cálculos de Mercado Laboral
labor_market = pyeph.LaborMarket(eph)
unemployment = labor_market.unemployment(group_by="REGION", div_by="PT") # Desempleo agrupado por region y dividiendo por Población Total
labeled_unemployment = pyeph.map_labels(unemployment) # Etiquetado de las variables
```

En español

```python
import pyeph

# Obtención
eph = pyeph.obtener(data="eph", ano=2021, periodo=2, tipo_base='individual') # EPH individual
canastas = pyeph.obtener(data="canastas") # canasta basica total y alimentaria
adequi = pyeph.obtener(data="adulto-equivalente") # adulto equivalente

# Cálculos de ejemplo de pobreza 
pobreza = pyeph.Pobreza(eph, canastas)
poblacion_pobre = pobreza.poblacion(agrupar_por='CH04') # Población pobre por sexo 
poblacion_pobre_etiquetado = pyeph.etiquetar(poblacion_pobre) # Etiquetado de las variables

# Cálculos de Mercado Laboral
mercado_laboral = pyeph.MercadoLaboral(eph)
desempleo = mercado_laboral.desempleo(agrupar_por="REGION", div_por="PT") # Desempleo agrupado por region y dividiendo por Población Total
desempleo_etiquetado = pyeph.etiquetar(desempleo) # Etiquetado de las variables
```
