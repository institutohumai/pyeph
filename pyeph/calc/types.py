# -*- coding: utf-8 -*-
import pandas as pd

class EPHType(object):

	def __get__(self, obj, *args):
		return self.value

	def __set__(self, obj, value):
		if not isinstance(value,pd.DataFrame):
			raise ValueError("eph debe ser un pd.DataFrame")
		self.value = value

class BasketType(object):

	def __get__(self, obj, *args):
		return self.value

	def __set__(self, obj, value):
		if not isinstance(value,pd.DataFrame):
			raise ValueError("canasta debe ser un pd.DataFrame")
		self.value = value
