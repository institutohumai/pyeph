import logging
from importlib import resources

import pandas as pd

from ._base_getter import Getter

logger = logging.getLogger(__name__)


class EquivalentAdult(Getter):
	"""
		Obtencion del df de adulto equivalente (tabla de referencia empaquetada).
	"""

	folder = "adulto_equivalente"
	filename = "adulto_equivalente.zip"

	def get_df(self, inform_user=True):
		ref = resources.files("pyeph.data").joinpath("adulto_equivalente.csv")
		with ref.open("rb") as f:
			df = pd.read_csv(f, low_memory=False)
		if inform_user:
			logger.info("Adulto equivalente cargado desde datos empaquetados (pyeph.data)")
		return df
