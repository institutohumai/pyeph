# -*- coding: utf-8 -*-
"""
Puente de comparabilidad para las bases de la EPH posteriores al rediseño
2024.

A partir del cuarto trimestre de 2024, el rediseño del cuestionario de la
EPH eliminó de las bases usuarias varias variables agregadas y publicó en su
lugar sub-componentes por fuente. Este módulo reconstruye las variables
eliminadas con reglas determinísticas, para mantener la comparabilidad con
la serie histórica.

Referencias
-----------
- Tessmer, G. y Boggiano, B. (2026). "From Breaks to Bridges: An
  Architecture for Survey Redesigns That Expand Conceptual Scope". SSRN
  Working Paper 6597399.
- Observatorio Económico Social UNR. "Manual Metodológico EPH –
  Observatorio", Parte A. https://hdl.handle.net/2133/33253
  (datasets: https://doi.org/10.57715/UNR/BL85Z8).
- Implementación de referencia en R propuesta al paquete `eph` de rOpenSci:
  https://github.com/ropensci/eph/issues/70
"""

import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

# Variables agregadas de la base HOGAR (estrategias del hogar, sí/no) y sus
# sub-componentes por fuente.
RELACIONES_HOGAR = {
    'V11': ['V11_01', 'V11_02'],
    'V21': ['V21_01', 'V21_02', 'V21_03'],
    'V22': ['V22_01', 'V22_02', 'V22_03'],
    'V5':  ['V5_01', 'V5_02', 'V5_03'],
}

# Variables agregadas de la base INDIVIDUAL (montos de ingresos no
# laborales) y sus sub-componentes.
RELACIONES_INDIVIDUAL = {
    'V11_M': ['V11_01_M', 'V11_02_M'],
    'V2_M':  ['V2_01_M', 'V2_02_M', 'V2_03_M'],
    'V21_M': ['V21_01_M', 'V21_02_M', 'V21_03_M'],
    'V22_M': ['V22_01_M', 'V22_02_M', 'V22_03_M'],
    'V5_M':  ['V5_01_M', 'V5_02_M', 'V5_03_M'],
}

# Variable de la base hogar que controla la reconstrucción de cada monto.
CONTROLES = {
    'V11_M': 'V11', 'V2_M': 'V2', 'V21_M': 'V21',
    'V22_M': 'V22', 'V5_M': 'V5',
}

# Primer período de la nueva metodología: 2024 trimestre 4.
_PERIODO_NUEVA = 2024 * 100 + 4


def comparability_bridge(base, base_hogar=None):
    """
    Reconstruye las variables agregadas eliminadas por el rediseño 2024.

    En la base hogar reconstruye las estrategias del hogar (V5, V11, V21 y
    V22) a partir de sus sub-componentes. En la base individual corrige la
    inversión PP11L1/PP11L2 (si detecta la condición de error) y reconstruye
    los montos de ingresos no laborales (V2_M, V5_M, V11_M, V21_M y V22_M)
    usando como control la variable de estrategia correspondiente de la base
    hogar, apareada por CODUSU + NRO_HOGAR.

    Las bases anteriores a 2024 T4 no requieren puente y se devuelven sin
    cambios. Si una variable agregada ya existe, o faltan sus
    sub-componentes, su reconstrucción se omite con un aviso. Las variables
    reconstruidas se agregan al final; ningún valor existente se modifica
    (única excepción: el intercambio PP11L1/PP11L2 cuando corresponde).

    Parameters
    ----------
    base : pandas.DataFrame
        Base usuaria de la EPH (hogar o individual), tal como la devuelve
        ``pyeph.get(data="eph", ...)``. El tipo se detecta por la presencia
        de la columna COMPONENTE.
    base_hogar : pandas.DataFrame, optional
        Base hogar del mismo trimestre. Obligatoria cuando ``base`` es una
        base individual (aporta las variables control; si sus agregados
        faltan, se reconstruyen internamente). Se ignora cuando ``base`` ya
        es una base de hogar.

    Returns
    -------
    pandas.DataFrame
        Copia de ``base`` con las variables reconstruidas agregadas.

    Examples
    --------
    >>> hogares = pyeph.get(data="eph", year=2025, period=1, base_type="hogar")
    >>> individuos = pyeph.get(data="eph", year=2025, period=1, base_type="individual")
    >>> hogares = comparability_bridge(hogares)
    >>> individuos = comparability_bridge(individuos, base_hogar=hogares)
    """
    if not isinstance(base, pd.DataFrame):
        raise ValueError("base debe ser un pandas.DataFrame (base usuaria de hogar o individual)")

    faltan = [c for c in ('ANO4', 'TRIMESTRE') if c not in base.columns]
    if faltan:
        raise ValueError(
            f"La base no contiene la(s) columna(s) {faltan}, necesarias para determinar el periodo"
        )

    # El puente aplica solo a las bases de la nueva metodologia (>= 2024 T4)
    if _era(base) == 'legacy':
        logger.info(
            "Base anterior al cambio metodologico (2024 T4): no requiere puente. "
            "Se devuelve sin cambios."
        )
        return base.copy()

    es_individual = 'COMPONENTE' in base.columns

    # ---- Base HOGAR ---------------------------------------------------------
    if not es_individual:
        if base_hogar is not None:
            logger.warning("base_hogar se ignora: base ya es una base de hogar.")
        return _puente_hogar(base.copy())

    # ---- Base INDIVIDUAL ----------------------------------------------------
    if base_hogar is None:
        raise ValueError(
            "Para una base individual se requiere base_hogar (la base hogar del "
            "mismo trimestre): las variables control de la reconstruccion "
            "(V2, V5, V11, V21, V22) provienen de la base de hogar"
        )
    if not isinstance(base_hogar, pd.DataFrame) or 'COMPONENTE' in base_hogar.columns:
        raise ValueError(
            "base_hogar no parece una base de hogar: debe ser un pandas.DataFrame "
            "sin la columna COMPONENTE"
        )
    per_indiv = _periodos(base)
    per_hogar = _periodos(base_hogar)
    if per_indiv != per_hogar:
        raise ValueError(
            f"base ({per_indiv}) y base_hogar ({per_hogar}) no pertenecen al mismo periodo"
        )

    df = base.copy()

    # Correccion PP11L1/PP11L2: en las bases publicadas los contenidos de
    # ambas columnas aparecen intercambiados. Condicion de error: PP11L2
    # registra los niveles 1/2/3 (que corresponden a la PP11L1 del
    # cuestionario legacy) y PP11L1 nunca registra el nivel 3.
    if {'PP11L1', 'PP11L2'}.issubset(df.columns):
        pp11l1 = pd.to_numeric(df['PP11L1'], errors='coerce')
        pp11l2 = pd.to_numeric(df['PP11L2'], errors='coerce')
        if {1, 2, 3}.issubset(set(pp11l2.dropna().unique())) and 3 not in set(pp11l1.dropna().unique()):
            logger.info("Se detecto la inversion PP11L1/PP11L2: se intercambian ambas columnas.")
            df[['PP11L1', 'PP11L2']] = df[['PP11L2', 'PP11L1']].to_numpy()

    # Variables control: si a la base hogar le faltan los agregados, se
    # reconstruyen aca (solo para uso interno; base_hogar no se devuelve).
    hogar = _puente_hogar(base_hogar.copy(), avisar=False)

    if hogar.duplicated(subset=['CODUSU', 'NRO_HOGAR']).any():
        raise ValueError(
            "base_hogar tiene combinaciones CODUSU + NRO_HOGAR duplicadas: "
            "no es posible asignar los controles del hogar"
        )

    creadas = []
    for dependiente, independientes in RELACIONES_INDIVIDUAL.items():
        control_var = CONTROLES[dependiente]
        if (
            dependiente not in df.columns
            and all(c in df.columns for c in independientes)
            and control_var in hogar.columns
        ):
            m = df[independientes].apply(pd.to_numeric, errors='coerce').to_numpy(dtype=float)
            ctrl = _control_del_hogar(df, hogar, control_var)
            df[dependiente] = [
                _reconstruye_ingreso(m[i, :], ctrl[i]) for i in range(len(df))
            ]
            creadas.append(dependiente)
        else:
            logger.info(
                "Se omite '%s': ya existe, faltan sus variables de origen o falta "
                "la variable control %s en base_hogar.", dependiente, control_var
            )
    if creadas:
        logger.info("Variables reconstruidas en la base individual: %s", ", ".join(creadas))

    return df


# ------------------------------------------------------------------------------
# Auxiliares internos
# ------------------------------------------------------------------------------

def _puente_hogar(df, avisar=True):
    """Reconstruye los agregados sí/no de una base hogar."""
    creadas = []
    for dependiente, independientes in RELACIONES_HOGAR.items():
        if dependiente not in df.columns and all(c in df.columns for c in independientes):
            m = df[independientes].apply(pd.to_numeric, errors='coerce').to_numpy(dtype=float)
            valores = [_calcula_dependiente(m[i, :]) for i in range(len(df))]
            df[dependiente] = pd.array(valores, dtype='Int64')
            creadas.append(dependiente)
        elif avisar:
            logger.info(
                "Se omite '%s': ya existe o faltan sus variables de origen.", dependiente
            )
    if avisar and creadas:
        logger.info("Variables reconstruidas en la base de hogar: %s", ", ".join(creadas))
    return df


def _calcula_dependiente(valores):
    """
    Agregado sí/no a partir de los sub-componentes de una fila.
    Códigos: 1 = Sí, 2 = No, 0 = No corresponde, 9 = Ns/Nr.
    Lógica idéntica al pipeline EPH-Observatorio (02.check.R, sección 3.1).
    """
    valores = np.asarray(valores, dtype=float)

    # 2 sub-componentes: regla de dominancia transitiva 1 > 2 > 0 > 9
    if len(valores) == 2:
        # Valores fuera de {1, 2, 0, 9} (o faltantes) -> sin dato, como en la
        # implementacion de referencia en R.
        if not np.isin(valores, (1.0, 2.0, 0.0, 9.0)).all():
            return None
        for nivel in (1, 2, 0, 9):
            if nivel in valores:
                return nivel
        return None  # pragma: no cover

    # 3 sub-componentes: reglas especiales sobre la dominancia estricta
    if len(valores) == 3:
        # Prioridad 1: al menos un 1 (Si) -> 1
        if (valores == 1).any():
            return 1
        # Prioridad 2: solo hay 0 (No corresponde) y 9 (Ns/Nr)
        if np.isin(valores, (0.0, 9.0)).all():
            # dos o mas 9 -> 9; un solo 9 (o ninguno) -> 0
            return 9 if (valores == 9).sum() >= 2 else 0
        # Prioridad 3 (default): 2 (No)
        return 2

    raise ValueError("La reconstruccion solo esta definida para 2 o 3 sub-componentes")


def _reconstruye_ingreso(valores, valor_control):
    """
    Monto agregado a partir de los sub-componentes de una fila y el valor de
    la variable control del hogar. Códigos negativos de INDEC: -7 = no
    corresponde, -8 = no tuvo ingresos ese mes, -9 = Ns/Nr.
    Lógica idéntica al pipeline EPH-Observatorio (02.check.R, sección 3.2).
    """
    valores = np.asarray(valores, dtype=float)
    validos = valores[~np.isnan(valores)]

    # Prioridad absoluta: hay ingresos positivos -> suma de los no negativos
    if (validos > 0).any():
        return float(validos[validos >= 0].sum())
    # Prioridad 1: todos los sub-componentes en 0 -> 0
    if (validos == 0).all():
        return 0.0
    # Prioridad 2: el hogar contesto [2 = No] a la fuente correspondiente -> -7
    if not np.isnan(valor_control) and valor_control == 2:
        return -7.0
    # Prioridad 3: incertidumbre; algun -9 -> el total no puede determinarse
    if (validos == -9).any():
        return -9.0
    # Prioridad 4: ingreso potencial; sin -9 pero con algun -8 -> -8
    if (validos == -8).any():
        return -8.0
    # Prioridad 5: no aplicabilidad; solo quedan -7 -> -7
    if (validos == -7).all():
        return -7.0
    # Prioridad 6 (default): cero explicito
    return 0.0


def _control_del_hogar(df, hogar, control_var):
    """
    Devuelve, para cada fila de la base individual, el valor de la variable
    control de su hogar (apareo por CODUSU + NRO_HOGAR; NaN si el individuo
    no tiene hogar en la base de hogar).
    """
    apareo = df[['CODUSU', 'NRO_HOGAR']].merge(
        hogar[['CODUSU', 'NRO_HOGAR', control_var]],
        on=['CODUSU', 'NRO_HOGAR'],
        how='left',
    )
    sin_hogar = int(apareo[control_var].isna().sum())
    ctrl = pd.to_numeric(apareo[control_var], errors='coerce').to_numpy(dtype=float)
    if sin_hogar and np.isnan(ctrl).sum() == sin_hogar:
        logger.info(
            "%d individuo(s) sin hogar correspondiente en base_hogar: su control queda NaN.",
            sin_hogar,
        )
    return ctrl


def _era(base):
    """
    Clasifica la base en 'legacy' (< 2024 T4) o 'nueva' (>= 2024 T4).
    Lanza ValueError si la base mezcla períodos de ambas metodologías.
    """
    anio = pd.to_numeric(base['ANO4'], errors='coerce')
    trim = pd.to_numeric(base['TRIMESTRE'], errors='coerce')
    periodos = (anio * 100 + trim).dropna().unique()
    if len(periodos) == 0:
        raise ValueError("No se pudo determinar el periodo: ANO4/TRIMESTRE sin datos validos")
    nueva = periodos >= _PERIODO_NUEVA
    if nueva.all():
        return 'nueva'
    if not nueva.any():
        return 'legacy'
    raise ValueError(
        "La base combina periodos anteriores y posteriores al cambio metodologico "
        "(2024 T4). Separe los periodos y aplique la funcion solo a los trimestres "
        "de la nueva metodologia"
    )


def _periodos(base):
    """Etiquetas de período de una base, ordenadas (p. ej. '2025-T1')."""
    anio = pd.to_numeric(base['ANO4'], errors='coerce')
    trim = pd.to_numeric(base['TRIMESTRE'], errors='coerce')
    etiquetas = sorted(
        f"{int(a)}-T{int(t)}" for a, t in set(zip(anio, trim))
        if not (np.isnan(a) or np.isnan(t))
    )
    return ", ".join(etiquetas)


# Traduccion
puente_comparabilidad = comparability_bridge
