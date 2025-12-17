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
		Obtencion del df de la canasta basica
	"""

	folder = "canastas"
	filename = "canastas.zip"

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
			Consulta el HTML de la página para obtener la fecha más reciente de canastas disponibles
			
			Returns
			-------
			datetime
				Fecha de la canasta más reciente disponible
		"""
		try:
			response = requests.get(self.BASE_GITHUB_URL, timeout=10)
			response.raise_for_status()
			
			# Buscar todos los archivos de canastas en el HTML
			pattern = r'canastas/cb[at]_(\d{4}-\d{2})\.zip'
			matches = re.findall(pattern, response.text)
			
			if not matches:
				raise DownloadError("No se encontraron archivos de canastas en la página")
			
			# Convertir a fechas y encontrar la más reciente
			dates = [datetime.strptime(match, '%Y-%m') for match in matches]
			latest_date = max(dates)
			logger.info(f"Última canasta disponible encontrada: {latest_date.strftime('%Y-%m')}")
			return latest_date
			
		except requests.RequestException as e:
			logger.error(f"Error al consultar la página: {e}")
			raise NetworkError(f"No se pudo consultar la página de canastas: {e}")
		except ValueError as e:
			logger.error(f"Error al parsear fechas de canastas: {e}")
			raise DownloadError(f"Error al procesar fechas de canastas: {e}")

	def get_df(self, inform_user=True):
		"""
			Retorna el DataFrame
			
			Parameters
			----------
			inform_user : bool, optional
				Mostrar mensaje informativo al usuario (default: True)
		"""
		df_inicial = pd.DataFrame()
		
		# Intentar obtener la fecha más reciente desde el HTML
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
