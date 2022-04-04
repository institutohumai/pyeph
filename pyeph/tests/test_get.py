import pytest
import pandas as pd

from datetime import date

from pyeph.get.api import get, obtener

parametters = pytest.mark.parametrize(
    "year,period", [
        (2016,2),
        (2017,2),
        (2018,2),
        (2019,2),
        (2020,2),
    ]
)

@parametters
def test_get(year, period):
    expected = get('microdata', year, period)
    assert isinstance(expected, pd.DataFrame)

@pytest.mark.parametrize(
    "ano,periodo", [
        (2016,2),
        (2017,2),
        (2018,2),
        (2019,2),
        (2020,2),
    ]
)
def test_obtener(ano, periodo):
    expected = obtener('microdata', ano, periodo)
    assert isinstance(expected, pd.DataFrame)

@pytest.mark.parametrize(
    "data,kwargs", [
        ('basket', {}),
        ('canastas', {}),
        ('adulto-equivalente', {}),
        ('equivalent-adult', {}),
        ('mautic', {"year": 2018, "period": 4, "base_type": "individual"}),
    ]
)
def test_others(data, kwargs):
    expected = get(data, **kwargs)
    assert isinstance(expected, pd.DataFrame)

# def test_all():
#     year_range = range(2015, date.today().year)
#     freqs = ["onda", "trimestre"]
#     periods = [1,2,3,4]
#     bases_types = ["individual", "hogar"]
#     for y in year_range:
#         for f in freqs:
#             for p in periods:
#                 for b in bases_types:
#                     if (
#                         (f == "onda" and p > 2) or
#                         (y <= 2003 and f != "onda") or
#                         (y >= 2004 and f != "trimestre") or
#                         (y == 2007 and p==3) or 
#                         ((y == 2015 and p in [3,4]) or (y==2016 and p==1))
#                         # Escribir todas las condiciones para que no compare si es df
#                     ):
#                         with pytest.raises(Exception):
#                             get("eph", year=y, period=p, freq=f, base_type=b)
#                     else:
#                         expected = get("eph", year=y, period=p, freq=f, base_type=b)
#                         assert isinstance(expected, pd.DataFrame)