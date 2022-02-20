from pyeph.calc.calculator import Calculator


class Template(Calculator):
    """
        Template para agregar nuevos calculos.

		Notas:
			Para crear un nuevo calculo es necesario copiar la carpeta "template", pegar y renombrar
			Se deben agregar constantes como atributos de las clases de cada calculo
			Estos atributos serán las columnas necesarias para el calculo que se pretende agregar
			con "VAR_EPH_nombrecolumna" (ver VAR_EPH_EJEMPLO mas abajo)
			Esto es necesario para que el nuevo calculo no trabaje sobre el DataFrame completo
			sino mas bien sobre las columnas necesarias
    """
    # Constantes EPH

    VAR_EPH_EJEMPLO = 'EJEMPLO'

    def __init__(self, eph):
        self.eph = eph
    
    def run(self): return

    # Traduccion
    correr = run
# Traduccion
Plantilla = Template