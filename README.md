# PyEPH - Libreria para el procesamiento de la Encuesta Permanente de Hogares en Python

<a><img src='docs/_static/logo.png' align="right" height="250" /></a>

![PyPI](https://img.shields.io/pypi/v/pyeph?color=orange&)
![PyPI - License](https://img.shields.io/pypi/l/pyeph?color=purple&)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyeph?)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pyeph?)
[![Downloads](https://static.pepy.tech/personalized-badge/pyeph?period=total&units=none&left_color=grey&right_color=yellowgreen&left_text=downloads)](https://pepy.tech/project/pyeph)
[![Documentation Status](https://readthedocs.org/projects/pyeph/badge/?version=latest)](https://pyeph.readthedocs.io/es/latest/?badge=latest)
[![DOI](https://zenodo.org/badge/461306367.svg)](https://zenodo.org/badge/latestdoi/461306367)

La librería Pyeph tiene como objetivo facilitar el procesamiento en Python de las [Encuesta Permanente de Hogares (eph)](https://www.indec.gob.ar/indec/web/Institucional-Indec-BasesDeDatos) publicadas por INDEC de forma periódica. Está pensada como un espacio donde se nuclean y centralizan los cálculos vinculados a las mismas para posteriormente ser utilizadas en investigaciones, artículos, publicaciones, etc.
Es una librería que hace principal hincapié en la transparencia metodológica utilizando licencias de código abierto y que promueve la colaboración de las comunidades de cientístas de datos, sociales, investigadorxs, desarrolladorxs, periodistas y demás curiosxs.

Permite la descarga de archivos de `EPH's` y otros como la `canasta basica` y `adulto equivalente` , como asi también algunos calculos rápidos relacionados con las mismas

> #### 👷‍♀️ Cómo colaborar
>
> **¡Las contribuciones son bienvenidas!** Si estás interesado en mejorar la librería o agregar nuevas funcionalidades o cálculos, por favor revisa nuestra [guía de contribución](.github/CONTRIBUTING.md) para obtener más información.

## Cómo citar la librería

```
Carolina Trogliero, Mariano Valdez y Maria Frances Gaska (2022). PyEPH: Librería para la obtención y el procesamiento de la Encuesta Permanente de Hogares (EPH-INDEC). PyEPH version https://doi.org/10.5281/zenodo.6727908
```

## Instalación

Pueden probar nuestra notebook de ejemplo en Google Colab

<a href="https://colab.research.google.com/github/institutohumai/pyeph/blob/main/examples.ipynb" target="_blank"> <img src='https://colab.research.google.com/assets/colab-badge.svg' /> </a>

Recordá abrir en una nueva pestaña

### Prerequisitos

- [Python 3](https://www.python.org/)
- [pip](https://www.pypi.org/)

### Instalando PyEPH

- Abra una terminal del sistema y escriba

```bash
$ pip install pyeph
```

## Uso básico

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

## Documentación

[Link del sitio de la documentación](https://pyeph.readthedocs.io/es/latest/)

---

## Agradecimientos

Dejamos aquí un especial agradecimiento al equipo de desarrollo de la librería [EPH en R](https://holatam.github.io/eph/authors.html). Todo el amor para elles ❤️ y a [Rami Argañaraz](https://www.linkedin.com/in/ramiro-arga%C3%B1araz-57764a16b/) por armarnos el loguito 😻

---

⌨️ con ❤️
