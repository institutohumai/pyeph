from pyeph.calc.dwelling import Dwelling
from pyeph.get import get
import pandas as pd
aglomerados = {32:'Ciudad de Buenos Aires', 33:'Partidos del GBA'}
def test_get_propietarios_aglomerado():
    eph = get(data="eph", year=2024, period=1, base_type='hogar')
    eph_ind = get(data="eph", year=2024, period=1, base_type='individual')
    dwelling = Dwelling(eph_ind, eph)
    dwelling.agregar_habitantes_hogar(column_name="HAB_HOG")
    print(dwelling.get_media_attr_hogar_by_tipo_prop("dormitorios", 32))
    print(dwelling.get_media_attr_hogar_individuo_by_tipo_prop("edad", 32))
    print(dwelling.get_media_attr_hogar_by_tipo_prop("HAB_HOG", 32))

test_get_propietarios_aglomerado()