import pandas as pd

from pyeph.tools.decorators import (
    validate_group_by,
    translate_params
    )

from pyeph.get.basket import Basket
from pyeph.get.equivalent_adult import EquivalentAdult

from ..types import BasketType
from ..calculator import Calculator


class Poverty(Calculator):
    """
		Obtencion de tasa de pobreza e indigencia de hogar y de personas.
	"""

    # Constantes Pobreza
    VAR_EPH_ANO = 'ANO4'
    VAR_EPH_TRIM = 'TRIMESTRE'
    VAR_EPH_SEXO = 'CH04'
    VAR_EPH_EDAD = 'CH06'
    VAR_EPH_HOGAR = 'CODUSU'
    VAR_EPH_NRO_HOGAR = 'NRO_HOGAR'
    VAR_EPH_REGION = 'REGION'
    VAR_EPH_ITF = 'ITF'

    VAR_CBT = 'CBT'
    VAR_CBA = 'CBA'
    VAR_CBT_HOGAR = 'CBT_HOGAR'
    VAR_CBA_HOGAR = 'CBA_HOGAR'
    VAR_AE = 'adequi'
    VAR_AE_HOGAR = 'adequi_hogar'
    VAR_PERIODO = 'periodo'
    VAR_BASKET_COD = 'codigo'
    VAR_STATUS = 'situacion'
    VAR_INDICATOR = 'Indicador'
    VAR_POVERTY = 'Pobreza'
    VAR_INDIGENCE = 'Indigencia'

    # No cambiar el orden de la lista de status
    STATUS_OPTIONS = ['indigente', 'pobre', 'no pobre']

    basket = BasketType() # Salva de recibir algo != a pandas.DataFrame

    @translate_params({'canasta': 'basket'})
    def __init__(self, 
        eph: pd.DataFrame, 
        basket: pd.DataFrame=None
    ):
        self.eph = eph
        check_pond = [c for c in self.eph.columns if c == 'PONDIH']

        if len(check_pond):
            Poverty.VAR_EPH_PONDERADOR_INGRESO = 'PONDIH'

        else:
            Poverty.VAR_EPH_PONDERADOR_INGRESO = 'PONDERA'

        
        # En caso de que el usuario no especifique una canasta, se descarga la del repo.
        if basket is None:
            self.basket = Basket().get_df().copy()
        else:
            self.basket = self.prepare_basket(basket.copy())
        # Obtencion del archivo con los valores del adultx equivalente
        self.equivalent_adult = EquivalentAdult().get_df().copy()

    @classmethod
    def compute_status(cls, row):
        if row[cls.VAR_EPH_ITF] is None:
            return None
        if row[cls.VAR_EPH_ITF] < row[cls.VAR_CBA_HOGAR]:
            return cls.STATUS_OPTIONS[0]
        if row[cls.VAR_EPH_ITF] < row[cls.VAR_CBT_HOGAR]:
            return cls.STATUS_OPTIONS[1]
        return cls.STATUS_OPTIONS[2]

    @classmethod
    def get_pivot_df(cls, df, calc_type, drop_level=True):
        df = df[df.index.get_level_values(cls.VAR_STATUS).isin(cls.STATUS_OPTIONS[:2])].reset_index()
        df = df.rename(columns={cls.VAR_STATUS: cls.VAR_INDICATOR, cls.VAR_EPH_PONDERADOR_INGRESO: 'Valor'})
        new_name_poverty = '{} ({})'.format(cls.VAR_POVERTY, calc_type)
        new_name_indigence = '{} ({})'.format(cls.VAR_INDIGENCE, calc_type)
        df[cls.VAR_INDICATOR] = df[cls.VAR_INDICATOR].replace([cls.STATUS_OPTIONS[0], cls.STATUS_OPTIONS[1]],
                                                                [new_name_indigence, new_name_poverty])
        if len(cls.VAR_USER) >= 1 and drop_level:
            df = pd.pivot_table(df, index=cls.VAR_USER, columns=cls.VAR_INDICATOR).round(3)
            df.columns = df.columns.droplevel()
        else:
            df = pd.pivot_table(df, columns=cls.VAR_INDICATOR).round(3)
        df[new_name_poverty] = df[new_name_poverty] + df[new_name_indigence]
        return df

    def generate_base_df(self, eph, basket, equivalent_adult):
        # Agrega variable periodo a la base de eph
        eph = eph.reset_index().drop(columns="index")
        period = self.get_period(eph)
        eph.loc[:, (self.VAR_PERIODO)] = period
        # Se obtiene los valores de las canastas para el periodo especificado
        basket = basket[self.basket[self.VAR_PERIODO] == period]
        basket = basket.groupby(by=[self.VAR_PERIODO, self.VAR_BASKET_COD]).mean().reset_index()
        basket = basket.drop(columns={self.VAR_PERIODO})
        # Se mergea con los valores de la CBT y CBA para es período
        eph = eph.merge(basket, how="left", left_on=self.VAR_EPH_REGION, right_on=self.VAR_BASKET_COD)
        # Se mergea con la información del adultx equivalente
        eph = eph.merge(equivalent_adult, how="left", on=[self.VAR_EPH_SEXO, self.VAR_EPH_EDAD])
        # Calculo de la CBT y CBA por adultx equivalente hogar
        eph[self.VAR_AE_HOGAR] = eph.groupby([self.VAR_EPH_HOGAR, self.VAR_EPH_NRO_HOGAR, self.VAR_PERIODO])[
            self.VAR_AE].transform('sum')
        eph[self.VAR_CBT_HOGAR] = eph[self.VAR_CBT] * eph[self.VAR_AE_HOGAR]
        eph[self.VAR_CBA_HOGAR] = eph[self.VAR_CBA] * eph[self.VAR_AE_HOGAR]
        # Calculo de status (indigente, pobre, no pobre)
        eph[self.VAR_STATUS] = eph.apply(self.compute_status, axis=1)
        return eph

    @translate_params({'agrupar_por': "group_by"})
    @validate_group_by
    def population(self, group_by=[]):
        # Calculo de pobreza e indigencia (poblacion)
        eph = self.prepare_eph(self.eph, group_by)
        base_df = self.generate_base_df(eph, self.basket, self.equivalent_adult)
        population_rate = self.distribution(base_df, self.VAR_EPH_PONDERADOR_INGRESO,
                                            self.VAR_USER + [self.VAR_STATUS])
        population_rate = self.get_pivot_df(population_rate, '%')
        population_quantity = base_df.groupby(by=self.VAR_USER + [self.VAR_STATUS])[
            self.VAR_EPH_PONDERADOR_INGRESO].sum()
        population_quantity = self.get_pivot_df(population_quantity, '#')
        df = population_rate.join(population_quantity)
        df = df.sort_index(ascending=False, axis=1)
        return df
         

    def household(self):
        # Calculo de pobreza e indigencia (hogares)
        eph = self.prepare_eph(self.eph, [])
        base_df = self.generate_base_df(eph, self.basket, self.equivalent_adult)
        household_df = base_df.copy()
        household_df = household_df[
            [self.VAR_EPH_HOGAR, self.VAR_EPH_PONDERADOR_INGRESO, self.VAR_STATUS]].drop_duplicates()
        household_rate = self.distribution(household_df, self.VAR_EPH_PONDERADOR_INGRESO, [self.VAR_STATUS])
        household_rate = self.get_pivot_df(household_rate, '%', False)
        household_quantity = household_df.groupby(by=self.VAR_STATUS)[self.VAR_EPH_PONDERADOR_INGRESO].sum()
        household_quantity = self.get_pivot_df(household_quantity, '#', False)
        df = household_rate.join(household_quantity)
        df = df.sort_index(ascending=False, axis=1)
        return df

    # Traduccion
    poblacion = population
    hogares = household
# Traduccion
Pobreza = Poverty
