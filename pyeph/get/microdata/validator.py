import sys

from pyeph.errors import *
from pyeph.ads import (
	INDEC_2007_2015,
	INDEC_2007_3,
	INDEC_STATS_EMERGENCY,
	QUARTER_OR_WAVE_OPTION
)

from .types import Frequency

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
			sys.stdout.write(INDEC_2007_2015)
			
	def handle_exceptions_warnings(self):
		self.valid_period_freq()
		self.valid_year_freq()
		self.valid_existent_db()
