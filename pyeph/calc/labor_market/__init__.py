import pandas as pd

from pyeph.tools.decorators import (
	translate_params,
	validate_group_by,
	validate_div_by
)

from ..calculator import Calculator


class LaborMarket(Calculator):
	"""
		Obtencion de la tasa de desempleo
	"""
	
	# Constantes Desempleo
	VAR_EPH_ANO = 'ANO4'
	VAR_EPH_TRIM = 'TRIMESTRE'
	VAR_EPH_EDAD = 'CH06'
	VAR_EPH_PONDERADOR = 'PONDERA'
	VAR_EPH_ESTADO = 'ESTADO'

	def __init__(self, 
		eph: pd.DataFrame
	):
		self.eph = eph
		
	@classmethod
	def get_pt_pet(cls, eph, div_by):
		if div_by == "PET":
			return eph[eph[cls.VAR_EPH_EDAD]>=14]
		return eph

	def calculate_grouped_indicator(self, df_denominator, df_numerator, indicator_name):
			denominator = df_denominator.groupby(self.VAR_USER).sum()[[self.VAR_EPH_PONDERADOR]]
			denominator = denominator.rename(columns = {self.VAR_EPH_PONDERADOR: 'DENOMINATOR'} )
			numerator = df_numerator.groupby(self.VAR_USER).sum()[[self.VAR_EPH_PONDERADOR]]
			numerator = numerator.rename(columns = {self.VAR_EPH_PONDERADOR: 'NUMERATOR'} )
			df = pd.merge(numerator, denominator, on = self.VAR_USER)
			df[indicator_name] = ((df['NUMERATOR']/df['DENOMINATOR'])*100).round(1)
			return df
	
	def calculate_indicator(self, df_denominator, df_numerator, indicator_name):
			denominador = df_denominator[self.VAR_EPH_PONDERADOR].sum()
			ocupades = df_numerator[self.VAR_EPH_PONDERADOR].sum()
			tasa = ((ocupades/denominador)*100).round(1)
			_data = {indicator_name:[tasa]}
			df = pd.DataFrame(data = _data)
			return df

	def generate_final_df(self, denominator, numerator,  indicator_name):
		if len(self.VAR_USER):
			df = self.calculate_grouped_indicator( denominator, numerator,  indicator_name)
		else: 
			df = self.calculate_indicator( denominator, numerator,  indicator_name)
		return df[[indicator_name]]
 		

	@translate_params({'agrupar_por': 'group_by', 'div_por': 'div_by'})
	@validate_group_by
	@validate_div_by
	def unemployment(self, group_by=[], div_by="PET"):
		_indicator_unemp_name = 'Tasa de Desempleo'
		base_df = self.prepare_eph(self.eph, group_by)
		# Obtencion del denominador
		unemployment_df = self.get_pt_pet(base_df, div_by).copy()
		# Obtiene poblacion economicamente activa (PEA)
		pea = unemployment_df[(unemployment_df[self.VAR_EPH_ESTADO]==1) | (unemployment_df[self.VAR_EPH_ESTADO]==2)]
		desocupades = unemployment_df[unemployment_df[self.VAR_EPH_ESTADO]==2]
		return self.generate_final_df(pea, desocupades,  _indicator_unemp_name)

	@translate_params({'agrupar_por': 'group_by', 'div_por': 'div_by'})
	@validate_group_by
	@validate_div_by
	def employment(self, group_by=[], div_by="PT"):
		_indicator_emp_name = 'Tasa de Empleo'
		base_df = self.prepare_eph(self.eph, group_by)
		# Obtiene poblacion total (PT)
		employment_df = self.get_pt_pet(base_df, div_by).copy()
		ocupades = employment_df[employment_df[self.VAR_EPH_ESTADO]==1]
		return self.generate_final_df(employment_df, ocupades, _indicator_emp_name)

	@translate_params({'agrupar_por': 'group_by', 'div_por': 'div_by'})
	@validate_group_by
	@validate_div_by
	def activity(self, group_by=[], div_by="PT"):
		_indicator_act_name = 'Tasa de Actividad'
		base_df = self.prepare_eph(self.eph, group_by)
		activity_df = self.get_pt_pet(base_df, div_by).copy()
		pea = activity_df[(activity_df[self.VAR_EPH_ESTADO]==1) | (activity_df[self.VAR_EPH_ESTADO]==2)]
		return self.generate_final_df(activity_df, pea,  _indicator_act_name)


	# Traduccion
	desempleo = unemployment
	empleo = employment
	actividad = activity
# Traduccion
MercadoLaboral = LaborMarket