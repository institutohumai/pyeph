import sys
from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd

from ..getter import Getter

class Basket(Getter):
	"""
		Obtencion del df de la canasta basica
	"""

	folder = "canastas"
	filename = "canastas.zip"

	@staticmethod
	def prepare_basket(df):
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
		region_map = {
			"cuyo": 42,
			"gran_buenos_aires":1,
			"noreste":41,
			"noroeste":40,
			"pampeana":43,
			"patagonia":44
		}
		df['codigo'] = df['region'].map(region_map)
		return df		

	def make_filenames(self, year_month):
		year_month = year_month.strftime('%Y-%m')
		return ['cbt_{}.zip'.format(year_month), 'cba_{}.zip'.format(year_month)]

	def get_df(self, inform_user=True):
		"""
			Retorna el DataFrame
		"""
		df_inicial = pd.DataFrame()
		year_month = date.today()
		query = False
		while query == False:
			try:
				# year_month = date(2021, 6, 1) #.today()
				for f in self.make_filenames(year_month):
					self.filename = f
					df_f =  pd.read_csv(self.get_file(), low_memory=False)
					df_f['tipo_canasta'] = f[:3].upper()
					df_inicial = pd.concat([df_inicial, df_f])
				query = True
			except:
				year_month = year_month - relativedelta(months=1)
		
		if inform_user:
			sys.stdout.write("CBT y CBA mas actualizada que se obtuvo: {} \n".format(year_month.strftime('%Y-%m')))
		df_final = self.prepare_basket(df_inicial)
		
		return df_final
