PyEPH - Libreria para el procesamiento de la Encuesta Permanente de Hogares para Python
=====================================

PyEPH es una librería para el procesamiento de la [Encuesta Permanente de Hogares (eph)](https://www.indec.gob.ar/indec/web/Institucional-Indec-BasesDeDatos) en [Python](https://www.python.org/). 
Permite la descarga de archivos de `EPH's` y otros como la `canasta basica` y `adulto equivalente` , como asi también algunos calculos rápidos relacionados con las mismas

# Instalación

#### Prerequisitos
- [Python 2 o 3](https://www.python.org/)
- [pip o pip3](https://www.pypi.org/)
#### Instalando PyEPH

- Abra una terminal del sistema y escriba 

```bash
$ pip install pyeph
```

#### Puesta en marcha

Esta librería puede ser utilizada en el entorno de su preferencia. Puede utilizarse en una `jupyter-notebook` o en un archivo simple `.py`

[...]

# Uso básico

## Descargando bases de datos

> pyeph.get() o pyeph.obtener()

Todas las bases que se necesite descargar para su posterior tratamiento debe realizarse desde la funcion `pyeph.get()`. Esta función instancia la obtención de los datos solicitados.
Algunos ejemplos:

```python
import pyeph

eph = pyeph.get(data="eph", year=2021, period=2, base_type='individual') # microdatos
canastas = pyeph.get(data="canastas") # canasta basica total y alimentaria 
adequi = pyeph.get(data="adulto-equivalente") # adulto equivalente 
```

#### Parámetros

| Parametro | Tipo de dato | Descripción |
| --------- | ------------ | ----------- |
| data | str | Tipo de base de dato a obtener. Puede ser 'eph', 'canastas', 'adulto-equivalente' |
| year | int | (Solo para las EPH) El año que se desea solicitar |
| period | int | (Solo para las EPH) El periodo que se desea solicitar |
| freq | str | (Solo para las EPH) Tipo de periodizacion "trimestre" u "onda". Default: "trimestre" |
| base_type | str | (Solo para las EPH) Tipo de EPH que se desea obtener. Puede ser 'individual' u 'hogar' |



---
## Ejecutando calculos

> Todos los calculos precisan de una eph en formato pd.DataFrame, puede descargarla con pyeph.get() o ser una personalizada


### Pobreza

> pyeph.Poverty() o pyeph.Pobreza()

### Desempleo

> pyeph.Unemployment() o pyeph.Desempleo()

## Documentación

[Link del sitio de la documentación](https://github.com/) (Aún en desarrollo)

---

### Tenga en cuenta

Esta librería se encuentra en estado permanente de desarrollo.

> Cualquier colaboración es bienvenida


## Agradecimientos

- Agradecimientos para les pi de https://github.com/holatam/eph (docs: https://cran.r-project.org/web/packages/eph/eph.pdf)
- Humai
- Devs

Falta agregar MIT license