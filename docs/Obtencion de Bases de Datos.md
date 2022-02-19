# Obtención de bases de datos

En este modulo se encuentra todo lo relacionado con la obtención de los datos para su posterior tratamiento

## ¿Qué se obtiene?

- Microdata
- Canasta básica
- Adulto equivalente
- En construcción...

## ¿En qué formato se obtienen?

Los archivos originales se encuentran en formato.csv comprimidos en formato .zip
Lo que se alacema efectivamente en disco es el archivo .zip

## ¿Desde dónde se obtienen?

Los archivos se encuentran almacenados en github. Esto debido a la necesidad de estandarizar los archivos para su posterior procesamiento en los cálculos.
Los archivo servidos por INDEC se encuentran descentralizados y con diferentes nomenclaturas.
Y, además, de esta manera ahorramos el posible mal funcionamiento del módulo de descarga de la libreria puesto que no siempre está disponible el sitio de INDEC para su consulta.
En cualquier caso, de verse necesario realizar la obtención de los datos desde INDEC por asuntos de fiabilidad, es un llamamiento a la comunidad para desarrollar esa sescción. En getter.py se deberá modificar el método from_indec()

## ¿Cómo es el mecanismo de obtención?

Dependiendo el tipo de base que se quiera obtener, se realizarán diferentes acciones.

Por ejemplo al realizar la consulta de los microdatos

```python
datos = pyeph.get(data="eph", year=2017, period=2)
```

la libreria revisa si existe en local el archivo de la eph solicitada. En caso de que exista, retorna el DataFrame del archivo .csv; en caso de no existir primero realiza su descarga.

Si se realiza la consulta de las canastas

```python
datos = pyeph.get(data="canastas")
```

la librería intenta obtener las CBA y CBT más actualizadas. Retornará la ultima que encuentre

## ¿Dónde se almacenan?

Los archivos descargados se pueden encontrar dentro de la carpeta ".db", localizada dentro de "ruta-local-de-python/site-packages/pyeph/"