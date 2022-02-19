# -*- coding: utf-8 -*-
import sys

from pyeph.errors import *

from .types import Frequency

class MicroDataValidator(object):
	"""
		Validacion de datos para la consulta de las bases
	"""

	def __init__(self):
		self.handle_exceptions_warnings()

	def valid_period_freq(self):
		if self.period > Frequency.VALUES[self.freq]:
			raise ValueError("La frecuencia solicitada ({}) requiere un periodo menor o igual a {}".format(self.freq, Frequency.VALUES[self.freq]))

	def valid_year_freq(self):
		if self.year <= 2003 and self.freq != 'onda': 
			raise ValueError("Para bases de datos hasta 2003, el tipo de frecuencia (freq) debe ser 'onda'")

	def valid_existent_db(self):
		error = None
		if self.year==2007 and self.period==3:
			error = """INDEC advierte: La informacion correspondiente al tercer trimestre 
	 				2007 no esta disponible ya que los aglomerados Mar del Plata-Batan, 
	 				Bahia Blanca-Cerri y Gran La Plata no fueron relevados por causas 
	 				de orden administrativo, mientras que los datos correspondientes al 
	 				Aglomerado Gran Buenos Aires no fueron relevados por paro del 
	 				personal de la EPH."""

		if (self.year ==2015 and self.period in [3,4]) or (self.year==2016 and self.period==1):
	 		error = """En el marco de la emergencia estadistica el INDEC no publico la base solicitada. 
	 				Mas informacion en: https://www.indec.gob.ar/ftp/cuadros/sociedad/anexo_informe_eph_23_08_16.pdf"""

		if error:
			raise NonExistentDBError(error)

		if self.year >= 2007 and self.year <= 2015:
			message = '''
				INDEC advierte:
					Advertencia sobre el uso de series estadisticas. Se advierte que las series estadisticas publicadas con
					posterioridad a enero del 2007 y hasta diciembre 2015 deben ser consideradas con reservas,
					excepto las que ya hayan sido revisadas en 2016 y su difusion lo consigne expresamente.
					El INDEC, en el marco de las atribuciones conferidas por los decretos 181/15 y 55/16, dispuso las investigaciones
					requeridas para establecer la regularidad de procedimientos de obtencion de datos, su procesamiento, elaboracion de indicadores y difusion
					Mas informacion en: https://www.indec.gob.ar/ftp/cuadros/sociedad/anexo_informe_eph_23_08_16.pdf
			'''
			sys.stdout.write(message.strip())
			
	def handle_exceptions_warnings(self):
		self.valid_period_freq()
		self.valid_year_freq()
		self.valid_existent_db()
