from pyeph.errors import NonExistentDBError

from .microdata import MicroData
from .basket import Basket
from .equivalent_adult import EquivalentAdult
from .mautic import Mautic

def get(data: str, *args, **kwargs):
	"""
	------------------------------ENGLISH BELOW-------------------------------------
	Esta función permite obtener los resultados de la Encuesta Permanente de Hogares (EPH) 2016-act. provista
	por INDEC.

	Args:
		data (str): solicitud de los datos que necesitas obtener. Posibles argumentos: 'microdata', 'eph',
		'canastas', 'adulto-equivalente', 'mautic'.

	*args:
		'eph':
			year : str
				año de la eph
			freq : str
				tipo de frecuencia "trimestral" u "onda" 
			period : list
				periodo que se desea consultar
			base_type : str, optional
				tipo de base a solicitar "individual", "hogar"
		'mautic':
			year : str
				año de la eph
			period : list
				periodo que se desea consultar

	Returns:
		pandas.DataFrame: Devuelve una estructura de datos columnar de pandas con los datos solicitados.

------------------------------ENGLISH DOCSTRING-------------------------------------

	This function allows to get the results of "Encuesta Permanente de Hogares (EPH) 2016-act.",
	permanent household survey, in Argentina provided by INDEC.

	Args:
		data (str): request about the data to adquire. Possible arguments: 'microdata', 'eph',
		'canastas', 'adulto-equivalente', 'mautic'.

	*args:
		'eph':
			year : str
				year of eph
			freq : str
				frequency about data "trimestral" u "onda" 
			period : list
				period to request.
			base_type : str, optional
				base type to request "individual", "hogar"
		'mautic':
			year : str
				year of eph
			period : list
				period to request.

	Returns:
		pandas.DataFrame: Returns a pandas data structure with the requested data. 
	"""

	
	handles = {
		'microdata': MicroData,
		'eph': MicroData,
		'basket': Basket,
		'canastas': Basket,
		'adulto-equivalente': EquivalentAdult,
		'equivalent-adult': EquivalentAdult,
		'mautic': Mautic
	}

	try:
		db_getter = handles[data](*args, **kwargs)
	except KeyError:
		posibles = ", ".join(handles.keys())
		raise NonExistentDBError("Debe seleccionar un tipo de base posible: [{}]".format(posibles))
	return db_getter.get_df()
# Traduccion
obtener = get
