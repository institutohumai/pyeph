import pandas as pd
import sys

def merge(eph, modulo, report=True):

    _relevant = ['CODUSU', 'ANO4', 'TRIMESTRE', 'NRO_HOGAR', 'ANO_TRIM']

    if 'COMPONENTE' in eph.columns:
        _relevant.append('COMPONENTE')

    eph['ANO_TRIM'] = eph['ANO4'].astype(int).astype(str) + '-' + eph['TRIMESTRE'].astype(str)
    modulo['ANO_TRIM'] = modulo['ANO4'].astype(int).astype(str) + '-' + modulo['TRIMESTRE'].astype(str)

    _share = [c for c in modulo if c in eph]

    _drop = [c for c in _share if c not in _relevant]

    modulo = modulo.drop(columns = _drop)


    _periodos_eph = eph['ANO_TRIM'].unique()
    _periodos_modulo = modulo['ANO_TRIM'].unique()

    _periodos_faltantes = [c for c in _periodos_eph if c not in _periodos_modulo]

    if len(_periodos_faltantes)!=0:
        df = eph
        sys.stdout.write("No se encontró coincidencia para los siguientes periodos: {} \n".format(_periodos_faltantes))

    else:
        df = pd.merge(eph, modulo, how= 'left', on=_relevant)

    return df

# Traduccion
aparear = merge