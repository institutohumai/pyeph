import pytest
import pandas as pd

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

