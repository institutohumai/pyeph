import logging
from datetime import date

from pyeph.tools.decorators import translate_params

from pyeph.errors import DownloadError, NetworkError, NonExistentDBError

from ._base_getter import Getter, URL_INDEC_ENTIC_BASE

logger = logging.getLogger(__name__)

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

	def _download_from_indec(self):
		yy = str(self.year)[-2:]
		url = f"{URL_INDEC_ENTIC_BASE}/EPH_Base_Usu_Tic_T{self.period}{yy}.zip"
		zip_bytes = self._download_indec_zip(url)
		needle = "hog" if self.base_type == "hogar" else "indiv"

		def txt_basename_predicate(name: str) -> bool:
			low = name.lower()
			return low.endswith(".txt") and needle in low

		self._repackage_txt_to_csv_zip(
			zip_bytes,
			txt_basename_predicate=txt_basename_predicate,
			normalizers=[],
			destination=self.download_destination,
		)

	def download(self):
		# 2016-2017: URL distinta en INDEC; el mirror las tiene estandarizadas.
		if self.period == 4 and 2018 <= self.year <= 2023:
			try:
				self._download_from_indec()
				logger.info(f"Descarga exitosa desde INDEC: {self.filename}")
				return
			except (NetworkError, DownloadError, NonExistentDBError) as e:
				logger.warning(
					"INDEC no respondio para %s; cayendo al mirror estatico (%s)",
					self.filename,
					e,
				)
		super().download()