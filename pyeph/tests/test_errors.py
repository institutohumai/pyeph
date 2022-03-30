import pytest

from pyeph import errors
from pyeph import ads
from pyeph.get.api import get


def test_period_freq():
    with pytest.raises(ValueError):
        get('microdata', 2015, 3, "onda")


@pytest.mark.parametrize(
    "year,period,freq", [
        (2002,2,"trimestre"),
        (2004,2,"onda"),
    ]
)
def test_year_freq(year, period, freq):
    with pytest.raises(ValueError) as excinfo:
        get('microdata', year, period, freq)
    assert ads.QUARTER_OR_WAVE_OPTION == excinfo.value.args[0]


@pytest.mark.parametrize(
    "year,period",[
        (2015,4),
        (2016,1),
    ]
)
def test_existent_db(year, period):
    with pytest.raises(errors.NonExistentDBError) as excinfo:
        get('microdata', year, period)
    assert ads.INDEC_STATS_EMERGENCY == excinfo.value.args[0]


def test_request_fruit():
    with pytest.raises(errors.NonExistentDBError) as excinfo:
        get('pepe-parrales', 2015, 2, "trimestre")
    assert "Debe seleccionar un tipo de base posible" in excinfo.value.args[0]