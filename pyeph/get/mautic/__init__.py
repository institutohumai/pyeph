from pyeph.tools.decorators import translate_params

from ..getter import Getter

from .types import (
	Year,
	Period,
	BaseType
)


class Mautic(Getter):
	"""
	Módulo de Acceso y Uso de Tecnologías de la Información y la Comunicación (Encuesta Permanente de Hogares)

    Parametros
    ----------
        year : str
            año de la eph
        period : list
            periodo que se desea consultar
	"""

	PREFIX_FOLDER = "mautic"

	year = Year()
	period = Period()
	base_type = BaseType()

	@translate_params({
		'ano': 'year',
		'periodo': 'period',
		'tipo_base': 'base_type'		
	})
	def __init__(self,
			year: int,
			period: int = 4,
			base_type: str = "individual"
		):
		self.year = year
		self.period = period
		self.base_type = base_type
		super(Mautic, self).__init__()

	@property
	def filename(self): return "mautic_{}_{}T{}.zip".format(
			self.base_type,
			self.year,
			self.period
			)

	@property
	def folder(self): return "{}_{}".format(
			self.PREFIX_FOLDER, 
			self.base_type
			)