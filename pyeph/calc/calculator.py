from pyeph.get.basket import Basket

from .types import EPHType

class Calculator:
	"""
		Metodos genericos para la utilizacion en mas de un calculo
	"""

	# Constantes Canastas
	BASKET_COLUMNS = ['periodo', 'region', 'CBA', 'CBT', 'codigo']

	eph = EPHType() # Salva de recibir algo != a pandas.DataFrame

	@classmethod
	def prepare_eph(cls, eph, group_by):
		# Variables fundamentales de la EPH
		VAR_FUNDAMENTALS = cls.get_fundamentals()
		if isinstance(group_by, str):
			group_by = [group_by]
		cls.VAR_USER = group_by
		# Filtro de eph para trabajar sobre un df mas pequeño
		VAR_KEEP = VAR_FUNDAMENTALS + cls.VAR_USER
		VAR_KEEP = list(set(VAR_KEEP))
		result = eph[VAR_KEEP].copy()
		return result

	@classmethod
	def prepare_basket(cls, basket):
		if not all(c in basket.columns for c in cls.BASKET_COLUMNS):
			basket = Basket.prepare_basket(basket)
		return basket

	@classmethod
	def info(cls): pass

	@classmethod
	def help(cls): return cls.__doc__.strip()

	@classmethod
	def get_fundamentals(cls):
		return [v for k, v in cls.__dict__.items() if 'VAR_EPH_' in k]

	@classmethod
	def distribution(cls, df, weight_var, values_var):
		df = df.copy()
		if not isinstance(values_var, list):
			values_var = [values_var]
		if len(values_var)>1:
			weights = df.groupby(values_var)[weight_var].sum()
			total_weight = weights.groupby(values_var[:-1]).sum()
			return weights.div(total_weight, axis = 'index')
		values_var = values_var[0]
		weights = df[weight_var]
		total_weight = weights.sum()
		# para el test: check.groupby(values_var[:-1]).sum() == 1.0
		return df.groupby(values_var)[weight_var].sum() / total_weight

	@classmethod
	def get_period(cls, df):
		year = str(df[cls.VAR_EPH_ANO].drop_duplicates()[0])
		trimester = str(df[cls.VAR_EPH_TRIM].drop_duplicates()[0])
		return '.'.join([year,trimester])

# Traduccion
Calculadora = Calculator