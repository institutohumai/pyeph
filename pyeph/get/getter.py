import os
import sys
import zipfile
import wget
import pandas as pd

from pyeph.errors import NonExistentDBError

MODULE_PATH = os.getcwd()


class Getter:
    """
	Obtencion de archivos para su posterior tratamiento 
	Utiliza los atributos de cada tipo de obtencion declarado en el archivo __init__.py

    Retorno en .get_file()
    -------
        file : str
			archivo .csv ubicado dentro del .zip con el mismo nombre

    Retorno en .get_df()
    -------
        df : pandas.DataFrame
			dataframe del .csv solicitado
	"""

    BASE_GITHUB_URL = "https://github.com/reflejar/pyeph-data/raw/master/"
    URL_INDEC = "https://www.indec.gob.ar/ftp/cuadros/menusuperior/eph"
    DEFAULT_DIR = "pyeph/.db"

    @property
    def download_base_folder(self):
        # ruta/completa/db/
        return os.path.join(MODULE_PATH, self.DEFAULT_DIR)

    @property
    def download_type_folder(self):
        # ruta/completa/db/tipo
        return os.path.join(self.download_base_folder, self.folder)

    @property
    def download_destination(self):
        # ruta/completa/db/tipo/archivo
        return os.path.join(self.download_type_folder, self.filename)

    def from_indec(self):
        pass

    def from_github(self):
        pathfile = os.path.join(self.BASE_GITHUB_URL, self.folder, self.filename).replace('\\', '/')
        wget.download(pathfile, self.download_destination)

    def download(self):
        try:
            self.from_github()
            sys.stdout.write("\n")
        except:
            raise NonExistentDBError()

    def check_if_exists(self):
        # Se fija si existe en el directorio. Caso contrario lo descarga
        base_folder = self.download_base_folder
        if not os.path.exists(base_folder):
            os.makedirs(base_folder)
        type_folder = self.download_type_folder
        if not os.path.exists(type_folder):
            os.makedirs(type_folder)
        zip_file = self.download_destination
        if not os.path.exists(zip_file):
            self.download()
        return zip_file

    def get_file(self):
        # Aquí hay que agregar un progress bar
        zip_file = self.check_if_exists()
        zip_file = zipfile.ZipFile(zip_file, 'r')
        csv_file = zip_file.open(self.filename.replace('.zip', '.csv'), 'r')
        return csv_file

    def get_df(self, inform_user=True):
        """
			Retorna el DataFrame
		"""
        df = pd.read_csv(self.get_file(), low_memory=False)
        if inform_user:
            sys.stdout.write("Obtenido con exito: {} \n".format(self.filename))
        return df
