# -*- coding: utf-8 -*-
"""
Tests para comparability_bridge() / puente_comparabilidad(). Réplica 1 a 1
de la suite de la implementación de referencia en R (ropensci/eph#70),
verificada además con un chequeo de equivalencia exhaustivo entre ambas.

No requieren red: usan bases sintéticas.
"""

import numpy as np
import pandas as pd
import pytest

from pyeph.tools.comparability import comparability_bridge, puente_comparabilidad


# --- Bases sinteticas ----------------------------------------------------------

def hogar_nueva():
    """
    Base hogar nueva metodologia (2025 T1), 7 hogares. Disenada para cubrir
    todas las ramas de las reglas: V11 (2 sub-componentes, dominancia
    1 > 2 > 0 > 9) y V5 (3 sub-componentes, reglas especiales).
    """
    return pd.DataFrame({
        'CODUSU': [f"H{i}" for i in range(1, 8)],
        'NRO_HOGAR': 1,
        'ANO4': 2025,
        'TRIMESTRE': 1,
        # V11: (1,9)->1  (2,0)->2  (0,9)->0  (9,9)->9  (2,2)->2  (1,1)->1  (0,0)->0
        'V11_01': [1, 2, 0, 9, 2, 1, 0],
        'V11_02': [9, 0, 9, 9, 2, 1, 0],
        # V5: (0,1,9)->1  (0,9,9)->9  (0,0,9)->0  (2,0,9)->2  (0,0,0)->0
        #     (2,2,2)->2  (1,0,0)->1
        'V5_01': [0, 0, 0, 2, 0, 2, 1],
        'V5_02': [1, 9, 0, 0, 0, 2, 0],
        'V5_03': [9, 9, 9, 9, 0, 2, 0],
        # V21 y V22 completos para que tambien se reconstruyan
        'V21_01': 0, 'V21_02': 0, 'V21_03': 0,
        'V22_01': 2, 'V22_02': 0, 'V22_03': 0,
        # Control de jubilaciones (V2 sigue existiendo en la base nueva):
        # el hogar 2 contesto No (2) -> controla la imputacion -7 de V2_M
        'V2': [1, 2, 1, 9, 1, 1, 1],
    })


def indiv_nueva():
    """
    Base individual apareada (1 persona por hogar; el individuo H9 no tiene
    hogar en la base hogar -> control NaN).
    """
    return pd.DataFrame({
        'CODUSU': [f"H{i}" for i in range(1, 8)] + ["H9"],
        'NRO_HOGAR': 1,
        'COMPONENTE': 1,
        'ANO4': 2025,
        'TRIMESTRE': 1,
        # V2_M, cubre las 6 prioridades + control:
        #   H1 (1000,-7,0)    -> 1000  (suma de no negativos)
        #   H2 (-7,-7,-7) c2  -> -7    (control hogar = No)
        #   H3 (0,0,0)        -> 0     (todos 0)
        #   H4 (-7,-9,-7) c9  -> -9    (incertidumbre)
        #   H5 (-7,-8,-7) c1  -> -8    (ingreso potencial)
        #   H6 (-7,-7,-7) c1  -> -7    (no aplicabilidad)
        #   H7 (0,-7,0)   c1  -> 0     (default)
        #   H9 (-7,-7,-7) cNaN-> -7    (sin hogar: salta el control, todos -7)
        'V2_01_M': [1000, -7, 0, -7, -7, -7, 0, -7],
        'V2_02_M': [-7, -7, 0, -9, -8, -7, -7, -7],
        'V2_03_M': [0, -7, 0, -7, -7, -7, 0, -7],
        # PP11L1/PP11L2 invertidas: PP11L2 registra 1/2/3 y PP11L1 no tiene 3
        'PP11L1': [1, 2, 1, 2, 1, 2, 1, 2],
        'PP11L2': [1, 2, 3, 1, 2, 3, 1, 2],
    })


# --- Base hogar ----------------------------------------------------------------

def test_reconstruye_agregados_hogar():
    h = comparability_bridge(hogar_nueva())
    assert h['V11'].tolist() == [1, 2, 0, 9, 2, 1, 0]
    assert h['V5'].tolist() == [1, 9, 0, 2, 0, 2, 1]
    assert 'V21' in h.columns and 'V22' in h.columns


def test_no_pisa_agregado_existente():
    h = hogar_nueva()
    h['V11'] = 5
    res = comparability_bridge(h)
    assert res['V11'].tolist() == [5] * 7


def test_omite_si_faltan_subcomponentes():
    h = hogar_nueva().drop(columns=['V5_03'])
    res = comparability_bridge(h)
    assert 'V5' not in res.columns
    assert 'V11' in res.columns


def test_no_modifica_la_base_de_entrada():
    h = hogar_nueva()
    columnas_antes = list(h.columns)
    comparability_bridge(h)
    assert list(h.columns) == columnas_antes


# --- Base individual -----------------------------------------------------------

def test_reconstruye_montos_con_control():
    i = comparability_bridge(indiv_nueva(), base_hogar=hogar_nueva())
    assert i['V2_M'].tolist() == [1000.0, -7.0, 0.0, -9.0, -8.0, -7.0, 0.0, -7.0]


def test_corrige_inversion_pp11l():
    i0 = indiv_nueva()
    i = comparability_bridge(i0, base_hogar=hogar_nueva())
    assert i['PP11L1'].tolist() == i0['PP11L2'].tolist()
    assert i['PP11L2'].tolist() == i0['PP11L1'].tolist()


def test_no_intercambia_sin_condicion_de_error():
    i0 = indiv_nueva()
    i0['PP11L1'] = [1, 2, 3, 1, 2, 3, 1, 2]  # PP11L1 si registra el nivel 3
    i = comparability_bridge(i0, base_hogar=hogar_nueva())
    assert i['PP11L1'].tolist() == i0['PP11L1'].tolist()


def test_exige_base_hogar_para_individual():
    with pytest.raises(ValueError, match="base_hogar"):
        comparability_bridge(indiv_nueva())


def test_rechaza_claves_duplicadas():
    h = pd.concat([hogar_nueva(), hogar_nueva().iloc[[0]]], ignore_index=True)
    with pytest.raises(ValueError, match="duplicadas"):
        comparability_bridge(indiv_nueva(), base_hogar=h)


def test_rechaza_periodos_distintos():
    h = hogar_nueva()
    h['TRIMESTRE'] = 2
    with pytest.raises(ValueError, match="periodo"):
        comparability_bridge(indiv_nueva(), base_hogar=h)


# --- Era y validaciones ---------------------------------------------------------

def test_devuelve_sin_cambios_las_bases_legacy():
    h = hogar_nueva()
    h['ANO4'] = 2023
    res = comparability_bridge(h)
    pd.testing.assert_frame_equal(res, h)


def test_rechaza_mezcla_de_eras():
    h = hogar_nueva()
    h['ANO4'] = [2023] + [2025] * 6
    with pytest.raises(ValueError, match="combina periodos"):
        comparability_bridge(h)


def test_valida_tipo_de_base():
    with pytest.raises(ValueError, match="DataFrame"):
        comparability_bridge("no_soy_un_dataframe")


def test_alias_en_castellano():
    assert puente_comparabilidad is comparability_bridge
