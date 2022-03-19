from datetime import date

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

