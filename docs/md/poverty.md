# Cálculo de la Pobreza e Indigencia

La clase  `pyeph.Pobreza()` o `pyeph.Poverty()` - instancia el calculo de la pobreza e indigencia utilizando la metodología de línea para las bases trimestrales. Tiene dos métodos principales (`hogares()`/`household()` y `poblacion()`/`population()`) que devuleven un dataframe con información referida a la tasa de pobreza de personas y la tasa de pobreza de hogares.

Aclaración: No existe información publicada fuera de los informes de prensa en formato pdf sobre los valores de las canastas básicas y alimentarias. No obstante, hemos desarrollado dos funcionaes que, de encontrarse disponibles dichos datos, podrían calcular de forma automática los valores de pobreza e indigencia.

## Uso

La clase `pyeph.Pobreza()` o `pyeph.Poverty()` recibe los siguientes parámetros:

```python
pyeph.Pobreza(eph, canasta)

o

pyeph.Poverty(eph, basket)
```

## Parámetros

| Parámetros | Tipo de dato | Descripción |
| -------- | ------------- | -------- |
| eph | pandas.DataFrame | Base de EPH individual publicada por INDEC. |
| basket (canasta)| pandas.DataFrame | Base de datos de Canasta Básica Total y Canasta Básica Alimentaria con el formato específicado [aquí](https://github.com/institutohumai/eph-python/blob/master/pyeph/tools/.examples/canasta_ejemplo.csv#markdown).|



## Métodos

La clase `pyeph.Pobreza()` o `pyeph.Poverty()` instancia el calculo de pobreza e indigencia. Para obtener el dataframe con los resultados podrá consultar los métodos `hogares()`/`household()`  o `poblacion()`/`population()`, según corresponda.


* Pobreza e Indigencia de Personas

Este método retorna como resultado un pandas.DataFrame donde se especifica el porcentaje y la cantidad  de personas en situación de pobreza e indigencia. Esta información puede calcularse agrupada por otras categorías de interés (ejemplo: sexo).

```python
pyeph.Pobreza(eph, canasta).poblacion(agrupar_por)

o 

pyeph.Poverty(eph, basket).population(group_by)
```

* Pobreza e Indigencia de Hogares


Este método retorna como resultado un pandas.DataFrame donde se especifica el porcentaje y la cantidad  de hogares en situación de pobreza e indigencia. En este caso, no es posible obtener la información agrupada por otra categoría.


```python
pyeph.Pobreza(eph, canasta).hogares()

o

pyeph.Poverty(eph, basket).household()
```


## Ejemplos

Primero se instancia la clase `pyeph.Pobreza()` o `pyeph.Poverty()` :

```python
import pyeph

# Obtencion de la base de datos 
eph = pyeph.obtener(data="eph", ano=2019, periodo=1, tipo_base='individual') # INGLÉS: eph = pyeph.get(data="eph", year=2019, period=1, base_type='individual')

#Obtencion de la canasta
canasta = pyeph.obtener(data="canastas") # INGLÉS: canasta = pyeph.get(data="canastas")

# Instanciar la clase Pobreza() o Poverty()
pobreza = pyeph.Pobreza(eph=eph, canasta=canasta) # INGLÉS: pobreza = pyeph.Poverty(eph=eph, basket=canasta)
```
Una vez instancida la clase con una EPH individual particular, se puede calcular la tasa de pobreza e indigencia de personas y de hogares, ejecutando los diferentes métodos.


### Pobreza e Indigencia de Personas

Una vez instanciada la clase `pyeph.Pobreza()` o `pyeph.Poverty()`  se ejecuta el método `poblacion()`/`population()`:

```python
# Calculo de Pobreza e Indigencia (general)

print('Pobreza de personas:')
pobreza_personas = pobreza.poblacion() # INGLÉS: pobreza_personas = pobreza.population()


# Calculo de Pobreza e Indigencia agrupado por categoría (puede ser mas de una)
print('Pobreza de personas según sexo:')
pobreza_personas = pobreza.poblacion(agrupar_por='CH04') # INGLÉS: pobreza_personas = pobreza.population(group_by='CH04')
```

### Pobreza e Indigencia de Hogares

Una vez instanciada la clase `pyeph.Pobreza()` o `pyeph.Poverty()`  se ejecuta el método `hogares()`/`household()`:

```python
# Calculo de Pobreza e Indigencia (general)

print('Pobreza de hogares:')
pobreza_personas = pobreza.hogares() # INGLÉS: pobreza_personas = pobreza.household()

```