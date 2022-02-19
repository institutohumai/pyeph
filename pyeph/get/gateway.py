from pyeph.errors import NonExistentDBError

from .microdata import MicroData
from .basket import Basket
from .equivalent_adult import EquivalentAdult

def get(data,*args, **kwargs):
	handles = {
		'microdata': MicroData,
		'eph': MicroData,
		'basket': Basket,
		'canastas': Basket,
		'adulto-equivalente': EquivalentAdult,
		'equivalent-adult': EquivalentAdult,
	}

	try:
		db_getter = handles[data](*args, **kwargs)
	except KeyError:
		posibles = ", ".join(handles.keys())
		raise NonExistentDBError("Debe seleccionar un tipo de base posible: [{}]".format(posibles))
	return db_getter.get_df()
# Traduccion
obtener = get