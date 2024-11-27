from datetime import date

from pyeph.tools.decorators import translate_params

from ._base_getter import Getter

class BaseType:

	VALUES = ['individual','hogar']

	def __get__(self, obj, *args):
		return self.value

	def __set__(self, obj, value):
		if not (isinstance(value,str) and value in self.VALUES):
			raise ValueError("Por favor ingresa un tipo de base valido: " + ", ".join(self.VALUES))
		self.value = value


class Year:

	INITIAL_YEAR = 2016

	def __get__(self, obj, *args):
		return self.value

	def __set__(self, obj, value):
		current_year = date.today().year
		if not (isinstance(value,int) and self.INITIAL_YEAR <= value <= current_year):
			raise ValueError("El año debe ser un número entre {} y {}.".format(self.INITIAL_YEAR, current_year))
		self.value = value



class Period:

	VALUES = [4]

	def __get__(self, obj, *args):
		return self.value

	def __set__(self, obj, value):
		if not (
			(isinstance(value,int) and value in self.VALUES) or
			value is None
		):
			raise ValueError("Por favor ingresa un numero de trimeste valido: " + ",".join(map(str, self.VALUES)))
		self.value = value



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