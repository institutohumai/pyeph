# PyEPH - Python library for processing Argentina's Permanent Household Survey (EPH) data

<a><img src='docs/_static/logo.png' align="right" height="250" /></a>

![PyPI](https://img.shields.io/pypi/v/pyeph?color=orange&)
![PyPI - License](https://img.shields.io/pypi/l/pyeph?color=purple&)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyeph?)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pyeph?)
[![Downloads](https://static.pepy.tech/personalized-badge/pyeph?period=total&units=none&left_color=grey&right_color=yellowgreen&left_text=downloads)](https://pepy.tech/project/pyeph)
[![Documentation Status](https://readthedocs.org/projects/pyeph/badge/?version=latest)](https://pyeph.readthedocs.io/es/latest/?badge=latest)
[![DOI](https://zenodo.org/badge/461306367.svg)](https://zenodo.org/badge/latestdoi/461306367)

The Pyeph library aims to facilitate Python-based processing of the [Permanent Household Survey (EPH)](https://www.indec.gob.ar/indec/web/Institucional-Indec-BasesDeDatos) periodically published by INDEC. It is designed as a centralized space that consolidates calculations related to these surveys for subsequent use in research, articles, publications, etc.

This library emphasizes methodological transparency through open-source licensing and promotes collaboration among communities of data scientists, social scientists, researchers, developers, journalists, and other curious minds.

It enables downloading `EPH` files as well as other datasets like the basic food `basket` and `adult equivalent` measurements, along with providing quick calculations related to them.

> #### 👷‍♀️ How to Contribute
>
> **Contributions are welcome!** If you're interested in improving the library or adding new features and calculations, please check out our [contribution guidelines]((.github/CONTRIBUTING.md)) for details.

## How to Cite the Library

```
Carolina Trogliero, Mariano Valdez, and Maria Frances Gaska (2022). PyEPH: A Python Library for Processing Argentina's Permanent Household Survey (EPH-INDEC). PyEPH version https://doi.org/10.5281/zenodo.6727908
```

## Installation

Try our example notebook on Google Colab:

<a href="https://colab.research.google.com/github/institutohumai/pyeph/blob/main/examples.ipynb" target="_blank"> <img src='https://colab.research.google.com/assets/colab-badge.svg' /> </a>

Recordá abrir en una nueva pestaña

### Prerequisites

- [Python 3](https://www.python.org/)
- [pip](https://www.pypi.org/)

### Installing PyEPH

- Run in your system terminal:

```bash
$ pip install pyeph
```

## Basic Usage


Below are some examples. For full documentation, see the links at the bottom.



- Data Retrieval

```python
import pyeph

# Obtención
eph = pyeph.get(data="eph", year=2021, period=2, base_type='individual') # EPH individual
basket = pyeph.get(data="basket") # Total and food basic baskets
equivalent_adult = pyeph.get(data="equivalent-adult") 

```

- Poverty Calculations


```python
poverty = pyeph.Poverty(eph, basket)
population_poverty = poverty.population(group_by='CH04') # Poverty by gender
labeled_poverty = pyeph.map_labels(population_poverty) # Labeled variables

```

- Labor Market Calculations


```python
labor_market = pyeph.LaborMarket(eph)
unemployment = labor_market.unemployment(group_by="REGION", div_by="PT") # Unemployment by region (vs. total population)
labeled_unemployment = pyeph.map_labels(unemployment) # Labeled variables

```

## Documentation

[Documentation in English](https://pyeph.readthedocs.io/en/latest/)

 

---
> 🙌 Special thanks to the development [team behind the R EPH library](https://holatam.github.io/eph/authors.html). 




⌨️ whit ❤️
