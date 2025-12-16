import sys
import logging
from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd

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

	def get_df(self, inform_user=True, max_retries=24):
		"""
			Retorna el DataFrame
			
			Parameters
			----------
			inform_user : bool, optional
				Mostrar mensaje informativo al usuario (default: True)
			max_retries : int, optional
				Número máximo de meses hacia atrás para buscar canastas (default: 24)
		"""
		df_inicial = pd.DataFrame()
		year_month = date.today()
		query = False
		attempts = 0
		
		while not query and attempts < max_retries:
			try:
				logger.debug(f"Intentando descargar canastas para: {year_month.strftime('%Y-%m')}")
				for f in self.make_filenames(year_month):
					self.filename = f
					df_f = pd.read_csv(self.get_file(), low_memory=False)
					df_f['tipo_canasta'] = f[:3].upper()
					df_inicial = pd.concat([df_inicial, df_f])
				query = True
				logger.info(f"Canastas obtenidas exitosamente para: {year_month.strftime('%Y-%m')}")
			except (DownloadError, NetworkError) as e:
				logger.warning(f"No se encontraron canastas para {year_month.strftime('%Y-%m')}: {e}")
				year_month = year_month - relativedelta(months=1)
				attempts += 1
			except Exception as e:
				logger.error(f"Error inesperado al obtener canastas para {year_month.strftime('%Y-%m')}: {e}")
				year_month = year_month - relativedelta(months=1)
				attempts += 1
		
		if not query:
			error_msg = f"No se pudieron obtener canastas después de {max_retries} intentos"
			logger.error(error_msg)
			raise DownloadError(error_msg)
		
		if inform_user:
			message = "CBT y CBA mas actualizada que se obtuvo: {}".format(year_month.strftime('%Y-%m'))
			logger.info(message)
			
		df_final = self.prepare_basket(df_inicial)
		return df_final
