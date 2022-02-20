# Obtención de bases de datos

La función  `pyeph.obtener()` o `pyeph.get()` - genera la obtención de un pandas.DataFrame de las bases que el usuario solicite.

## ¿Qué se obtiene?

- Microdata
- Canasta básica
- Adulto equivalente
- En construcción...

## ¿En qué formato se obtienen?

Los archivos originales se encuentran en formato '.csv' comprimidos en formato '.zip'
Lo que se alacema efectivamente en disco es el archivo '.zip'

## ¿Desde dónde se obtienen?

Los archivos se encuentran almacenados en github. Esto debido a la necesidad de estandarizar los archivos para su posterior procesamiento en los cálculos.
Los archivo servidos por INDEC se encuentran descentralizados y con diferentes nomenclaturas.
Y, además, de esta manera ahorramos el posible mal funcionamiento del módulo de descarga de la libreria puesto que no siempre está disponible el sitio de INDEC para su consulta.
En cualquier caso, de verse necesario realizar la obtención de los datos desde INDEC por asuntos de fiabilidad, es un llamamiento a la comunidad para desarrollar esa sescción. En getter.py se deberá modificar el método from_indec()

## ¿Dónde se almacenan?

Los archivos descargados se pueden encontrar dentro de la carpeta ".db", localizada dentro de "ruta-local-de-python/site-packages/pyeph/"

## Uso

Dependiendo el tipo de base que se quiera obtener, se realizarán diferentes acciones. 

### Microdatos

Al peticionar los microdatos pyeph revisa si existe el archivo de la eph solicitada en local. En caso de que exista, retorna el DataFrame del archivo .csv; en caso de no existir primero realiza su descarga.

```python
pyeph.obtener(data="eph", ano=2017, periodo=2, frecuencia="trimestre", tipo_base="individual")

o

pyeph.get(data="eph", year=2017, period=2, freq="trimestre", base_type="individual")
```

#### Parámetros

| Parámetros | Tipo de dato | Descripción |
| -------- | ------------- | -------- |
| data=eph | str | "eph" para solicitar los microdatos de las EPH's |
| ano (year) | int | Año de la EPH solicitada |
| periodo (period) | int | Periodo de la EPH solicitada |
| frecuencia (freq) | str | Frecuencia de periodización (default: "trimestre") |
| tipo_base (base_type) | str | Tipo de base (Hogar o Individual) (default: "individual") |


### Canasta Básica Alimentaria y Canasta Básica Total

Al peticionar la canasta pyeph intenta obtener las CBA y CBT más actualizadas. Retornará la ultima que encuentre

```python
pyeph.obtener(data="canastas")

o

pyeph.get(data="basket")
```

#### Parámetros

| Parámetros | Tipo de dato | Descripción |
| -------- | ------------- | -------- |
| data=canastas (basket) | str | CBA y CBT |
