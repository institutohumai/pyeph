import pandas as pd

def merge(eph, modulo, report=True):

    _relevant = ['CODUSU', 'ANO4', 'TRIMESTRE', 'NRO_HOGAR']

    if 'COMPONENTE' in eph.columns:
        _relevant.append('COMPONENTE')

    _share = [c for c in modulo if c in eph]

    _drop = [c for c in _share if c not in _relevant]

    modulo = modulo.drop(columns = _drop)

    df = pd.merge(eph, modulo, how= 'left', on=_relevant)

    return df

# Traduccion
aparear = merge