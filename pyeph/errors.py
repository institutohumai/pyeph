class BaseError(Exception):
	"""
		Base Error
	"""
	def __init__(self, message=None):
		self.message = message or self.__doc__
		super(BaseError, self).__init__(self.message.strip())


class NonExistentDBError(BaseError):
	"""
		La base solicitada no fue provista por INDEC.
	"""


class DownloadError(BaseError):
	"""
		Error al descargar el archivo solicitado.
	"""


class NetworkError(BaseError):
	"""
		Error de conexión de red.
	"""
