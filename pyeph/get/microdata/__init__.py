# -*- coding: utf-8 -*-
from pyeph.decorators import translate_params

from ..getter import Getter
from .validator import MicroDataValidator
from .types import (
	Year,
	Period,
	Frequency,
	BaseType
)


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
			year,
			period,
			freq="trimestre",
			base_type="individual",
			*args, **kwargs
		):
		self.year = year
		self.period = period
		self.freq = freq
		self.base_type = self.folder = base_type
		super(MicroData, self).__init__(*args, **kwargs)

	@property
	def filename(self): return "base_{}_{}{}{}.zip".format(
			self.base_type,
			self.year,
			self.freq[0].upper(),
			self.period
			)
