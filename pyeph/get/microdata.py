import sys
import logging
from datetime import date

import pandas as pd

logger = logging.getLogger(__name__)

from pyeph.tools.decorators import translate_params
from pyeph.tools.labels import vars_labels

from ._base_getter import Getter

from pyeph.errors import *
from pyeph.ads import (
	INDEC_2007_2015,
	INDEC_2007_3,
	INDEC_STATS_EMERGENCY,
	QUARTER_OR_WAVE_OPTION
)


class BaseType:

	VALUES = ['individual','hogar']

	def __get__(self, obj, *args):
		return self.value

	def __set__(self, obj, value):
		if not (isinstance(value,str) and value in self.VALUES):
			raise ValueError("Por favor ingresa un tipo de base valido: " + ", ".join(self.VALUES))
		self.value = value

class Frequency:

	VALUES = {
        'trimestre': 4,
        'onda': 2
    }

	def __get__(self, obj, *args):
		return self.value

	def __set__(self, obj, value):
		if not (isinstance(value,str) and value in self.VALUES):
			raise ValueError("Por favor ingresa un tipo de base valido: " + ", ".join(self.VALUES.keys()))
		self.value = value

class Period:

	VALUES = [1,2,3,4]

	def __get__(self, obj, *args):
		return self.value

	def __set__(self, obj, value):
		if not (
			(isinstance(value,int) and value in self.VALUES) or
			value is None
		):
			raise ValueError("Por favor ingresa un numero de trimeste valido: " + ",".join(map(str, self.VALUES)))
		self.value = value

class Year:
	def __get__(self, obj, *args):
		return self.value

	def __set__(self, obj, value):
		current_year = date.today().year
		if not (isinstance(value,int) and value <= current_year):
			raise ValueError("El año debe ser un número menor o igual a {}.".format(current_year))
		self.value = value


class MicroDataValidator:
	"""
		Validacion de datos para la consulta de las bases
	"""

	def __init__(self):
		self.handle_exceptions_warnings()

	def valid_period_freq(self):
		if self.period > Frequency.VALUES[self.freq]:
			raise ValueError("La frecuencia solicitada ({}) requiere un periodo menor o igual a {}".format(self.freq, Frequency.VALUES[self.freq]))

	def valid_year_freq(self):
		if self.year <= 2003 and self.freq != 'onda': 
			raise ValueError(QUARTER_OR_WAVE_OPTION)
		if self.year >= 2004 and self.freq != 'trimestre': 
			raise ValueError(QUARTER_OR_WAVE_OPTION)			

	def valid_existent_db(self):
		if self.year==2007 and self.period==3:
			raise NonExistentDBError(INDEC_2007_3)

		if (self.year == 2015 and self.period in [3,4]) or (self.year==2016 and self.period==1):
			raise NonExistentDBError(INDEC_STATS_EMERGENCY)

		if self.year >= 2007 and self.year <= 2015:
			logger.warning(INDEC_2007_2015)
			
	def handle_exceptions_warnings(self):
		self.valid_period_freq()
		self.valid_year_freq()
		self.valid_existent_db()


class MicroData(Getter, MicroDataValidator):
	"""
	Obtencion del df de la eph solicitada

    Parametros
    ----------
        year : str
            año de la eph
        freq : str
            tipo de frecuencia "trimestral" u "onda" 
        period : list
            periodo que se desea consultar
		base_type : str, optional
			tipo de base a solicitar "individual", "hogar"
	"""
	
	year = Year()
	period = Period()
	freq = Frequency()
	base_type = BaseType()

	@translate_params({
		'ano': 'year',
		'periodo': 'period',
		'frecuencia': 'freq',
		'tipo_base': 'base_type'
	})
	def __init__(self,
			year: int,
			period: int,
			freq: str = "trimestre",
			base_type: str = "individual",
		):
		self.year = year
		self.period = period
		self.freq = freq
		self.base_type = self.folder = base_type
		super(MicroData, self).__init__()

	@property
	def filename(self): return "base_{}_{}{}{}.zip".format(
			self.base_type,
			self.year,
			self.freq[0].upper(),
			self.period
			)

	def get_df(self, inform_user=True):
		pd.DataFrame.help = vars_labels
		return super().get_df(inform_user)