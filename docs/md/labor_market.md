# Cálculos de Mercado Laboral

La clase  `pyeph.MercadoLaboral()` o `pyeph.LaborMarket()` - prepara las bases para los cálculos de los diferentes indicadores habituales vinculados al mercado laboral. Tiene tres métodos principales -`empleo()`/`employment()`, `desempleo()`/`unemployment()` y `actividad()`/`activity()`- que devuleven un dataframe con información referida a cada indicador.

## Uso

La clase `pyeph.MercadoLaboral()` o `pyeph.LaborMarket()` recibe los siguientes parámetros:

```python
pyeph.MercadoLaboral(eph)

o

pyeph.LaborMarket(eph)
```

## Parámetros

| Parámetros | Tipo de dato | Descripción |
| -------- | ------------- | -------- |
| eph | pandas.DataFrame | Base de EPH individual publicada por INDEC. |


## Métodos

La clase `pyeph.MercadoLaboral()` o `pyeph.LaborMarket()` prepara las bases para los cálculos de los diferentes indicadores habituales vinculados al mercado laboral. Para obtener el dataframe con los resultados podrá consultar los métodos `empleo()`/`employment()`, `desempleo()`/`unemployment()` o `actividad()`/`activity()`, según corresponda.


* Empleo

Este método retorna como resultado un pandas.DataFrame donde se especifica [...].

```python
pyeph.MercadoLaboral(eph).empleo(agrupar_por, div_por)

o 

pyeph.LaborMarket(eph).employment(group_by, div_by)
```
| Parámetros | Tipo de dato | Descripción |
| -------- | ------------- | -------- |
| group_by (agrupar_por) | str or list, default: None | Nombre de la variable o lista de nombres de las variables por las cuales se desea agrupar y calcular los indicadores. Ejemplo: 'CH04' o  [ 'CH04', 'REGION']|
| div_by (div_por) | str, default='PT' | Indica la población que se utilizará para el cálculo de la tasa de empleo. Puede asumir 'PT' indicando población total o 'PET' indicando población en edad de trabajar.
* Desempleo

Este método retorna como resultado un pandas.DataFrame donde se especifica [...].

```python
pyeph.MercadoLaboral(eph).desempleo(agrupar_por, div_por)

o 

pyeph.LaborMarket(eph).unemployment(group_by, div_by)
```
| Parámetros | Tipo de dato | Descripción |
| -------- | ------------- | -------- |
| group_by (agrupar_por) | str or list, default: None | Nombre de la variable o lista de nombres de las variables por las cuales se desea agrupar y calcular los indicadores. Ejemplo: 'CH04' o  [ 'CH04', 'REGION']|
| div_by (div_por) | str, default='PET' | Indica la población que se utilizará para el cálculo de la tasa de empleo. Puede asumir 'PT' indicando población total o 'PET' indicando población en edad de trabajar.
* Actividad

Este método retorna como resultado un pandas.DataFrame donde se especifica [...].

```python
pyeph.MercadoLaboral(eph).actividad(agrupar_por, div_por)

o 

pyeph.LaborMarket(eph).activity(group_by, div_by)
```
| Parámetros | Tipo de dato | Descripción |
| -------- | ------------- | -------- |
| group_by (agrupar_por) | str or list, default: None | Nombre de la variable o lista de nombres de las variables por las cuales se desea agrupar y calcular los indicadores. Ejemplo: 'CH04' o  [ 'CH04', 'REGION']|
| div_by (div_por) | str, default='PT' | Indica la población que se utilizará para el cálculo de la tasa de empleo. Puede asumir 'PT' indicando población total o 'PET' indicando población en edad de trabajar.

## Ejemplos

Primero se instancia la clase `pyeph.MercadoLaboral()` o `pyeph.LaborMarket()`:

```python
import pyeph

# Obtencion de la base de datos 
eph = pyeph.obtener(data="eph", ano=2019, periodo=1, tipo_base='individual') # INGLÉS: eph = pyeph.get(data="eph", year=2019, period=1, base_type='individual')

```
Resultado:

|index|CODUSU|ANO4|TRIMESTRE|NRO\_HOGAR|COMPONENTE|H15|REGION|MAS\_500|AGLOMERADO|PONDERA|CH03|CH04|CH05|CH06|CH07|CH08|CH09|CH10|CH11|CH12|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|0|TQRMNOPPUHKNKNCDEFOCD00629562|2019|1|2|2|1|41|N|8|108|2|2|03/06/1990|28|1|4|1|2|0|4|
|1|TQRMNOPPUHKNKNCDEFOCD00629562|2019|1|2|3|1|41|N|8|108|3|2|29/12/2005|13|5|4|1|1|1|4|
|2|TQRMNOPPUHKNKNCDEFOCD00629562|2019|1|2|4|0|41|N|8|108|3|1|26/01/2018|1|5|4|3|0|0|0|
|3|TQRMNORUQHKNKNCDEFOCD00629563|2019|1|1|1|1|41|N|8|108|1|2|30/03/1978|41|5|4|1|2|0|6|
|4|TQRMNORUQHKNKNCDEFOCD00629563|2019|1|1|2|0|41|N|8|108|3|2|20/09/2009|9|5|4|1|1|1|2|
|5|TQRMNOPUVHKOKMCDEFOCD00629564|2019|1|1|2|1|41|N|8|141|1|1|26/04/1967|51|3|4|1|2|0|2|
|6|TQRMNOQWVHMNLPCDEFOCD00629565|2019|1|1|1|1|41|N|8|221|1|1|15/03/1955|63|2|1|1|2|0|4|
|7|TQRMNOQWVHMNLPCDEFOCD00629565|2019|1|1|2|1|41|N|8|221|2|2|25/04/1956|62|2|1|1|2|0|4|
|8|TQRMNOQWVHMNLPCDEFOCD00629565|2019|1|1|3|1|41|N|8|221|3|2|10/06/1994|24|5|1|1|1|1|7|
|9|TQRMNOQWXHMNLPCDEFOCD00629566|2019|1|1|1|1|41|N|8|221|1|1|22/07/1944|74|4|1|1|2|0|2|

```python
# Instanciar la clase LaborMarket o MercadoLaboral
mercado_laboral = pyeph.MercadoLaboral(eph) # INGLÉS: mercado_laboral = pyeph.LaborMarket(eph)
```
Una vez instancida la clase con una EPH individual particular, se pueden calcular los indicadores del mercado laboral, ejecutando los diferentes métodos.

### Desempleo

Una vez instanciada la clase `pyeph.MercadoLaboral()` o `pyeph.LaborMarket()` se ejecuta el método `desempleo()`/`unemployment()`:

```python
# Calculo de Desempleo General 

print("\nTasa de desempleo considerando la Población en Edad de Trabajar:\n")
print(mercado_laboral.desempleo()) # INGLÉS: mercado_laboral.unemployment()
```
Resultado:

Tasa de desempleo considerando la Población en Edad de Trabajar:
|Tasa de Desempleo|
|---|
|10\.1|

```python
print("\nTasa de desempleo considerando la Población Total:\n")
print(mercado_laboral.desempleo(div_por='PT')) # INGLÉS: mercado_laboral.unemployment(div_by='PT')
```

Resultado:

Tasa de desempleo considerando la Población Total:

|Tasa de Desempleo|
|---|
|10\.1|

```python

# Calculo de Desempleo agrupado por categoría (puede ser mas de una)

print("\nTasa de desempleo considerando la Población en Edad de Trabajar según sexo:\n")
print(mercado_laboral.desempleo(agrupar_por = 'CH04')) # INGLÉS: mercado_laboral.unemployment(group_by='CH04')
```
Resultado:

Tasa de desempleo considerando la Población en Edad de Trabajar según sexo:

|CH04|Tasa de Desempleo|
|---|---|
|1|9\.2|
|2|11\.2|

```python

print("\nTasa de desempleo considerando la Población Total según sexo:\n")
print(mercado_laboral.desempleo(agrupar_por = 'CH04', div_por='PT')) # INGLÉS: mercado_laboral.unemployment(group_by='CH04', div_by='PT')


```
Resultado:

Tasa de desempleo considerando la Población Total según sexo:

|CH04|Tasa de Desempleo|
|---|---|
|1|9\.2|
|2|11\.2|

### Empleo

Una vez instanciada la clase `pyeph.MercadoLaboral()` o `pyeph.LaborMarket()` se ejecuta el método `empleo()`/`employment()`:

```python
# Calculo de Empleo General 

print("\nTasa de empleo considerando la Población en Edad de Trabajar:\n")
print(mercado_laboral.empleo()) # INGLÉS: mercado_laboral.employment()

```
Resultado:

Tasa de empleo considerando la Población en Edad de Trabajar:

|Tasa de Empleo|
|---|
|42\.3|

```python

print("\nTasa de empleo considerando la Población Total:\n")
print(mercado_laboral.empleo(div_por='PT')) # INGLÉS: mercado_laboral.employment(div_by='PT')

```
Resultado:

Tasa de empleo considerando la Población Total:

|Tasa de Empleo|
|---|
|42\.3|


```python

# Calculo de Empleo agrupado por categoría (puede ser mas de una)

print("\nTasa de empleo considerando la Población en Edad de Trabajar según sexo:\n")
print(mercado_laboral.empleo(agrupar_por = 'CH04')) # INGLÉS: mercado_laboral.employment(group_by='CH04')

```
Resultado:

Tasa de empleo considerando la Población en Edad de Trabajar según sexo:

|CH04|Tasa de Empleo|
|---|---|
|1|49\.7|
|2|35\.3|
```python

print("\nTasa de empleo considerando la Población Total según sexo:\n")
print(mercado_laboral.empleo(agrupar_por = 'CH04', div_por='PT')) # INGLÉS: mercado_laboral.employment(group_by='CH04', div_by='PT')

```

Resultado:

Tasa de empleo considerando la Población Total según sexo:

|CH04|Tasa de Empleo|
|---|---|
|1|49\.7|
|2|35\.3|

### Actividad

Una vez instanciada la clase `pyeph.MercadoLaboral()` o `pyeph.LaborMarket()` se ejecuta el método `actividad()`/`activity()`:


```python

# Calculo de Actividad General

print("\nTasa de actividad considerando la Población en Edad de Trabajar:\n")
print(mercado_laboral.actividad()) # INGLÉS: mercado_laboral.activity()

```

Resultado:

Tasa de actividad considerando la Población en Edad de Trabajar:
|Tasa de Actividad|
|---|
|47\.0|

```python

print("\nTasa de actividad considerando la Población Total:\n")
print(mercado_laboral.actividad(div_por='PT')) # INGLÉS: mercado_laboral.activity(div_by='PT')

```
Resultado:

Tasa de actividad considerando la Población Total:

|Tasa de Actividad|
|---|
|47\.0|

```python

# Calculo de Actividad agrupado por categoría (puede ser mas de una)

print("\nTasa de actividad considerando la Población en Edad de Trabajar según sexo:\n")
print(mercado_laboral.actividad(agrupar_por = 'CH04')) # INGLÉS: mercado_laboral.activity(group_by='CH04')
```
Resultado:

Tasa de actividad considerando la Población en Edad de Trabajar según sexo:

|CH04|Tasa de Actividad|
|---|---|
|1|54\.7|
|2|39\.8|



```python


print("\nTasa de actividad considerando la Población Total según sexo:\n")
print(mercado_laboral.actividad(agrupar_por = 'CH04', div_por='PT')) # INGLÉS: mercado_laboral.activity(group_by='CH04', div_by='PT')

```

Resultado:

Tasa de actividad considerando la Población Total según sexo:

|CH04|Tasa de Actividad|
|---|---|
|1|54\.7|
|2|39\.8|