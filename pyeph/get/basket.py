import io
import logging
from datetime import datetime
import pandas as pd
import re
import requests

from ._base_getter import Getter
from pyeph.errors import DownloadError, NetworkError

logger = logging.getLogger(__name__)

class Basket(Getter):
	"""
		Obtencion del df de la canasta basica.

		Por defecto se intenta obtener la serie completa desde la fuente oficial
		(datos.gob.ar - SSPM), que se actualiza mensualmente. Si esa fuente no
		esta disponible se cae al mirror estatico en https://reflejar.github.io/pyeph-data/,
		que se actualiza con menor frecuencia.
	"""

	folder = "canastas"
	filename = "canastas.zip"

	# Fuente oficial: Subsecretaria de Programacion Macroeconomica (SSPM).
	# Datos publicados por INDEC y republicados mensualmente en datos.gob.ar.
	DATOS_GOB_CBT_URL = (
		"https://infra.datos.gob.ar/catalog/sspm/dataset/446/distribution/446.1/"
		"download/canasta-basica-total-regiones-del-pais.csv"
	)
	DATOS_GOB_CBA_URL = (
		"https://infra.datos.gob.ar/catalog/sspm/dataset/445/distribution/445.1/"
		"download/canasta-basica-alimentaria-regiones-del-pais.csv"
	)

	@staticmethod
	def prepare_basket(df):
		REGION_MAP = {
			"cuyo": 42,
			"gran_buenos_aires":1,
			"noreste":41,
			"noroeste":40,
			"pampeana":43,
			"patagonia":44
		}	
		
		df['indice_tiempo'] =  pd.to_datetime(df['indice_tiempo'])
		df['year'] = df["indice_tiempo"].dt.strftime("%Y")
		df['trim'] = ((df['indice_tiempo'].dt.month-1)//3+1).astype(str)
		df['periodo'] = df['year'] + '.' + df['trim']

		_id_vars = ['indice_tiempo', 'tipo_canasta', 'year', 'trim', 'periodo']
		_value_vars = [c for c in df.columns if c not in _id_vars]

		df =pd.melt(df, id_vars=_id_vars, value_vars=_value_vars, var_name='region', value_name='valor')
		_index = [c for c in df.columns if c not in ['valor', 'tipo_canasta']]
		df = pd.pivot_table(df, values='valor', columns='tipo_canasta', index = _index ,aggfunc='sum' )
		df = df.reset_index()

		df['codigo'] = df['region'].map(REGION_MAP)
		return df		

	def make_filenames(self, year_month):
		year_month = year_month.strftime('%Y-%m')
		return ['cbt_{}.zip'.format(year_month), 'cba_{}.zip'.format(year_month)]
	
	def get_latest_basket_date(self):
		"""
			Consulta el HTML del mirror estatico para obtener la fecha mas reciente
			de canastas disponibles.
			
			Returns
			-------
			datetime
				Fecha de la canasta mas reciente disponible en el mirror estatico.
		"""
		try:
			response = requests.get(self.BASE_GITHUB_URL, timeout=10)
			response.raise_for_status()
			
			pattern = r'canastas/cb[at]_(\d{4}-\d{2})\.zip'
			matches = re.findall(pattern, response.text)
			
			if not matches:
				raise DownloadError("No se encontraron archivos de canastas en la página")
			
			dates = [datetime.strptime(match, '%Y-%m') for match in matches]
			latest_date = max(dates)
			logger.info(f"Última canasta disponible encontrada: {latest_date.strftime('%Y-%m')}")
			return latest_date
			
		except requests.exceptions.RequestException as e:
			logger.error(f"Error al consultar la página: {e}")
			raise NetworkError(f"No se pudo consultar la página de canastas: {e}")
		except ValueError as e:
			logger.error(f"Error al parsear fechas de canastas: {e}")
			raise DownloadError(f"Error al procesar fechas de canastas: {e}")

	def _download_from_datos_gob(self):
		"""
			Descarga las series CBT y CBA desde datos.gob.ar (fuente oficial,
			actualizacion mensual) y las concatena con la columna `tipo_canasta`
			que `prepare_basket` espera.
		"""
		df_inicial = pd.DataFrame()
		for url, tipo in [
			(self.DATOS_GOB_CBT_URL, 'CBT'),
			(self.DATOS_GOB_CBA_URL, 'CBA'),
		]:
			response = requests.get(url, timeout=30)
			response.raise_for_status()
			df_f = pd.read_csv(io.BytesIO(response.content), low_memory=False)
			df_f['tipo_canasta'] = tipo
			df_inicial = pd.concat([df_inicial, df_f])
		return df_inicial

	def _download_from_github_mirror(self):
		"""
			Fallback: descarga las canastas desde el mirror estatico en
			github pages. Devuelve el DataFrame crudo y la fecha (year-month)
			que se logro recuperar.
		"""
		df_inicial = pd.DataFrame()
		year_month = self.get_latest_basket_date()
		for f in self.make_filenames(year_month):
			self.filename = f
			df_f = pd.read_csv(self.get_file(), low_memory=False)
			df_f['tipo_canasta'] = f[:3].upper()
			df_inicial = pd.concat([df_inicial, df_f])
	
		
		if inform_user:
			message = "CBT y CBA mas actualizada que se obtuvo: {}".format(year_month.strftime('%Y-%m'))
			logger.info(message)
		
		df_final = self.prepare_basket(df_inicial)
		return df_final
